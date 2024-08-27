from typing import Callable as _Callable

import referencing as _referencing
from referencing import jsonschema as _ref_jsonschema
import jsonschemata as _jsonschemata
import pkgdata as _pkgdata
import pyserials as _ps


def load(
    dynamic: bool = False,
    crawl: bool = True,
    add_resources: list[dict | _referencing.Resource | tuple[str, dict | _referencing.Resource]] | None = None,
    add_resources_default_spec: _referencing.Specification = _ref_jsonschema.DRAFT202012,
    retrieval_func: _Callable[[str], str | _referencing.Resource] = None,
):
    schemata = {}
    resources = add_resources or []
    schema_dir_path = _pkgdata.get_package_path_from_caller(top_level=True) / "_data" / "schema"
    for schema_filepath in schema_dir_path.glob("**/*.yaml"):
        schema_dict = _ps.read.yaml_from_file(path=schema_filepath)
        _jsonschemata.edit.required_last(schema_dict)
        resources.append(schema_dict)
        schema_path = schema_dict["$id"].removeprefix("https://docsman.repodynamics.com/schema/")
        schemata[schema_path] = schema_dict
    registry = _jsonschemata.registry.make(
        dynamic=dynamic,
        crawl=crawl,
        add_resources=resources,
        add_resources_default_spec=add_resources_default_spec,
        retrieval_func=retrieval_func,
    )
    return registry, schemata


def validate(data: dict, schema_path: str):
    _ps.validate.jsonschema(
        data=data,
        schema=_SCHEMATA[schema_path],
        registry=_REGISTRY,
        fill_defaults=True,
    )
    return


_REGISTRY, _SCHEMATA = load()
