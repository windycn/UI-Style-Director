# UI Style Contract Schema

The contract is intentionally plain JSON so Codex, scripts, and humans can all read it.

```json
{
  "schemaVersion": "0.1.0",
  "styleId": "flat-white",
  "styleName": "Flat White",
  "intent": "Clear, calm, high-efficiency SaaS interface.",
  "productContext": {
    "productType": "SaaS",
    "audience": "Operators and knowledge workers",
    "primaryJobs": [],
    "contentDensity": "medium-high"
  },
  "visualPosture": {
    "density": "medium-high",
    "tone": "calm, precise, utilitarian",
    "ornamentation": "low",
    "brandExpression": "restrained"
  },
  "tokens": {
    "color": {
      "background": "#F8FAFC",
      "surface": "#FFFFFF",
      "surfaceMuted": "#F1F5F9",
      "text": "#101828",
      "muted": "#667085",
      "accent": "#2563EB",
      "border": "#E5E7EB",
      "danger": "#DC2626",
      "success": "#16A34A"
    },
    "typography": {
      "fontFamily": "system-ui",
      "bodySize": "14px",
      "headingWeight": "650",
      "lineHeight": "1.45"
    },
    "spacing": {
      "grid": "4px",
      "controlGap": "8px",
      "panelPadding": "16px",
      "sectionGap": "24px"
    },
    "radius": {
      "control": "6px",
      "panel": "8px",
      "modal": "10px"
    },
    "shadow": {
      "panel": "none",
      "popover": "0 12px 32px rgba(15, 23, 42, 0.12)"
    },
    "border": {
      "default": "1px solid #E5E7EB",
      "strong": "1px solid #CBD5E1"
    }
  },
  "layoutRules": [],
  "componentRules": {
    "buttons": [],
    "forms": [],
    "tables": [],
    "cards": [],
    "navigation": [],
    "modals": [],
    "charts": [],
    "states": []
  },
  "interactionRules": [],
  "accessibilityRules": [],
  "avoid": [],
  "codeMapping": {
    "cssVariables": {},
    "tailwind": {},
    "componentPatterns": [],
    "filesToInspect": []
  }
}
```

## Notes

- Keep values specific enough to implement.
- Put subjective rationale in the style guide, not only in the JSON.
- `avoid` rules matter as much as positive rules because they prevent drift.
- `codeMapping` should be updated after reading the actual project.
