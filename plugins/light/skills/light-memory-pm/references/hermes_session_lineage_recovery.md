# Hermes session lineage recovery

Use this reference when a Hermes conversation/window appears missing, the latest restored chat looks too short, or the user wants a long compressed task restored under a workspace.

## Durable lesson

Hermes long tasks may be split across many sessions through context compression. The visible `hermes sessions list` view is not a complete recovery view: archived sessions, child sessions, and continuation branches can exist in `state.db` while not appearing as standalone recent sessions.

## Recovery pattern

1. Identify the current active session and suspected tail session.
2. Inspect the canonical `state.db` for `sessions` and `messages`, including `archived`, `cwd`, `parent_session_id`, `started_at`, `ended_at`, and message counts.
3. Walk the main chain backward from the suspected tail via `parent_session_id`, then reverse it for chronology.
4. Recursively enumerate descendants from the root to capture branches/new windows.
5. Back up `state.db` before metadata edits.
6. Export all related messages to JSONL and write a Markdown index with session IDs, titles, timestamps, counts, cwd, and backup path.
7. Restore metadata conservatively: unarchive related sessions, normalize `cwd` only when the user explicitly requested that workspace, and prefix titles for grouping.
8. Verify the visible sessions list after edits. If setting the current session as a child hides it, keep the current workspace session top-level and rely on title/cwd/index for grouping.

## Pitfall

Do not report only the latest `#N` continuation as “the conversation.” It may contain only the final tail. Report the full main-chain and full-subtree counts separately.