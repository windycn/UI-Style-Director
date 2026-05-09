# Contract-First UI Workflow

UI Style Director works best when style decisions become persistent project assets.

## Artifact Order

1. `.ui-style/ui-style-contract.json`
2. `.ui-style/UI_STYLE_GUIDE.md`
3. `.ui-style/implementation-notes.md`
4. `.ui-style/image-prompts/*.md`
5. `.ui-style/drafts/*`
6. `.ui-style/review-checklist.md`

## Style Resolution

Use this precedence order:

1. Explicit instruction in the current user request.
2. Page or component override.
3. Existing project contract.
4. Named preset.
5. Inferred custom style.

## Implementation Rule

Do not restyle a UI from general taste alone. Convert the target style into concrete tokens, layout rules, component rules, and forbidden patterns, then implement those rules in the codebase's existing styling system.

## Review Rule

Every UI implementation should be checked against:

- Token alignment.
- Layout density.
- Typography scale.
- Component shape and hierarchy.
- State coverage.
- Accessibility.
- Contract `avoid` list.
