import pkgdata as _pkgdata


_data_dir_path = _pkgdata.get_package_path_from_caller(top_level=True) / "_data"


def code_of_conduct(name: str) -> str:
    """Get the text of a code of conduct."""
    filepath = _data_dir_path / "code_of_conduct" / f"{name}.txt"
    return filepath.read_text()
