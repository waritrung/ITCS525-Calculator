import re

_percent_pair = re.compile(r"""
    (?P<a>\d+(?:\.\d+)?)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)(?P<p>%+)
""", re.VERBOSE)
_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)(?P<p>%+)")


def expand_percent(expr: str) -> str:
    """Expand percent expressions including multiple % signs."""
    s = expr

    # Expand A op B%% patterns
    while True:
        m = _percent_pair.search(s)
        if not m:
            break
        a, op, b, perc = m.group("a", "op", "b", "p")
        count = len(perc)
        
        # Build nested (b / 100) / 100 ... count times
        b_expr = b
        for _ in range(count):
            b_expr = f"({b_expr}/100)"

        if op in "+-":
            repl = f"{a} {op} ({b_expr}*{a})"
        elif op == "*":
            repl = f"{a} * {b_expr}"
        else:
            repl = f"{a} / {b_expr}"

        s = s[:m.start()] + repl + s[m.end():]

    # Expand standalone N%%%%
    def percent_replacer(m):
        n = m.group("n")
        perc = m.group("p")
        count = len(perc)
        expr = n
        for _ in range(count):
            expr = f"({expr}/100)"
        return expr

    s = _number_percent.sub(percent_replacer, s)
    return s
