# -*- coding: utf-8 -*-
from enum import Enum


class Tags(str, Enum):
    TRACKERS = "trackers"
    IMAGE = "image"
    INFERENCE = "inference"
    OBJECT_TRACKING = "object_tracking"
    MODELS = "models"
