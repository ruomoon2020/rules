package com.company.product.modules.system.application;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.company.product.common.exception.BusinessException;
import com.company.product.common.exception.ErrorCodes;
import com.company.product.common.web.PageResponse;
import com.company.product.modules.system.api.dto.UserCreateRequest;
import com.company.product.modules.system.api.dto.UserDetailResponse;
import com.company.product.modules.system.api.dto.UserPageQuery;
import com.company.product.modules.system.api.dto.UserSummaryResponse;
import com.company.product.modules.system.api.dto.UserUpdateRequest;
import com.company.product.modules.system.application.audit.AuditRecordCommand;
import com.company.product.modules.system.application.audit.AuditRecorder;
import com.company.product.modules.system.application.converter.UserConverter;
import com.company.product.modules.system.domain.User;
import com.company.product.modules.system.infrastructure.mapper.UserMapper;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.util.Map;

@Service
public class UserService {

    private static final Map<String, String> SORT_WHITELIST = Map.of(
            "createdAt", "created_at"
    );

    private final UserMapper userMapper;
    private final UserConverter userConverter;
    private final AuditRecorder auditRecorder;

    public UserService(UserMapper userMapper, UserConverter userConverter, AuditRecorder auditRecorder) {
        this.userMapper = userMapper;
        this.userConverter = userConverter;
        this.auditRecorder = auditRecorder;
    }

    @Transactional(readOnly = true)
    public PageResponse<UserSummaryResponse> page(UserPageQuery query) {
        Page<User> page = new Page<>(query.page(), query.pageSize());
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        if (StringUtils.hasText(query.status())) {
            wrapper.eq(User::getStatus, query.status());
        }
        if (StringUtils.hasText(query.keyword())) {
            wrapper.like(User::getUsername, query.keyword());
        }
        applySort(wrapper, query.sortField(), query.sortOrder());
        userMapper.selectPage(page, wrapper);
        return userConverter.toPageResponse(page);
    }

    @Transactional(readOnly = true)
    public UserDetailResponse detail(long id) {
        User user = userMapper.selectById(id);
        if (user == null) {
            throw new BusinessException(ErrorCodes.USER_NOT_FOUND, "用户不存在", HttpStatus.NOT_FOUND);
        }
        return userConverter.toDetail(user);
    }

    @Transactional
    public UserDetailResponse create(UserCreateRequest request) {
        User entity = userConverter.toEntity(request);
        userMapper.insert(entity);
        return userConverter.toDetail(entity);
    }

    @Transactional
    public UserDetailResponse update(long id, UserUpdateRequest request) {
        User user = userMapper.selectById(id);
        if (user == null) {
            throw new BusinessException(ErrorCodes.USER_NOT_FOUND, "用户不存在", HttpStatus.NOT_FOUND);
        }
        if (request.email() != null) {
            user.setEmail(request.email());
        }
        if (request.status() != null) {
            user.setStatus(request.status());
        }
        userMapper.updateById(user);
        return userConverter.toDetail(user);
    }

    @Transactional
    public void delete(long id) {
        User user = userMapper.selectById(id);
        if (user == null) {
            throw new BusinessException(ErrorCodes.USER_NOT_FOUND, "用户不存在", HttpStatus.NOT_FOUND);
        }
        String beforeSummary = "username=" + user.getUsername() + ",status=" + user.getStatus();
        // 同一事务内先写审计再删数据；审计失败则整体回滚（阻断型操作，见 27-audit-log.md）
        auditRecorder.record(AuditRecordCommand.success(
                "USER_DELETE",
                "User",
                String.valueOf(id),
                beforeSummary
        ));
        userMapper.deleteById(id);
    }

    private void applySort(LambdaQueryWrapper<User> wrapper, String sortField, String sortOrder) {
        if (!StringUtils.hasText(sortField)) {
            wrapper.orderByDesc(User::getCreatedAt);
            return;
        }
        String column = SORT_WHITELIST.get(sortField);
        if (column == null) {
            throw new BusinessException(ErrorCodes.INTERNAL_ERROR, "非法排序字段");
        }
        boolean asc = "asc".equalsIgnoreCase(sortOrder);
        wrapper.last("ORDER BY " + column + (asc ? " ASC" : " DESC"));
    }
}
