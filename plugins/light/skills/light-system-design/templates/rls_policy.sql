-- PostgreSQL 行级安全 (RLS) 骨架（多租户起手模板）
-- 约定要点见 ../references.md 与 SKILL.md「安全与运维 / 行级安全」段。
-- 配合 schema.sql 使用；落地前用真实角色跑通再上线。
--
-- ⚠ 关于下文的 auth.tenant_id()：它【不是】内置函数，必须自行定义。
--   - Supabase 内置的只有 auth.uid() / auth.jwt()，并【没有】 auth.tenant_id()。
--   - 可移植做法（不依赖 Supabase）：用会话变量取租户 id，连接建立后由应用
--     执行 `SET app.tenant_id = '<id>';`（或事务级 SET LOCAL），policy 里读：
--       create or replace function auth.tenant_id() returns bigint
--       language sql stable as $$
--         select nullif(current_setting('app.tenant_id', true), '')::bigint
--       $$;
--     第二参 true 表示变量未设置时返回 NULL 而非报错（未设置即拒绝所有行）。
--   - Supabase 场景另一做法：从 JWT 取，如
--       create or replace function auth.tenant_id() returns bigint
--       language sql stable as $$
--         select nullif(auth.jwt() -> 'app_metadata' ->> 'tenant_id', '')::bigint
--       $$;
--     租户 id 务必放 raw_app_meta_data（用户改不了），别放 raw_user_meta_data。
--   先建好上面任一函数，下面的 policy 才能跑通。

-- 1. 开启 RLS（开启后默认拒绝所有访问，必须显式加 policy）
alter table app_user enable row level security;

-- 2. 分操作写 policy，永远写 to 子句（限定角色，别让 policy 对所有角色生效）
-- select：用户只能看本租户数据
create policy app_user_select on app_user
    for select to authenticated
    using (tenant_id = (select auth.tenant_id()));   -- 函数包进 select 触发 initPlan 缓存，避免逐行求值

-- insert：只能往自己租户插
create policy app_user_insert on app_user
    for insert to authenticated
    with check (tenant_id = (select auth.tenant_id()));

-- update：只能改自己租户，且改完仍属本租户
create policy app_user_update on app_user
    for update to authenticated
    using (tenant_id = (select auth.tenant_id()))
    with check (tenant_id = (select auth.tenant_id()));

-- 3. policy 引用的列要建索引（否则每行求值走全表扫）
create index if not exists idx_app_user_tenant_rls on app_user(tenant_id);

-- 性能与安全注意：
--   * 授权数据用 raw_app_meta_data（用户改不了），别用 raw_user_meta_data。
--   * 复杂跨表判断别在 policy 里 join，改子查询 IN，或封装成 security definer
--     函数放非暴露 schema，避免 RLS 递归与性能塌方。
--   * 验证：以目标角色 set role authenticated; 跑查询，确认只返回本租户行。
