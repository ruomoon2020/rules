-- 审计日志表（MySQL 样板），字段与 openapi AuditLogResponse / fullstack-contract 对齐
CREATE TABLE IF NOT EXISTS sys_audit_log (
    id              BIGINT        NOT NULL PRIMARY KEY COMMENT '雪花 ID',
    tenant_id       VARCHAR(64)   NULL,
    operator_id     VARCHAR(64)   NOT NULL,
    action          VARCHAR(64)   NOT NULL,
    resource_type   VARCHAR(64)   NOT NULL,
    resource_id     VARCHAR(128)  NULL,
    request_summary VARCHAR(512)  NULL,
    file_name       VARCHAR(256)  NULL,
    before_summary  VARCHAR(1024) NULL,
    after_summary   VARCHAR(1024) NULL,
    result          VARCHAR(16)   NOT NULL,
    error_code      VARCHAR(64)   NULL,
    trace_id        VARCHAR(64)   NULL,
    ip              VARCHAR(64)   NULL,
    user_agent      VARCHAR(512)  NULL,
    occurred_at     DATETIME(3)   NOT NULL,
    created_at      DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    KEY idx_audit_occurred (occurred_at),
    KEY idx_audit_operator (operator_id, occurred_at),
    KEY idx_audit_action (action, occurred_at),
    KEY idx_audit_resource (resource_type, resource_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
