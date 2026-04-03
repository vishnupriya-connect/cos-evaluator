def format_output(result):
    def render(obj, indent=0):
        lines = []
        space = "  " * indent

        if isinstance(obj, dict):
            for key, value in obj.items():
                lines.append(f"{space}{key}")
                lines.extend(render(value, indent + 1))

        elif isinstance(obj, list):
            for item in obj:
                lines.append(f"{space}-")
                lines.extend(render(item, indent + 1))

        else:
            lines.append(f"{space}{obj}")

        return lines

    return "\n".join(render(result))