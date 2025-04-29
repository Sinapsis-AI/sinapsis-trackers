# -*- coding: utf-8 -*-
from typing import Literal

import numpy as np
import torch
from cotracker.utils.visualizer import Visualizer
from sinapsis_core.data_containers.data_packet import DataContainer, ImageColor, ImagePacket
from sinapsis_core.template_base import Template
from sinapsis_core.template_base.base_models import TemplateAttributeType

from sinapsis_cotracker.templates.co_tracker_base import CoTrackerAttributes, CoTrackerBase, InferenceResults


class CoTrackerVisualizer(Template):
    """Facebook Research Co-tracker Visualizer template.

    This class visualizes the results of the Co-tracker model by taking a video input
    as images in the container, converting them to a torch tensor, and using the predictions
    and visibility values for each pixel. It produces new images with the tracked pixels and
    optionally overwriting the original images.

    Usage example:

    agent:
        name: my_test_agent
    templates:
    -   template_name: InputTemplate
        class_name: InputTemplate
        attributes: {}
    -   template_name: CoTrackerVisualizer
        class_name: CoTrackerVisualizer
        template_input: InputTemplate
        attributes:
            device: 'cuda'
            generic_key_field: str
            pad_value: 0
            mode: 'rainbow'
            linewidth: 3
            tracks_leave_trace: -1
            overwrite: true

    """

    class AttributesBaseModel(CoTrackerAttributes):
        """Configuration attributes for the CoTrackerVisualizer.

        Attributes:
            pad_value (int): Padding value used for video processing. Default is 0.
            mode (Literal["cool", "rainbow", "optical_flow"]): Visualization mode.
                Options include "cool", "rainbow", and "optical_flow". Default is "rainbow".
            linewidth (int): Line width of the circles drawn on the tracked points. Default is 2.
            tracks_leave_trace (int): Number of frames to leave a trace for the tracked points.
                Use -1 for an infinite trace. Default is 0.
            overwrite (bool): If True, overwrites the existing images in the container.
                If False, appends the visualized frames to the existing images. Default is False.
        """

        pad_value: int = 0
        mode: Literal["cool", "rainbow", "optical_flow"] = "rainbow"
        linewidth: int = 2
        tracks_leave_trace: int = 0
        overwrite: bool = False
        generic_key_field: str

    def __init__(self, attributes: TemplateAttributeType) -> None:
        super().__init__(attributes)
        self.visualizer = Visualizer(
            pad_value=self.attributes.pad_value,
            mode=self.attributes.mode,
            linewidth=self.attributes.linewidth,
            show_first_frame=0,
        )

    def _visualize_results(self, torch_video: torch.Tensor, tracker_results: InferenceResults) -> np.ndarray:
        """Visualizes the tracking results for a given video.

        Args:
            torch_video (torch.Tensor): The input video as a torch tensor of shape (T, C, H, W),
                where T is the number of frames, C is the number of channels, and H and W are
                the height and width of the frames.
            tracker_results (InferenceResults): The tracking results containing tracks and
                visibility values for each pixel.

        Returns:
            np.ndarray: The visualized video frames as a numpy array of shape (T, H, W, C),
                where C is the number of color channels (e.g., 3 for RGB).
        """
        preds, visibilities = (
            tracker_results.tracks,
            tracker_results.visibilities,
        )
        output = self.visualizer.visualize(torch_video, preds, visibilities, save_video=False)
        output = output.squeeze(0).to(torch.uint8).permute(0, 2, 3, 1).cpu().numpy()

        return output

    def execute(self, container: DataContainer) -> DataContainer:
        """Extracts tracking results from the `generic_data` field of the container,
        visualizes the results using the Co-tracker visualizer, and either appends or overwrites
        the `images` field in the container with the visualized frames.

        Args:
            container (DataContainer): The input data container containing:
                - `images`: A list of ImagePacket objects representing the video frames.
                - `generic_data`: A dictionary containing tracking results under the key
                  specified by `generic_key_field`.

        Returns:
            DataContainer: The updated data container with the visualized frames added to
                the `images` field. If `overwrite` is True, the original frames are replaced
                with the visualized frames. If False, the visualized frames are appended.
        """

        tracker_results = self._get_generic_data(container, self.attributes.generic_key_field)
        if not container.images or not tracker_results:
            return container

        video_array = np.asarray([image.content for image in container.images])
        torch_video = CoTrackerBase.pre_process_video(video_array, self.attributes.device)
        color_space = container.images[0].color_space or ImageColor.RGB

        if self.attributes.overwrite:
            container.images = []

        frames = self._visualize_results(torch_video, tracker_results)
        container.images.extend(
            [ImagePacket(content=frame, source=f"{i}", color_space=color_space) for i, frame in enumerate(frames)]
        )

        return container
