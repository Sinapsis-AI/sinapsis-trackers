# -*- coding: utf-8 -*-
import importlib
from typing import Callable

_root_lib_path = "sinapsis_rf_trackers.templates"

_template_lookup = {
    "DeepSORTTrackerInference": f"{_root_lib_path}.deepsort_tracker_inference",
    "SORTTrackerInference": f"{_root_lib_path}.sort_tracker_inference",
}


def __getattr__(name: str) -> Callable:
    if name in _template_lookup:
        module = importlib.import_module(_template_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"template `{name}` not found in {_root_lib_path}")


__all__ = list(_template_lookup.keys())
