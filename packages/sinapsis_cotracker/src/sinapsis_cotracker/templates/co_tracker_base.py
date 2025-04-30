# -*- coding: utf-8 -*-
import os
from abc import abstractmethod
from typing import Literal

import numpy as np
import torch
from pydantic import BaseModel, ConfigDict
from sinapsis_core.data_containers.data_packet import DataContainer
from sinapsis_core.template_base import Template
from sinapsis_core.template_base.base_models import TemplateAttributes, TemplateAttributeType, UIPropertiesMetadata, OutputTypes
from sinapsis_core.utils.env_var_keys import SINAPSIS_CACHE_DIR

from sinapsis_cotracker.helpers.file_downloader import download_file


class InferenceResults(BaseModel):
    """Base model to store the predictions and visibilities tensors."""

    tracks: np.ndarray | torch.Tensor | None
    visibilities: np.ndarray | torch.Tensor | None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CoTrackerAttributes(TemplateAttributes):
    """General configuration attributes for the CoTracker templates.

    Attributes:
        device (Literal["cuda", "cpu"]): The device to use for tensor operations.
            Options are "cuda" for GPU processing or "cpu" for CPU processing.
    """

    device: Literal["cuda", "cpu"]


class CoTrackerBase(Template):
    """Base class for Co-tracker templates."""

    _MODEL_TYPE: str | None = None
    UIProperties = UIPropertiesMetadata(category="CoTracker", output_type=OutputTypes.IMAGE)

    class AttributesBaseModel(CoTrackerAttributes):
        """Configuration attributes for the CoTrackerBase.

        Attributes:
            model_cache_dir (str): The directory where the model checkpoint will be cached.
                Defaults to the value of `SINAPSIS_CACHE_DIR`.
            model_variant (Literal["baseline", "scaled"]): The variant of the Co-tracker model
                to use. Options are "baseline" or "scaled".
        """

        model_cache_dir: str = SINAPSIS_CACHE_DIR
        model_variant: Literal["baseline", "scaled"]

    def __init__(self, attributes: TemplateAttributeType) -> None:
        super().__init__(attributes)
        self.checkpoint_path = self._download_model()

    def _download_model(self) -> str:
        """Downloads the model checkpoint from Hugging Face and returns the local path.

        Returns:
            str: The local file path to the downloaded model checkpoint.
        """
        filename = f"{self.attributes.model_variant}_{self._MODEL_TYPE}.pth"
        url = f"https://huggingface.co/facebook/cotracker3/resolve/main/{filename}"
        path = os.path.join(self.attributes.model_cache_dir, filename)
        download_file(
            url,
            path,
            filename,
        )
        return path

    @staticmethod
    def pre_process_video(video_frames: np.ndarray, device: str) -> torch.Tensor:
        """Preprocesses video frames into a torch tensor suitable for Co-tracker processing.

        Args:
            video_frames (np.ndarray): The input video frames as a numpy array of shape
                (N, H, W, C), where N is the number of frames, H is the height, W is the
                width, and C is the number of channels.
            device (str): The device to which the tensor should be moved (e.g., "cuda" or "cpu").

        Returns:
            torch.Tensor: The preprocessed video frames as a torch tensor of shape
                (B, N, C, H, W), where B is the batch dimension.
        """
        tensor_video = torch.Tensor(video_frames).permute(0, 3, 1, 2)[None].float().to(device)
        return tensor_video

    def save_results(self, tracks: torch.Tensor, visibilities: torch.Tensor, container: DataContainer) -> None:
        """Saves the tracking results (tracks and visibilities) to the provided `DataContainer`.

        Args:
            tracks (torch.Tensor): The predicted tracks for the video frames. Shape: (B, T, N, 2),
                where B is the batch size, T is the number of frames, and N is the number of points.
            visibilities (torch.Tensor): The visibility flags for the tracks. Shape: (B, T, N),
                where B is the batch size, T is the number of frames, and N is the number of points.
            container (DataContainer): The `DataContainer` where the results will be stored.
        """
        results = InferenceResults(tracks=tracks.cpu(), visibilities=visibilities.cpu())
        self._set_generic_data(container, results)

    @abstractmethod
    def execute(self, container: DataContainer) -> DataContainer:
        """Processes the input `DataContainer` and returns the updated container.

        This method must be implemented by subclasses to define specific behavior for processing
        video frames and generating tracking results.

        Args:
            container (DataContainer): The input `DataContainer` containing video frames and
                other relevant data.

        Returns:
            DataContainer: The updated `DataContainer` with tracking results stored in the
                `generic_data` field.
        """
