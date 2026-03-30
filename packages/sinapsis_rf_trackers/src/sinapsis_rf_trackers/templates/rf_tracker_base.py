# -*- coding: utf-8 -*-

from abc import abstractmethod
from enum import Enum
from typing import Any

import numpy as np
import supervision as sv
from sinapsis_core.data_containers.annotations import BoundingBox, ImageAnnotations, Segmentation
from sinapsis_core.data_containers.data_packet import DataContainer, ImagePacket
from sinapsis_core.template_base import Template
from sinapsis_core.template_base.base_models import (
    OutputTypes,
    TemplateAttributes,
    TemplateAttributeType,
    UIPropertiesMetadata,
)
from sinapsis_data_visualization.helpers.detection_utils import bbox_xywh_to_xyxy, bbox_xyxy_to_xywh

from sinapsis_rf_trackers.helpers.tags import Tags


class DetectionKWArgs(Enum):
    """Key word arguments for constructing Detections object"""

    xyxy = "xyxy"
    confidence = "confidence"
    class_id = "class_id"
    class_names = "class_names"
    mask = "mask"
    data = "data"


class RFTrackerBaseAttrs(TemplateAttributes):
    """Base attributes for RF trackers (SORT/DeepSORT).

    Args:
        track_activation_threshold (float): Detection confidence threshold for track activation.
            Increasing track_activation_threshold improves accuracy and stability but might miss
            true detections. Decreasing it increases completeness but risks introducing noise
            and instability. Defaults to 0.25.
        lost_track_buffer (int): Number of frames to buffer when a track is lost.
            Increasing lost_track_buffer enhances occlusion handling, significantly reducing
            the likelihood of track fragmentation or disappearance caused by brief detection gaps.
            Defaults to 30.
        frame_rate (float): The frame rate of the video sequence being processed.
            This affects the temporal dynamics of the tracking algorithm. Defaults to 30.0.
        minimum_consecutive_frames (int): Number of consecutive frames that an object must
            be tracked before it is considered a 'valid' track. Increasing minimum_consecutive_frames
            prevents the creation of accidental tracks from false detection or double detection,
            but risks missing shorter tracks. Defaults to 3.
        minimum_iou_threshold (float): Minimum IoU threshold for associating detections with tracks.
            Higher values require better spatial overlap for association, improving precision but
            potentially reducing recall. Defaults to 0.3.
    """

    track_activation_threshold: float = 0.25
    lost_track_buffer: int = 30
    frame_rate: float = 30.0
    minimum_consecutive_frames: int = 3
    minimum_iou_threshold: float = 0.3


class RFTrackerBase(Template):
    """
    Base class for Roboflow trackers (SORT/DeepSORT), provides common functionality for tracking algorithms including
    annotation processing, detection conversion, and template execution patterns.
    """

    AttributesBaseModel = RFTrackerBaseAttrs
    UIProperties = UIPropertiesMetadata(
        category="RFTrackers",
        output_type=OutputTypes.IMAGE,
        tags=[Tags.TRACKERS, Tags.IMAGE, Tags.INFERENCE, Tags.MODELS, Tags.OBJECT_TRACKING],
    )

    def __init__(self, attributes: TemplateAttributeType) -> None:
        super().__init__(attributes)
        self.tracker = self.init_tracker()

    @abstractmethod
    def init_tracker(self) -> Any:
        """Initialize the specific tracker implementation.

        This method must be implemented by subclasses to create and configure
        the actual tracking algorithm instance.

        Returns:
            The initialized tracker object.
        """

    def _extract_annotations(self, image_packet: ImagePacket) -> dict[str, list[Any]]:
        """
        Processes image annotations and converts them into the format required
        by supervision.Detections for tracking operations.

        Args:
            image_packet: The image packet containing annotations to process.

        Returns:
            A dictionary containing lists of detection data with keys:
                - 'xyxy': Bounding box coordinates in [x1, y1, x2, y2] format
                - 'confidence': Confidence scores for each detection
                - 'class_id': Class IDs for each detection
                - 'mask': Segmentation masks (if available)
                - 'class_names': Class names for each detection
        """
        xyxy = []
        confidence = []
        class_id = []
        mask = []
        class_names = []

        for ann in image_packet.annotations:
            if isinstance(ann.bbox, BoundingBox):
                xyxy.append(bbox_xywh_to_xyxy(ann.bbox))
                confidence.append(ann.confidence_score)
                class_id.append(ann.label)
                class_names.append(ann.label_str)
                if isinstance(ann.segmentation, Segmentation):
                    mask.append(ann.segmentation.mask)

        return {
            DetectionKWArgs.xyxy.value: xyxy,
            DetectionKWArgs.confidence.value: confidence,
            DetectionKWArgs.class_id.value: class_id,
            DetectionKWArgs.mask.value: mask,
            DetectionKWArgs.class_names.value: class_names,
        }

    def _annotations_to_detections(self, annotations_dict: dict[str, list[Any]]) -> sv.Detections:
        """
        Takes the extracted annotation data and creates a supervision.Detections
        object that can be used by tracking algorithms.

        Args:
            annotations_dict: Dictionary containing detection data extracted from annotations.

        Returns:
            A supervision.Detections object containing all detection information.
        """
        detection_args: dict[str, np.ndarray] = {}
        for key, value in annotations_dict.items():
            if value:
                detection_args[key] = np.array(value)

        if DetectionKWArgs.class_names.value in detection_args:
            class_names = detection_args.pop(DetectionKWArgs.class_names.value)
            detection_args[DetectionKWArgs.data.value] = {DetectionKWArgs.class_names.value: class_names}

        return sv.Detections(**detection_args)

    def _detections_to_annotations(self, detections: sv.Detections) -> list[ImageAnnotations]:
        """
        Transforms tracked detections back into the annotation format used
        throughout the Sinapsis framework, including tracker IDs.

        Args:
            detections: The supervision.Detections object containing tracking results.

        Returns:
            A list of ImageAnnotations with bounding boxes, labels, and tracker IDs.
        """
        annotations: list[ImageAnnotations] = []
        class_names = detections.data.get(DetectionKWArgs.class_names.value, [None] * len(detections))

        for idx, (bbox, confidence, class_id, tracker_id) in enumerate(
            zip(detections.xyxy, detections.confidence, detections.class_id, detections.tracker_id)
        ):
            x, y, w, h = bbox_xyxy_to_xywh(bbox)
            ann = ImageAnnotations(
                label=class_id,
                label_str=class_names[idx],
                confidence_score=float(confidence),
                bbox=BoundingBox(x, y, w, h),
                extra_labels={"ID": int(tracker_id)},
            )
            annotations.append(ann)

        return annotations

    def execute(self, container: DataContainer) -> DataContainer:
        """
        Processes each image packet in the container, applying the tracking algorithm
        to update object identities across frames.

        Args:
            container: The data container with image packets to process.

        Returns:
            The updated container with tracking annotations added to each image.
        """
        for image_packet in container.images:
            if not image_packet.annotations:
                continue

            annotations_dict = self._extract_annotations(image_packet)
            detections = self._annotations_to_detections(annotations_dict)
            tracked_detections = self.update_with_frame(detections, image_packet.content)
            new_annotations = self._detections_to_annotations(tracked_detections)
            image_packet.annotations = new_annotations

        return container

    @abstractmethod
    def update_with_frame(self, detections: sv.Detections, frame: np.ndarray | None = None) -> sv.Detections:
        """
        This method must be implemented by subclasses to perform the actual
        tracking update using their specific algorithm.

        Args:
            detections: Current frame detections to be tracked.
            frame: The image frame data (required for appearance-based trackers).

        Returns:
            Updated detections with tracker IDs assigned.
        """
