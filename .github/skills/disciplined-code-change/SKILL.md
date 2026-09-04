---
name: disciplined-code-change
description: 'Use when modifying an existing codebase: trace the concrete behavior, form a falsifiable hypothesis, make the smallest focused edit, validate immediately, and report residual risk. Applies to bug fixes, feature changes, refactors, notebook-backed Python work, and test repairs.'
argument-hint: 'Describe the requested behavior, affected file or failing check, and any constraints.'
user-invocable: true
disable-model-invocation: false
---

# Disciplined Code Change

## Purpose

Turn a code-change request into a verified, focused change. Preserve the repository's existing conventions and leave unrelated work untouched.

## Procedure

1. **Anchor the request.** Start from the named file, symbol, failing behavior, command, test, or nearest implementation surface. If none is named, perform one targeted search to find it.
2. **Read locally.** Inspect only the owning code path plus one nearby test, call site, or abstraction boundary when needed. Check repository instructions and the current worktree before editing.
3. **State a hypothesis.** Identify the code path that controls the behavior and write one falsifiable explanation of the problem or expected change. Name the cheapest check that could disconfirm it.
4. **Choose the smallest slice.** Prefer the existing abstraction and local patterns. Avoid unrelated cleanup, broad refactors, API changes, and formatting churn.
5. **Edit directly.** Make a small, reversible change. Add or adjust focused tests when the behavior is not already covered. Do not overwrite user changes.
6. **Validate immediately.** Run the cheapest behavior-scoped check available, then a narrow test, compile, lint, typecheck, or notebook execution as appropriate. Do this before broad exploration or adjacent edits.
7. **React to the result.**
   - If validation supports the hypothesis but exposes a local defect, repair the same slice and rerun the same check.
   - If validation disproves the hypothesis, take one nearby hop toward the code that directly controls the behavior, revise the hypothesis, and make the smallest next edit.
   - If validation is ambiguous, perform one nearby disambiguating read or call-site/test check before deciding.
   - Do not attempt to fix unrelated failures; record them as residual risk.
8. **Finish with executable evidence.** Run at least one post-edit executable validation whenever the environment provides one. For notebooks, execute the affected cell or a minimal reproducible path and inspect its output. If no executable check is available, use a diff review and syntax/static inspection.
9. **Report concisely.** Summarize the behavior changed, files touched, validation performed, and any remaining failure or assumption. Link workspace files when referencing them.

## Decision Rules

- **Behavior unclear:** inspect the nearest call site or test first; ask a focused question only when repository evidence cannot establish the contract.
- **No nearby test:** create the smallest regression check that captures the requested behavior, unless the project has no test runner or the change is documentation-only.
- **Dirty worktree:** preserve existing changes. Work around unrelated edits; if edits in the target slice conflict, understand them and integrate rather than revert.
- **Tests unavailable:** use the narrowest available syntax, import, type, lint, runtime, or notebook check and state the limitation.
- **Multiple plausible implementations:** choose the one with the clearest falsifiable check and smallest blast radius.

## Completion Checklist

- [ ] The controlling code path and expected contract are identified.
- [ ] One falsifiable hypothesis and discriminating check were used.
- [ ] The edit is limited to the requested behavior.
- [ ] A focused executable validation passed, or its absence is documented.
- [ ] New diagnostics and relevant test failures were addressed or reported.
- [ ] Unrelated user changes were preserved.
