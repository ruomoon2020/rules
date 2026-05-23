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
