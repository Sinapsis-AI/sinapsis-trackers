# -*- coding: utf-8 -*-
from collections import deque

import numpy as np
import torch
from cotracker.predictor import CoTrackerOnlinePredictor
from sinapsis_core.data_containers.data_packet import DataContainer

from sinapsis_cotracker.templates.co_tracker_base import CoTrackerBase


class CoTrackerOnline(CoTrackerBase):
    """Template for online, incremental pixel tracking using the CoTracker model.

    This template is designed for "generator" agent mode, meaning it processes video
    as a stream of frames arriving over time. It is stateful, maintaining an
    internal memory (buffer) of previous frames to ensure continuous and coherent
    tracking between sequential executions. It is the ideal choice for real-time
    applications or for processing video data in small, incremental chunks.

    Usage example:

    agent:
        name: my_test_agent
    templates:
    -   template_name: InputTemplate
        class_name: InputTemplate
        attributes: {}
    -   template_name: CoTrackerOnline
        class_name: CoTrackerOnline
        template_input: InputTemplate
        attributes:
            model_cache_dir: './models'
            model_variant: 'scaled'
            device: 'cuda'
            grid_size: 15
            grid_query_frame: 0
            add_support_grid: false

    """

    _MODEL_TYPE = "online"

    class AttributesBaseModel(CoTrackerBase.AttributesBaseModel):
        """Configuration attributes for the CoTrackerOnline template.

        Attributes:
            grid_size (int): The size of the grid for sampling points. Default is 5.
            grid_query_frame (int): The frame index from which to sample the grid points.
                Default is 0.
            add_support_grid (bool): Whether to add a support grid for tracking. Default is False.
        """

        grid_size: int = 5
        grid_query_frame: int = 0
        add_support_grid: bool = False

    def initialize(self) -> None:
        """Initializes the template's common state for creation or reset.
        This method is called by both `__init__` and `reset_state` to ensure
        a consistent state. Can be overriden by subclasses for specific behaviour.
        """
        super().initialize()
        self.cotracker = CoTrackerOnlinePredictor(self.checkpoint_path).to(self.attributes.device)
        self.is_first_step = True
        self.tracks: torch.Tensor | None = None
        self.visibilities: torch.Tensor | None = None
        self.buffer: deque[np.ndarray] = deque(maxlen=self.cotracker.step * 2)
        self.previous_preds_count: int = 0

    def _split_into_chunks(self, frames: list[np.ndarray]) -> list[list[np.ndarray]]:
        """Splits the input frames into chunks based on the model type (scaled or baseline).

        Args:
            frames (list[np.ndarray]): The input video frames as a list of numpy arrays.

        Returns:
            list[list[np.ndarray]]: A list of chunks, where each chunk is a list of frames.
                For the scaled model, chunks are of size `step * 2`. For the baseline model,
                chunks are of size `step`.
        """
        chunks = []
        step = self.cotracker.step
        window_len = self.cotracker.step * 2

        if self.attributes.model_variant == "scaled":
            for i in range(0, len(frames), step):
                chunk = frames[i : i + window_len]
                chunks.append(chunk)
        else:
            for i in range(0, len(frames), step):
                chunk = frames[i : i + step]
                chunks.append(chunk)

        return chunks

    def _inference_step(self, window_frames: deque[np.ndarray]) -> None:
        """Performs inference on a window of frames.

        Args:
            window_frames (deque[np.ndarray]): A deque of frames to process. Each frame is a
                numpy array of shape (H, W, C).

        Returns:
            tuple[torch.Tensor, torch.Tensor]: A tuple containing the predicted tracks and
                visibilities. Tracks have shape (B, T, N, 2), and visibilities have shape
                (B, T, N), where B is the batch size, T is the number of frames, and N is
                the number of points.
        """
        video_array = np.stack(window_frames)
        torch_video = self.pre_process_video(video_array, self.attributes.device)

        self.tracks, self.visibilities = self.cotracker(
            torch_video,
            is_first_step=self.is_first_step,
            grid_size=self.attributes.grid_size,
            grid_query_frame=self.attributes.grid_query_frame,
            add_support_grid=self.attributes.add_support_grid,
        )

    def _inference(self, frames_chunks: list[list[np.ndarray]]) -> None:
        """Processes a list of frame chunks and performs inference on each chunk.

        Args:
            frames_chunks (list[list[np.ndarray]]): A list of chunks, where each chunk is a
                list of frames.

        Returns:
            tuple[torch.Tensor, torch.Tensor]: A tuple containing the predicted tracks and
                visibilities for the processed frames.
        """
        for chunk in frames_chunks:
            for frame in chunk:
                self.buffer.append(frame)
            self._inference_step(self.buffer)
            self.is_first_step = False

    def save_results(self, tracks: torch.Tensor, visibilities: torch.Tensor, container: DataContainer) -> None:
        """Saves the tracking results (tracks and visibilities) to the provided `DataContainer`.

        Args:
            tracks (torch.Tensor): The predicted tracks for the video frames. Shape: (B, T, N, 2),
                where B is the batch size, T is the number of frames, and N is the number of points.
            visibilities (torch.Tensor): The visibility flags for the tracks. Shape: (B, T, N),
                where B is the batch size, T is the number of frames, and N is the number of points.
            container (DataContainer): The `DataContainer` where the results will be stored.
        """
        if tracks is None or visibilities is None:
            return

        n_frames = len(container.images)
        start_index = self.previous_preds_count
        end_index = start_index + n_frames

        if tracks.shape[1] >= end_index:
            final_tracks = tracks[:, start_index:end_index, :, :]
            final_visibilities = visibilities[:, start_index:end_index, :]
            super().save_results(final_tracks, final_visibilities, container)
            self.previous_preds_count = tracks.shape[1]
        else:
            self.logger.warning(
                f"Not enough predictions to save. Needed index up to {end_index}, "
                f"but only {tracks.shape[1]} predictions are available."
            )

    def execute(self, container: DataContainer) -> DataContainer:
        """Processes the input `DataContainer` and returns the updated container.

        Args:
            container (DataContainer): The input `DataContainer` containing video frames and
                other relevant data.

        Returns:
            DataContainer: The updated `DataContainer` with tracking results stored in the
                `generic_data` field.
        """
        if not container.images:
            return container

        image_packets = container.images
        frames = np.asarray([image.content for image in image_packets])
        frames_chunks = self._split_into_chunks(frames)
        self._inference(frames_chunks)
        self.save_results(self.tracks, self.visibilities, container)

        return container

    def _cleanup(self) -> None:
        """Cleans up the inference-specific stateful objects.
        This method moves the main cotracker model to the CPU to free up
        VRAM and then deletes the references to it, preparing the template for
        a full reset.
        """
        if hasattr(self, "cotracker") and self.cotracker is not None:
            self.cotracker.to("cpu")
            del self.cotracker
