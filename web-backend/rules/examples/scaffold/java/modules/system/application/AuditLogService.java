package com.company.product.modules.system.application;

import com.company.product.common.exception.BusinessException;
import com.company.product.common.exception.ErrorCodes;
import com.company.product.common.web.PageResponse;
import com.company.product.modules.system.api.dto.AuditLogPageQuery;
import com.company.product.modules.system.api.dto.AuditLogResponse;
import com.company.product.modules.system.api.dto.AuditLogSummaryResponse;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 审计日志查询（样板）。写入见 {@link com.company.product.modules.system.application.audit.AuditRecorder}。
 */
@Service
public class AuditLogService {

    @Transactional(readOnly = true)
    public PageResponse<AuditLogSummaryResponse> page(AuditLogPageQuery query) {
        // 样板：接入 sys_audit_log 表与 Mapper；此处返回空页
        return new PageResponse<>(query.page(), query.pageSize(), 0, List.of());
    }

    @Transactional(readOnly = true)
    public AuditLogResponse detail(String id) {
        // 样板：按 id 查询；未实现时抛业务异常
        throw new BusinessException(ErrorCodes.AUDIT_LOG_NOT_FOUND, "audit log not found: " + id);
    }
}
