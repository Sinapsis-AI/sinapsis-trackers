# -*- coding: utf-8 -*-
import torch
from sinapsis_core.data_containers.data_packet import DataContainer

from sinapsis_cotracker.templates.co_tracker_online import CoTrackerOnline


class CoTrackerOfflineLarge(CoTrackerOnline):
    """Template for batch pixel tracking using the CoTracker model.

    This template is designed for "single" agent mode, where the entire video is
    processed in one independent, stateless execution. While it operates as an offline
    process, it leverages the memory-efficient engine from `CoTrackerOnline` to
    prevent out-of-memory errors, making it the ideal choice for videos that are
    too long for the standard `CoTrackerOffline` template.

    Usage example:

    agent:
        name: my_test_agent
    templates:
    -   template_name: InputTemplate
        class_name: InputTemplate
        attributes: {}
    -   template_name: CoTrackerOfflineLarge
        class_name: CoTrackerOfflineLarge
        template_input: InputTemplate
        attributes:
            model_cache_dir: './models'
            model_variant: 'scaled'
            device: 'cuda'
            grid_size: 15
            grid_query_frame: 0
            add_support_grid: false

    """

    class AttributesBaseModel(CoTrackerOnline.AttributesBaseModel):
        """Configuration attributes for the CoTrackerOfflineLarge template.

        Attributes:
            reset_after_execution (bool): If True, the tracker's state is completely
                reset after each execution to guarantee a stateless, independent run,
                which is the expected behavior for a batch process. Defaults to True.
        """

        reset_after_execution: bool = True

    def save_results(self, tracks: torch.Tensor, visibilities: torch.Tensor, container: DataContainer) -> None:
        """Saves the tracking results (tracks and visibilities) to the provided `DataContainer`.

        Args:
            tracks (torch.Tensor): The predicted tracks for the video frames. Shape: (B, T, N, 2),
                where B is the batch size, T is the number of frames, and N is the number of points.
            visibilities (torch.Tensor): The visibility flags for the tracks. Shape: (B, T, N),
                where B is the batch size, T is the number of frames, and N is the number of points.
            container (DataContainer): The `DataContainer` where the results will be stored.
        """
        n_frames = len(container.images)

        if tracks is not None and visibilities is not None:
            final_tracks = tracks[:, :n_frames, :, :]
            final_visibilities = visibilities[:, :n_frames, :]
            super(CoTrackerOnline, self).save_results(final_tracks, final_visibilities, container)

    def execute(self, container: DataContainer) -> DataContainer:
        """Processes the input `DataContainer` and returns the updated container.

        Args:
            container (DataContainer): The input `DataContainer` containing video frames and
                other relevant data.

        Returns:
            DataContainer: The updated `DataContainer` with tracking results stored in the
                `generic_data` field.
        """
        container = super().execute(container)

        if self.attributes.reset_after_execution:
            self.reset_state()

        return container
