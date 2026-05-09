# UI Code Review Rubric

Review UI work against the contract before final delivery.

## Pass Criteria

- The implementation uses existing project styling primitives where possible.
- Color, radius, spacing, shadow, and typography match the contract.
- Layout density matches the product context.
- Components share a consistent shape language.
- Empty, loading, error, hover, focus, and disabled states are not forgotten for touched UI.
- Responsive behavior remains usable.
- Accessibility contrast and focus visibility are preserved.
- The implementation avoids every explicit forbidden pattern in the contract.

## Common Failures

- Adding gradients, large rounded cards, or heavy shadows to a restrained preset.
- Building a marketing-style hero inside an operational app.
- Creating nested cards that make hierarchy muddy.
- Using text labels where a standard icon control is expected.
- Creating one-off colors instead of tokens.
- Letting the image draft override product usability.
- Increasing whitespace until dense workflows become slow.

## Final Response Signal

Mention the contract path, changed UI files, verification performed, and any remaining subjective visual risk.
