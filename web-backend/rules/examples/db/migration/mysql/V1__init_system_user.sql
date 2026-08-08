-- Flyway MySQL 样板（表名/字段按项目调整）
CREATE TABLE IF NOT EXISTS sys_user (
    id           BIGINT       NOT NULL PRIMARY KEY COMMENT '雪花 ID',
    username     VARCHAR(32)  NOT NULL COMMENT '登录用户名',
    email        VARCHAR(128) NULL COMMENT '邮箱',
    phone        VARCHAR(32)  NULL COMMENT '手机号',
    status       VARCHAR(16)  NOT NULL DEFAULT 'ENABLED' COMMENT '状态：ENABLED/DISABLED',
    deleted      TINYINT      NOT NULL DEFAULT 0 COMMENT '逻辑删除标记：0=未删除,1=已删除',
    version      INT          NOT NULL DEFAULT 0 COMMENT '乐观锁版本号',
    created_at   DATETIME(3)  NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '创建时间',
    updated_at   DATETIME(3)  NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '更新时间',
    UNIQUE KEY uk_sys_user_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统用户表';
