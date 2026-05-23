-- Flyway MySQL 样板（表名/字段按项目调整）
CREATE TABLE IF NOT EXISTS sys_user (
    id           BIGINT       NOT NULL PRIMARY KEY COMMENT '雪花 ID',
    username     VARCHAR(32)  NOT NULL,
    email        VARCHAR(128) NULL,
    phone        VARCHAR(32)  NULL,
    status       VARCHAR(16)  NOT NULL DEFAULT 'ENABLED',
    deleted      TINYINT      NOT NULL DEFAULT 0,
    version      INT          NOT NULL DEFAULT 0,
    created_at   DATETIME(3)  NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    updated_at   DATETIME(3)  NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    UNIQUE KEY uk_sys_user_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
