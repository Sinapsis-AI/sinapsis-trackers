# -*- coding: utf-8 -*-
import importlib
from typing import Callable

_root_lib_path = "sinapsis_cotracker.templates"

_template_lookup = {
    "CoTrackerOffline": f"{_root_lib_path}.co_tracker_offline",
    "CoTrackerOnline": f"{_root_lib_path}.co_tracker_online",
    "CoTrackerVisualizer": f"{_root_lib_path}.co_tracker_visualizer",
}


def __getattr__(name: str) -> Callable:
    if name in _template_lookup:
        module = importlib.import_module(_template_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"template `{name}` not found in {_root_lib_path}")


__all__ = list(_template_lookup.keys())
