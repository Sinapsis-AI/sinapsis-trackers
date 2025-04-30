# -*- coding: utf-8 -*-

from enum import Enum
from typing import Any

import numpy as np
import supervision as sv
from sinapsis_core.data_containers.annotations import BoundingBox, ImageAnnotations, Segmentation
from sinapsis_core.data_containers.data_packet import DataContainer, ImagePacket
from sinapsis_core.template_base import Template
from sinapsis_core.template_base.base_models import TemplateAttributes, TemplateAttributeType, UIPropertiesMetadata, OutputTypes
from sinapsis_data_visualization.helpers.detection_utils import bbox_xywh_to_xyxy, bbox_xyxy_to_xywh
from supervision import Detections


class ByteTrackAttrs(TemplateAttributes):
    """Attributes for the ByteTrack template

    Args:
        track_activation_threshold (float): Detection confidence threshold
            for track activation. Increasing track_activation_threshold improves accuracy
            and stability but might miss true detections. Decreasing it increases
            completeness but risks introducing noise and instability.
        lost_track_buffer (int): Number of frames to buffer when a track is lost.
            Increasing lost_track_buffer enhances occlusion handling, significantly
            reducing the likelihood of track fragmentation or disappearance caused
            by brief detection gaps.
        minimum_matching_threshold (float): Threshold for matching tracks with detections.
            Increasing minimum_matching_threshold improves accuracy but risks fragmentation.
            Decreasing it improves completeness but risks false positives and drift.
        frame_rate (int): The frame rate of the video.
        minimum_consecutive_frames (int): Number of consecutive frames that an object must
            be tracked before it is considered a 'valid' track.
            Increasing minimum_consecutive_frames prevents the creation of accidental tracks from
            false detection or double detection, but risks missing shorter tracks.
    """

    track_activation_threshold: float = 0.20
    lost_track_buffer: int = 30
    minimum_matching_threshold: float = 0.7
    frame_rate: float | int = 30
    minimum_consecutive_frames: int = 1


class DetectionKWArgs(Enum):
    """Key word arguments for constructing Detections object"""

    xyxy: str = "xyxy"
    confidence: str = "confidence"
    class_id: str = "class_id"
    class_names: str = "class_names"
    mask: str = "mask"


class ByteTrack(Template):
    """A template class for implementing the ByteTrack tracking algorithm.

    This class provides functionality to track objects across frames using the ByteTrack algorithm.
    It handles the conversion of annotations to detections, updates tracks, and converts detections
    back to annotations.

    Usage example:

    agent:
        name: my_test_agent
    templates:
    -   template_name: InputTemplate
        class_name: InputTemplate
        attributes: {}
    -   template_name: ByteTrack
        class_name: ByteTrack
        template_input: InputTemplate
        attributes:
            track_activation_threshold: 0.2
            lost_track_buffer: 30
            minimum_matching_threshold: 0.5
            frame_rate: 30
            minimum_consecutive_frames: 1

    """

    AttributesBaseModel = ByteTrackAttrs
    UIProperties = UIPropertiesMetadata(category="ByteTrack", output_type=OutputTypes.IMAGE)

    def __init__(self, attributes: TemplateAttributeType) -> None:
        super().__init__(attributes)
        self.tracker = sv.ByteTrack(
            track_activation_threshold=self.attributes.track_activation_threshold,
            lost_track_buffer=self.attributes.lost_track_buffer,
            minimum_matching_threshold=self.attributes.minimum_matching_threshold,
            frame_rate=self.attributes.frame_rate,
            minimum_consecutive_frames=self.attributes.minimum_consecutive_frames,
        )

    def _extract_annotations(self, image_packet: ImagePacket) -> dict[str, list[Any]]:
        """Extract detection data from image annotations.

        Args:
            image_packet (ImagePacket): The image packet containing annotations to process.

        Returns:
            dict[str, list[Any]]: A dictionary containing lists of detection data:
                - 'xyxy': List of bounding box coordinates in [x1, y1, x2, y2] format.
                - 'confidence': List of confidence scores for each detection.
                - 'class_id': List of class IDs for each detection.
                - 'mask': List of segmentation masks (if available).
                - 'class_names': List of class names for each detection.
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

    def _annotations_to_detections(self, annotations_dict: dict[str, list[Any]]) -> Detections:
        """Convert image annotations into a Detections object for tracking.

        Args:
            annotations_dict (dict[str, list[Any]]): The image packet containing annotations to
                process.

        Returns:
            Detections: A Detections object containing:
                - Bounding boxes in [x1, y1, x2, y2] format.
                - Confidence scores for each detection.
                - Class IDs for each detection.
                - Segmentation masks (if available).
                - Class names for each detection.
        """
        new_detections_args: dict[str, np.ndarray | None] = {}
        for key, field in annotations_dict.items():
            if all(x is None for x in field):
                new_detections_args[key] = None
            else:
                new_detections_args[key] = np.array(annotations_dict[key])

        detections = Detections(
            xyxy=new_detections_args[DetectionKWArgs.xyxy.value],
            confidence=new_detections_args[DetectionKWArgs.confidence.value],
            class_id=new_detections_args[DetectionKWArgs.class_id.value],
            mask=new_detections_args[DetectionKWArgs.mask.value],
            data={DetectionKWArgs.class_names.value: new_detections_args[DetectionKWArgs.class_names.value]},
        )
        return detections

    def _detections_to_annotations(self, detections: Detections) -> list[ImageAnnotations]:
        """Convert Detections object back into a list of ImageAnnotations.

        Args:
            detections (Detections): The Detections object to convert.

        Returns:
            list[ImageAnnotations]: A list of ImageAnnotations containing:
                - Bounding boxes in [x, y, width, height] format.
                - Class IDs and names.
                - Tracker IDs (if available).
        """
        annotations = []
        class_names = detections.data.get(DetectionKWArgs.class_names.value, [])
        tracker_ids = detections.tracker_id
        for class_id, xyxy, class_name, tracker_id in zip(
            detections.class_id, detections.xyxy, class_names, tracker_ids
        ):
            x, y, w, h = bbox_xyxy_to_xywh(xyxy)
            ann = ImageAnnotations(
                label=class_id,
                label_str=class_name,
                bbox=BoundingBox(x, y, w, h),
                extra_labels={"ID": int(tracker_id)},
            )
            annotations.append(ann)
        return annotations

    def execute(self, container: DataContainer) -> DataContainer:
        """Process all image packets in the container through the ByteTrack tracker.

        Args:
            container (DataContainer): The container holding image packets with annotations.

        Returns:
            DataContainer: The updated container with new annotations from the tracker.
        """
        for image_packet in container.images:
            annotations_dict = self._extract_annotations(image_packet)
            detections = self._annotations_to_detections(annotations_dict)
            new_detections = self.tracker.update_with_detections(detections)
            new_annotations = self._detections_to_annotations(new_detections)
            image_packet.annotations = new_annotations
        return container
