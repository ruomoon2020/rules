-- Flyway PostgreSQL 样板
CREATE TABLE IF NOT EXISTS sys_user (
    id           BIGINT       PRIMARY KEY,
    username     VARCHAR(32)  NOT NULL,
    email        VARCHAR(128),
    phone        VARCHAR(32),
    status       VARCHAR(16)  NOT NULL DEFAULT 'ENABLED',
    deleted      SMALLINT     NOT NULL DEFAULT 0,
    version      INT          NOT NULL DEFAULT 0,
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    CONSTRAINT uk_sys_user_username UNIQUE (username)
);

COMMENT ON TABLE sys_user IS '系统用户表';
COMMENT ON COLUMN sys_user.id IS '雪花 ID';
COMMENT ON COLUMN sys_user.username IS '登录用户名';
COMMENT ON COLUMN sys_user.email IS '邮箱';
COMMENT ON COLUMN sys_user.phone IS '手机号';
COMMENT ON COLUMN sys_user.status IS '状态：ENABLED/DISABLED';
COMMENT ON COLUMN sys_user.deleted IS '逻辑删除标记：0=未删除,1=已删除';
COMMENT ON COLUMN sys_user.version IS '乐观锁版本号';
COMMENT ON COLUMN sys_user.created_at IS '创建时间';
COMMENT ON COLUMN sys_user.updated_at IS '更新时间';
