# -*- coding: utf-8 -*-

import numpy as np
import supervision as sv
from trackers import SORTTracker

from sinapsis_rf_trackers.templates.rf_tracker_base import RFTrackerBase


class SORTTrackerInference(RFTrackerBase):
    """
    This template provides the logic to use the SORT tracker from
    Roboflow's trackers library. It processes detection annotations from upstream templates
    and adds tracking IDs to maintain object identity across video frames.

    Usage example:

        agent:
          name: sort_tracker_agent
        templates:
        - template_name: InputTemplate
          class_name: InputTemplate
          attributes: {}
        - template_name: SORTTrackerInference
          class_name: SORTTrackerInference
          template_input: InputTemplate
          attributes:
            track_activation_threshold: 0.25
            lost_track_buffer: 30
            minimum_consecutive_frames: 3
            minimum_iou_threshold: 0.3
            frame_rate: 30

    """

    def init_tracker(self) -> SORTTracker:
        """
        Creates and configures a SORT tracker instance using the attributes
        specified in the template configuration.

        Returns:
            Configured SORTTracker instance ready for tracking operations.
        """
        return SORTTracker(
            lost_track_buffer=self.attributes.lost_track_buffer,
            frame_rate=self.attributes.frame_rate,
            track_activation_threshold=self.attributes.track_activation_threshold,
            minimum_consecutive_frames=self.attributes.minimum_consecutive_frames,
            minimum_iou_threshold=self.attributes.minimum_iou_threshold,
        )

    def update_with_frame(self, detections: sv.Detections, frame: np.ndarray | None = None) -> sv.Detections:
        """
        Performs tracking update using only detection information (bounding boxes,
        confidence scores). The frame parameter is ignored as SORT doesn't use
        appearance features.

        Args:
            detections: Current frame detections with bounding boxes and scores.
            frame: Image frame data (unused by SORT, kept for interface consistency).

        Returns:
            Updated detections with tracker IDs assigned by the SORT algorithm.
        """
        _ = frame
        return self.tracker.update(detections)
