def tag(text: str, ref: str) -> str:
    return f"({ref})=\n{text}"

def comma_list(items: list[str], item_as_code: bool = False, as_html: bool = False) -> str:
    if item_as_code:
        items = [inline_code(item, as_html=as_html) for item in items]
    return ", ".join(items)


def normal_list(items: list[str], item_as_code: bool = False, indent_level: int = 0, indent_size: int = 4) -> str:
    new_items = []
    for item in items:
        if item_as_code:
            item = inline_code(item)
        new_items.append(indent_level * indent_size * " " + f"- {item}")
    return "\n".join(new_items)


def inline_code(text: str, as_html: bool = False) -> str:
    if as_html:
        return f"<code>{text}</code>"
    return f"`{text}`"
