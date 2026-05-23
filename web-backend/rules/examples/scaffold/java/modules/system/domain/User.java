package com.company.product.modules.system.domain;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableLogic;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.annotation.Version;

import java.time.Instant;

/**
 * 用户实体（样板）。禁止作为 REST 出参。
 */
@TableName("sys_user")
public class User {

    @TableId
    private Long id;
    private String username;
    private String email;
    private String phone;
    private String status;
    @TableLogic
    private Integer deleted;
    @Version
    private Integer version;
    private Instant createdAt;
    private Instant updatedAt;

    // getter/setter 或使用 Lombok @Data（按项目约定）
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
}
