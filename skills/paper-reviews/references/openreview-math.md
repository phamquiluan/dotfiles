# OpenReview Math Formatting

OpenReview uses MathJax to render TeX. Only **math-mode** macros are supported — no text-mode commands (`\emph`, `\textbf`, `\begin{enumerate}`, etc.). Use Markdown for all text formatting.

## Delimiters

| Type | Syntax | Example |
|------|--------|---------|
| Inline | `$...$` | `$\alpha = 0.05$` |
| Display | `$$...$$` | `$$\sum_{i=1}^{n} x_i$$` |

## Escaping Rules

### Markdown-enabled fields (reviews, comments)

All backslashes must be **double-escaped** (`\\`) because Markdown strips single backslashes before MathJax processes them.

| Intent | Write this | NOT this |
|--------|-----------|----------|
| `\alpha` | `\\alpha` | `\alpha` |
| `\frac{a}{b}` | `\\frac{a}{b}` | `\frac{a}{b}` |
| `\sum_{i=1}^{n}` | `\\sum_{i=1}^{n}` | `\sum_{i=1}^{n}` |
| Thin space `\,` | `\\,` | `\,` |
| Newline in align | `\\\\` | `\\` |
| Underscore at word boundary | `\\_` | `_` (may break) |

### HTML characters inside math

Add spaces around `<` and `>` to prevent HTML tag interpretation:

- Write `$a < b$` as `$a < b$` (with spaces) — or use `$a \lt b$`
- Write `$x > 0$` as `$x > 0$` (with spaces) — or use `$x \gt 0$`

No HTML tags inside math delimiters.

## Supported Constructs

Common math-mode commands that work:

```
Greek:        $\\alpha, \\beta, \\gamma, \\theta, \\lambda, \\mu, \\sigma$
Fractions:    $\\frac{a}{b}$
Subscripts:   $x_{i}$, $x_{i,j}$
Superscripts: $x^{2}$, $e^{-\\lambda t}$
Sums:         $\\sum_{i=1}^{n} x_i$
Products:     $\\prod_{j=1}^{m} p_j$
Integrals:    $\\int_{0}^{\\infty} f(x) \\, dx$
Limits:       $\\lim_{n \\to \\infty}$
Norms:        $\\| x \\|$, $\\lVert x \\rVert$
Sets:         $\\{1, 2, 3\\}$, $\\mathbb{R}^n$
Operators:    $\\log$, $\\exp$, $\\min$, $\\max$, $\\arg\\min$
Matrices:     \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}
Align:        \\begin{aligned} ... \\end{aligned}  (inside $$ delimiters)
```

## Array Environment Limitations

Only `l`, `r`, `c`, `|`, and `:` (dashed lines) are recognized in array preambles. Everything else is ignored.

## Unsupported Features

- Text-mode macros (`\emph`, `\textbf`, `\textit`)
- `\begin{enumerate}`, `\begin{itemize}` — use Markdown lists
- Custom macro definitions (`\newcommand`) — not reliable
- Complex array preamble options beyond `l`, `r`, `c`, `|`, `:`

If a macro is unsupported, it renders as **red text**.

## Examples in Review Context

### Inline math in a weakness

```
The loss function $\\mathcal{L} = \\sum_{i} \\ell(f(x_i), y_i)$ (Line 142) lacks
a regularization term. Adding $\\lambda \\|\\theta\\|_2^2$ would help prevent
overfitting on the small dataset described in Section 4.
```

### Display math in a question

```
The paper defines the metric as (Lines 89-91):

$$\\text{Score} = \\frac{1}{N} \\sum_{i=1}^{N} \\mathbb{1}[y_i = \\hat{y}_i]$$

But this ignores class imbalance. Would a weighted variant such as
$\\sum_c w_c \\cdot \\text{Acc}_c$ change the conclusions in Table 3?
```
