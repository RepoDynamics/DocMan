import copy
from typing import Literal, get_type_hints as _get_type_hints
from types import FunctionType as _FunctionType
from pathlib import Path as _Path

import pybadger as bdg
from markitup import html as _html, md as _md, dtype as _dtype, doc as _doc
import pyserials as _ps

from docsman import element as _elem


class DocumentGenerator:

    def __init__(
        self,
        default_domain: Literal["html", "md", "agg"] = "agg",
        themed: bool = True,
    ):
        self.domain = default_domain
        self.themed = themed
        self.generator = {
            "html": self.generate_html_element,
            "md": self.generate_md_element,
            "agg": self.generate_agg_element,
        }
        return

    def generate(self, elements: list[dict | str]) -> _doc.Document:
        content = []
        for element in elements:
            if isinstance(element, str):
                content.append(element)
            else:
                content.append(self.generate_element(element))
        return _doc.from_contents(content=content)

    def generate_element(self, element: dict):
        elem_class = element.pop("class")
        elem_class_parts = elem_class.split(".")
        if len(elem_class_parts) == 1:
            domain = self.domain
            elem_id = elem_class_parts[0]
        else:
            domain, elem_id = elem_class_parts
        return self.generator[domain](elem_id, element)

    def generate_agg_element(self, elem_id: str, element: dict):
        align_span, align_div, attrs_span, attrs_div = (
            element.pop(key, None) for key in ("align_span", "align_div", "attrs_span", "attrs_div")
        )
        generator = self._get_elem_generator(_elem, elem_id, "Aggregate")
        element = generator(themed=self.themed, **element)
        if align_span or attrs_span:
            attrs_span = (attrs_span or {}) | {"align": align_span}
            element = _html.elem.span(element, attrs_span)
        if align_div or attrs_div:
            attrs_div = (attrs_div or {}) | {"align": align_div}
            element = _html.elem.div(element, attrs_div)
        return element

    def generate_html_element(self, elem_id: str, element: dict):
        generator = self._get_elem_generator(_html.elem, elem_id, "HTML")
        generator_params = _get_type_hints(generator)
        generator_params.pop("return", None)
        for param_name, param_type in generator_params.items():
            if param_type in (_dtype.ElementContent, _dtype.ElementContentInput) and param_name in element:
                content = element[param_name]
                if isinstance(content, dict):
                    element[param_name] = self.generate_element(element=content)
                elif isinstance(content, (list, tuple)):
                    element[param_name] = [self.generate_element(element=elem) for elem in content]
        if elem_id in (
            "comment", "h", "picture_color_scheme", "picture_from_sources", "table_from_rows",
        ):
            return generator(**element)
        return generator(*[element.get(param_name) for param_name in generator_params])

    def generate_md_element(self):
        return

    @staticmethod
    def _get_elem_generator(module, elem_id, class_name):
        error_msg = f"Element '{elem_id}' is not a valid {class_name} element."
        try:
            func = getattr(module, elem_id)
        except AttributeError:
            raise AttributeError(error_msg)
        if not isinstance(func, _FunctionType):
            raise AttributeError(error_msg)
        return func
