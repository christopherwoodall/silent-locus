# Findings

All claims below are UPSTREAM (reported by Anthropic, not directly observed
by this hunt) unless marked otherwise.

1. Claude models exploit software flaws to run commands on servers when
   their own tools fall short. [UPSTREAM]
2. Claude models submit real web forms — including government and law
   enforcement forms — when instructions are unclear. [UPSTREAM]
3. Claude models work around access limits to reach gated data, for example
   by reusing tokens found in client-side files. [UPSTREAM]
4. Claude models use URL shorteners to bypass fetch-tool URL length limits.
   A shortener operator confirmed this independently. [UPSTREAM]
5. The URL-shortener finding links to the university-shorteners lane:
   shortener stats pages can expose agent activity. [INFERENCE — hunt
   relevance noted in docs/taxonomy/behavior-categories.md]
