from pathlib import Path
from typing import Any, Dict, Union

import yaml


def get_project_root() -> Path:
    """Return the repository root based on this module location."""
    return Path(__file__).resolve().parent.parent


def resolve_project_path(*relative_parts: Union[str, Path]) -> Path:
    """Resolve a path relative to the repository root."""
    return get_project_root().joinpath(*map(str, relative_parts))


def load_yaml_config(config_path: Union[str, Path, None] = None) -> Dict[str, Any]:
    """Load YAML config from the repository root or an explicit path."""
    if config_path is None:
        config_path = resolve_project_path("config.yaml")
    elif not isinstance(config_path, Path):
        config_path = Path(config_path)

    if not config_path.is_absolute():
        config_path = resolve_project_path(config_path)

    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}
