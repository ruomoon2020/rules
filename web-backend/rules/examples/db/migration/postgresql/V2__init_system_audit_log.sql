-- 审计日志表（PostgreSQL 样板）
CREATE TABLE IF NOT EXISTS sys_audit_log (
    id              BIGINT        PRIMARY KEY,
    tenant_id       VARCHAR(64),
    operator_id     VARCHAR(64)   NOT NULL,
    action          VARCHAR(64)   NOT NULL,
    resource_type   VARCHAR(64)   NOT NULL,
    resource_id     VARCHAR(128),
    request_summary VARCHAR(512),
    file_name       VARCHAR(256),
    before_summary  VARCHAR(1024),
    after_summary   VARCHAR(1024),
    result          VARCHAR(16)   NOT NULL,
    error_code      VARCHAR(64),
    trace_id        VARCHAR(64),
    ip              VARCHAR(64),
    user_agent      VARCHAR(512),
    occurred_at     TIMESTAMPTZ   NOT NULL,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_occurred ON sys_audit_log (occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_operator ON sys_audit_log (operator_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_action ON sys_audit_log (action, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_resource ON sys_audit_log (resource_type, resource_id);
