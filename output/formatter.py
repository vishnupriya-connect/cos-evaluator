def format_output(data, indent=0):
    lines = []
    space = "  " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            lines.append(f"{space}{key}")
            lines.extend(format_output(value, indent + 1))
    elif isinstance(data, list):
        for item in data:
            lines.append(f"{space}-")
            lines.extend(format_output(item, indent + 1))
    else:
        lines.append(f"{space}{data}")

    return lines