# -*- coding: utf-8 -*-

from typing import Any, Literal

import numpy as np
import supervision as sv
from pydantic import BaseModel, ConfigDict, Field
from sinapsis_core.utils.env_var_keys import SINAPSIS_CACHE_DIR
from trackers import DeepSORTTracker, ReIDModel

from sinapsis_rf_trackers.templates.rf_tracker_base import RFTrackerBase, RFTrackerBaseAttrs


class ReIDKwargs(BaseModel):
    """Defines the keyword arguments for initializing a Re-Identification model."""

    pretrained_cfg: dict[str, Any] | None = None
    pretrained_cfg_overlay: dict[str, Any] | None = None
    checkpoint_path: str | None = None
    cache_dir: str = SINAPSIS_CACHE_DIR
    scriptable: bool | None = None
    exportable: bool | None = None
    no_jit: bool | None = None
    model_config = ConfigDict(extra="allow")


class DeepSORTTrackerAttrs(RFTrackerBaseAttrs):
    """Attributes for the DeepSORT tracker template.

    Args:
        appearance_threshold (float): Threshold for appearance-based matching.
            Higher values make the tracker more conservative in appearance matching,
            reducing identity switches but potentially losing tracks during occlusions.
            Defaults to 0.7.
        appearance_weight (float): Weight of appearance features versus motion features
            in the association cost. Higher values prioritize appearance matching,
            lower values prioritize motion consistency. Defaults to 0.5.
        distance_metric (str): Distance metric for appearance feature comparison.
            Supported metrics include 'cosine' and 'euclidean'. Cosine distance
            is generally more robust for appearance features. Defaults to "cosine".
        reid_model_name (str): Name of the feature extraction model from timm or a path
            to a checkpoint. Defaults to "tf_efficientnet_b1.in1k".
        reid_device (Literal["auto", "cuda", "cpu"]): Device to run the Re-ID model on.
            'auto' selects CUDA if available. Defaults to "auto".
        reid_get_pooled_features (bool): Whether to use pooled features from the Re-ID model.
            Defaults to True.
        reid_kwargs (ReIDKwargs): Additional keyword arguments to pass to the Re-ID model
            constructor.
    """

    appearance_threshold: float = 0.7
    appearance_weight: float = 0.5
    distance_metric: str = "cosine"
    reid_model_name: str = "tf_efficientnet_b1.in1k"
    reid_device: Literal["auto", "cuda", "cpu"] = "auto"
    reid_get_pooled_features: bool = True
    reid_kwargs: ReIDKwargs = Field(default_factory=ReIDKwargs)


class DeepSORTTrackerInference(RFTrackerBase):
    """
    This template provides the logic to use the DeepSORT tracker from
    Roboflow's trackers library. It enhances the basic SORT tracking by incorporating
    appearance features, making it more robust for challenging tracking scenarios
    with occlusions and crowded scenes.

    Key Features:
        - Appearance-based re-identification using deep features
        - Reduced identity switches compared to motion-only trackers
        - Configurable appearance and motion feature weighting
        - Support for various CNN backbones via timm library

    Usage example:

        agent:
          name: deepsort_tracker_agent
        templates:
        - template_name: InputTemplate
          class_name: InputTemplate
          attributes: {}
        - template_name: DeepSORTTrackerInference
          class_name: DeepSORTTrackerInference
          template_input: InputTemplate
          attributes:
            track_activation_threshold: 0.25
            lost_track_buffer: 30
            minimum_consecutive_frames: 3
            minimum_iou_threshold: 0.3
            frame_rate: 30
            appearance_threshold: 0.7
            appearance_weight: 0.5
            distance_metric: "cosine"
            reid_model_name: "tf_efficientnet_b1.in1k"
            reid_device: "auto"
    """

    AttributesBaseModel = DeepSORTTrackerAttrs

    def _init_reid_model(self) -> ReIDModel:
        """Initialize the Re-Identification model for appearance-based tracking.

        Creates and configures a feature extractor to generate appearance
        embeddings for tracked objects.

        Returns:
            Configured ReIDModel instance ready for feature extraction.
        """
        return ReIDModel.from_timm(
            model_name_or_checkpoint_path=self.attributes.reid_model_name,
            device=self.attributes.reid_device,
            get_pooled_features=self.attributes.reid_get_pooled_features,
            **self.attributes.reid_kwargs.model_dump(exclude_none=True),
        )

    def init_tracker(self) -> DeepSORTTracker:
        """Initialize the DeepSORT tracker with configured parameters.

        Creates and configures a DeepSORT tracker instance using both motion
        and appearance parameters specified in the template configuration.

        Returns:
            Configured DeepSORTTracker instance ready for tracking operations.
        """
        return DeepSORTTracker(
            reid_model=self._init_reid_model(),
            lost_track_buffer=self.attributes.lost_track_buffer,
            frame_rate=self.attributes.frame_rate,
            track_activation_threshold=self.attributes.track_activation_threshold,
            minimum_consecutive_frames=self.attributes.minimum_consecutive_frames,
            minimum_iou_threshold=self.attributes.minimum_iou_threshold,
            appearance_threshold=self.attributes.appearance_threshold,
            appearance_weight=self.attributes.appearance_weight,
            distance_metric=self.attributes.distance_metric,
        )

    def update_with_frame(self, detections: sv.Detections, frame: np.ndarray | None = None) -> sv.Detections:
        """
        Performs tracking update using both detection information and image frame
        for appearance feature extraction. The frame is required for DeepSORT to
        generate appearance embeddings for re-identification.

        Args:
            detections: Current frame detections with bounding boxes and scores.
            frame: Image frame data required for appearance feature extraction.

        Returns:
            Updated detections with tracker IDs assigned by the DeepSORT algorithm.

        Note:
            If no frame is provided, a warning is logged and original detections
            are returned without tracking updates.
        """
        if frame is None:
            self.logger.warning("DeepSORT requires a frame for feature extraction.")
            return detections
        return self.tracker.update(detections, frame)
