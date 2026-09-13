# CLAUDE.md

> Claude Code operational brief. Synchronized with repository AGENTS.md.

@AGENTS.md

## Claude Code Specific Directives
- **Session Continuity**: Always check `.agent/memory-bank/activeContext.md` upon initialization.
- **Minimal Diffs**: Target exact edits rather than regenerating whole files.
- **Verification**: Run the test suite before reporting task completion.
- **Scratch Scripts**: Place temporary debug scripts in `.agent/scratch/`.
