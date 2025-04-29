# -*- coding: utf-8 -*-
from typing import cast

import numpy as np
import torch
from cotracker.predictor import CoTrackerPredictor
from sinapsis_core.data_containers.data_packet import DataContainer, ImagePacket
from sinapsis_core.template_base.base_models import TemplateAttributeType

from sinapsis_cotracker.templates.co_tracker_base import CoTrackerBase


class CoTrackerOffline(CoTrackerBase):
    """Template to perform offline pixel tracking for videos using Facebook Research's CoTracker model.

    This template is designed for **offline tracking**, meaning it requires the full video (all frames)
    as input before processing. It does not support real-time tracking or streaming input.

    The template transforms the video into a PyTorch Tensor and applies the CoTracker model to extract
    the tracks and visibilities of pixels throughout the entire sequence. The goal is to track the
    movement of specific points across the frames.

    Usage example:

    agent:
        name: my_test_agent
    templates:
    -   template_name: InputTemplate
        class_name: InputTemplate
        attributes: {}
    -   template_name: CoTrackerOffline
        class_name: CoTrackerOffline
        template_input: InputTemplate
        attributes:
            model_cache_dir: './models'
            model_variant: 'scaled'
            device: 'cuda'
            use_segmentation_mask: true
            grid_size: 15
            grid_query_frame: 0
            backward_tracking: false

    """

    _MODEL_TYPE = "offline"

    class AttributesBaseModel(CoTrackerBase.AttributesBaseModel):
        """Configuration attributes for the CoTrackerInference template.

        Attributes:
            use_segmentation_mask (bool): Whether to use segmentation masks for tracking. Default is False.
            grid_size (int): Size of the grid, i.e., the number of points to track in the video.
            grid_query_frame (int): Frame index from which to start tracking for grid-based tracking. Default is 0.
            backward_tracking (bool): Whether to enable backward tracking. Default is False.
        """

        use_segmentation_mask: bool = False
        grid_size: int
        grid_query_frame: int = 0
        backward_tracking: bool = False

    def __init__(self, attributes: TemplateAttributeType) -> None:
        super().__init__(attributes)
        self.cotracker = CoTrackerPredictor(self.checkpoint_path).to(self.attributes.device)

    def _inference(self, video: torch.Tensor, mask: torch.Tensor | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        """Tracks pixels in a video using the CoTracker model.

        Args:
            video (torch.Tensor): The input video as a torch tensor of shape (B, N, C, H, W),
                where B is the batch size, N is the number of frames, C is the number of channels,
                and H and W are the height and width of the frames.
            mask (torch.Tensor | None): Optional segmentation mask of shape (B, 1, H, W) to restrict tracking
                to specific regions. Default is None.

        Returns:
            tuple[torch.Tensor, torch.Tensor]: A tuple containing:
                - pred_tracks: The predicted trajectories of the tracked points.
                - pred_visibility: The visibility of the tracked points.
        """
        tracks, visibilities = self.cotracker(
            video,
            segm_mask=mask,
            grid_size=self.attributes.grid_size,
            grid_query_frame=self.attributes.grid_query_frame,
            backward_tracking=self.attributes.backward_tracking,
        )
        return cast(torch.Tensor, tracks), cast(torch.Tensor, visibilities)

    def _extract_segmentation_masks(self, image_packets: list[ImagePacket]) -> torch.Tensor:
        """Extracts and merges segmentation masks from image packets.

        Args:
            image_packets (list[ImagePacket]): List of image packets containing images and annotations.

        Returns:
            torch.Tensor: A tensor of shape (B, 1, H, W) containing the merged segmentation masks.
        """
        masks = []
        for image_packet in image_packets:
            default_mask = np.zeros_like(image_packet.content[:, :, 0], dtype=np.uint8)

            for annotation in image_packet.annotations:
                if annotation.segmentation and annotation.segmentation.mask is not None:
                    default_mask = np.logical_or(default_mask, annotation.segmentation.mask).astype(np.uint8)

            masks.append(default_mask)

        masks = np.stack(masks)
        masks = torch.tensor(masks, device=self.attributes.device).unsqueeze(1)
        return masks

    def execute(self, container: DataContainer) -> DataContainer:
        """Processes the input `DataContainer` and stores the tracking results.

        Args:
            container (DataContainer): The input data container.

        Returns:
            DataContainer: The updated data container with the tracking results. If no results are produced,
                the original container is returned unchanged.
        """
        if not container.images:
            return container

        image_packets = container.images
        frames = np.asarray([image.content for image in image_packets])
        masks = self._extract_segmentation_masks(image_packets) if self.attributes.use_segmentation_mask else None
        torch_video = self.pre_process_video(frames, self.attributes.device)
        tracks, visibilities = self._inference(torch_video, masks)
        self.save_results(tracks, visibilities, container)

        return container
