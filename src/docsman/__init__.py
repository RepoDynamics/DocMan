from typing import Literal

from docsman.doc import DocumentGenerator


def generate(
    content: list[dict | str],
    default_domain: Literal["html", "md", "agg"] = "agg",
    themed: bool = True,
):
    generator = DocumentGenerator(default_domain=default_domain, themed=themed)
    return generator.generate(elements=content)
