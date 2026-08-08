-- 审计日志表（MySQL 样板），字段与 openapi AuditLogResponse / fullstack-contract 对齐
CREATE TABLE IF NOT EXISTS sys_audit_log (
    id              BIGINT        NOT NULL PRIMARY KEY COMMENT '雪花 ID',
    tenant_id       VARCHAR(64)   NULL COMMENT '租户 ID；单租户项目可为空',
    operator_id     VARCHAR(64)   NOT NULL COMMENT '操作者用户 ID 或系统主体 ID',
    action          VARCHAR(64)   NOT NULL COMMENT '操作动作编码',
    resource_type   VARCHAR(64)   NOT NULL COMMENT '资源类型编码',
    resource_id     VARCHAR(128)  NULL COMMENT '资源 ID',
    request_summary VARCHAR(512)  NULL COMMENT '请求摘要；禁止记录敏感明文',
    file_name       VARCHAR(256)  NULL COMMENT '文件名；导入导出场景使用',
    before_summary  VARCHAR(1024) NULL COMMENT '变更前摘要；禁止记录敏感明文',
    after_summary   VARCHAR(1024) NULL COMMENT '变更后摘要；禁止记录敏感明文',
    result          VARCHAR(16)   NOT NULL COMMENT '操作结果：SUCCESS/FAIL',
    error_code      VARCHAR(64)   NULL COMMENT '失败错误码',
    trace_id        VARCHAR(64)   NULL COMMENT '链路追踪 ID',
    ip              VARCHAR(64)   NULL COMMENT '客户端 IP',
    user_agent      VARCHAR(512)  NULL COMMENT '客户端 User-Agent',
    occurred_at     DATETIME(3)   NOT NULL COMMENT '业务发生时间',
    created_at      DATETIME(3)   NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '记录创建时间',
    KEY idx_audit_occurred (occurred_at),
    KEY idx_audit_operator (operator_id, occurred_at),
    KEY idx_audit_action (action, occurred_at),
    KEY idx_audit_resource (resource_type, resource_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统审计日志表';
