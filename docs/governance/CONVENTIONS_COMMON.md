# Common Conventions

## Workflow

- Task lifecycle: `Todo -> InProgress -> QAReady -> ValidatorPass -> Committed -> Done`
- Failure path: `* -> Rework -> QAReady`
- One task per commit.

## Branch

- Codex orchestration branch naming: `codex/<scope>`

## Merge

- 대형 구조 변경 PR: `Merge Commit` 우선
- 소규모 문서/정리 PR: `Squash Merge`
- 해시 추적 문서가 있으면 `Rebase Merge` 지양
