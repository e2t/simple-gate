import locale

locale.setlocale(locale.LC_ALL, "")


def fstr(value: float, maxf=6, minf=0, grouping=True):
    fcount = minf
    if maxf > minf:
        frac = value % 1
        rounded_frac = round(frac, maxf)
        if (n := len(f"{rounded_frac}") - 2) > minf:
            fcount = n
    return locale.format_string(f"%.{fcount}f", value, grouping=grouping)


def heading(text: str) -> str:
    indent = "======"
    return f"{indent} {text} {indent}"
