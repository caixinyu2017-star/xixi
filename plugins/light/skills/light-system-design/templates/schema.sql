-- PostgreSQL 建表骨架（约定起手模板，非完整业务模型）
-- 用法：按项目改表名/字段；落地前用 EXPLAIN ANALYZE 验证索引、人工审迁移。
-- 约定要点见 ../references.md 与 SKILL.md「数据库」段。

-- 主键二选一：① bigint generated always as identity（单库高性能）
--             ② uuid（分布式/不暴露自增量；用 gen_random_uuid()，需 pgcrypto）
create table tenant (
    id          bigint generated always as identity primary key,
    name        text        not null,
    created_at  timestamptz not null default now(),   -- 审计列：创建时间
    updated_at  timestamptz not null default now()    -- 审计列：更新时间（配触发器自动刷新）
);

create table app_user (
    id          bigint generated always as identity primary key,
    tenant_id   bigint      not null references tenant(id) on delete cascade,
    email       text        not null,
    role        text        not null default 'member'
                            check (role in ('owner','admin','member')),  -- CHECK 约束示例
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now(),
    unique (tenant_id, email)              -- 同租户内邮箱唯一
);

-- 外键列必须建索引（PostgreSQL 不自动为外键建索引，否则父表删除/级联会全表扫）
create index idx_app_user_tenant on app_user(tenant_id);

-- 大表/线上加索引用 CONCURRENTLY（不锁写）；注意：不能在事务块内执行，需单独跑
-- create index concurrently idx_app_user_email on app_user(email);

-- 验证：EXPLAIN (ANALYZE, BUFFERS) select ... where tenant_id = $1;
-- 看是否走 idx_app_user_tenant，而非 Seq Scan。
