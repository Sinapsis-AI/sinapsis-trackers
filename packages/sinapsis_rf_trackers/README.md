<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Roboflow Trackers
<br>
</h1>

<h4 align="center">Multi-object tracking templates using SORT and DeepSORT algorithms powered by Roboflow</h4>

<p align="center">
<a href="#installation">🐍  Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#license"> 🔍 License </a>
</p>

The `sinapsis-rf-trackers` module provides powerful and flexible implementations for multi-object tracking using **SORT** and **DeepSORT** algorithms from the **Roboflow trackers library**. This package offers seamless integration with Sinapsis workflows, allowing users to easily configure and run **tracking pipelines** for video input processing, object detection, and tracking tasks with various detector backends.

<h2 id="installation"> 🐍  Installation </h2>

Install using your package manager of choice. We encourage the use of <code>uv</code>

Example with <code>uv</code>:

```bash
  uv pip install sinapsis-rf-trackers --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-rf-trackers --extra-index-url https://pypi.sinapsis.tech
```

### Optional Dependencies

For complete functionality with different detectors and I/O operations:

```bash
# For Ultralytics YOLO detectors
uv pip install sinapsis-rf-trackers[sinapsis-ultralytics] --extra-index-url https://pypi.sinapsis.tech

# For DFINE detectors
uv pip install sinapsis-rf-trackers[sinapsis-dfine] --extra-index-url https://pypi.sinapsis.tech

# For video processing capabilities
uv pip install sinapsis-rf-trackers[sinapsis-data-readers,sinapsis-data-writers] --extra-index-url https://pypi.sinapsis.tech

# Install all dependencies
uv pip install sinapsis-rf-trackers[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Features</h2>

<h3> Templates Supported</h3>

The **Sinapsis RF Trackers** module provides Sinapsis templates that wrap Roboflow's proven tracking algorithms for multi-object tracking. The package leverages the **Roboflow trackers library** to deliver enterprise-grade tracking performance with easy-to-use configurations.

Currently, the package includes the following templates:

- **SORTTrackerInference**: Simple Online and Realtime Tracking algorithm implementation from Roboflow, featuring motion-based tracking using Kalman filters and Hungarian algorithm for data association.

    <details>
    <summary>Attributes</summary>

    - `track_activation_threshold` (Optional): Detection confidence threshold for track activation. Increasing this value improves accuracy and stability but might miss true detections. Decreasing it increases completeness but risks introducing noise and instability (default: `0.25`).
    - `lost_track_buffer` (Optional): Number of frames to buffer when a track is lost. Increasing this value enhances occlusion handling, significantly reducing the likelihood of track fragmentation or disappearance caused by brief detection gaps (default: `30`).
    - `frame_rate` (Optional): The frame rate of the video sequence being processed. This affects the temporal dynamics of the tracking algorithm (default: `30.0`).
    - `minimum_consecutive_frames` (Optional): Number of consecutive frames that an object must be tracked before it is considered a 'valid' track. Increasing this value prevents the creation of accidental tracks from false detection or double detection, but risks missing shorter tracks (default: `3`).
    - `minimum_iou_threshold` (Optional): Minimum IoU threshold for associating detections with tracks. Higher values require better spatial overlap for association, improving precision but potentially reducing recall (default: `0.3`).

    </details>

- **DeepSORTTrackerInference**: Enhanced SORT algorithm from Roboflow with deep appearance features for improved re-identification and reduced identity switches during occlusions.

    <details>
    <summary>Attributes</summary>

    - `track_activation_threshold` (Optional): Detection confidence threshold for track activation. Increasing this value improves accuracy and stability but might miss true detections. Decreasing it increases completeness but risks introducing noise and instability (default: `0.25`).
    - `lost_track_buffer` (Optional): Number of frames to buffer when a track is lost. Increasing this value enhances occlusion handling, significantly reducing the likelihood of track fragmentation or disappearance caused by brief detection gaps (default: `30`).
    - `frame_rate` (Optional): The frame rate of the video sequence being processed. This affects the temporal dynamics of the tracking algorithm (default: `30.0`).
    - `minimum_consecutive_frames` (Optional): Number of consecutive frames that an object must be tracked before it is considered a 'valid' track. Increasing this value prevents the creation of accidental tracks from false detection or double detection, but risks missing shorter tracks (default: `3`).
    - `minimum_iou_threshold` (Optional): Minimum IoU threshold for associating detections with tracks. Higher values require better spatial overlap for association, improving precision but potentially reducing recall (default: `0.3`).
    - `appearance_threshold` (Optional): Threshold for appearance-based matching. Higher values make the tracker more conservative in appearance matching, reducing identity switches but potentially losing tracks during occlusions (default: `0.7`).
    - `appearance_weight` (Optional): Weight of appearance features versus motion features in the association cost. Higher values prioritize appearance matching, lower values prioritize motion consistency (default: `0.5`).
    - `distance_metric` (Optional): Distance metric for appearance feature comparison. Supported metrics include 'cosine' and 'euclidean'. Cosine distance is generally more robust for appearance features (default: `"cosine"`).
    - `reid_model_name` (Optional): Name of the ReID model to use. Should be compatible with either timm library or custom model format (default: `"tf_efficientnet_b1.in1k"`).
    - `reid_device` (Optional): Device to run feature extraction on. CUDA provides faster inference but requires GPU availability. Options: `"auto"`, `"cuda"`, `"cpu"` (default: `"auto"`).
    - `reid_get_pooled_features` (Optional): Whether to use pooled features from the Re-ID model (default: `true`).
    - `reid_kwargs` (Optional): Additional keyword arguments to pass to the Re-ID model constructor.

    </details>

> [!TIP]
> Use CLI command ``` sinapsis info --all-template-names``` to show a list with all the available Template names installed with Sinapsis RF Trackers.

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***SORTTrackerInference*** use ```sinapsis info --example-template-config SORTTrackerInference``` to produce the following example config:

```yaml
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
```

For ***DeepSORTTrackerInference*** use ```sinapsis info --example-template-config DeepSORTTrackerInference``` to produce the following example config:

```yaml
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
    reid_device: "cuda"
```

<details>
<summary><strong><span style="font-size: 1.25em;">📚 Example Usage</span></strong></summary>

Below are example YAML configurations for processing video files and performing real-time tracking using different detector backends with Roboflow's tracking algorithms.

<details>
<summary><strong><span style="font-size: 1.4em;">SORT with Ultralytics YOLO</span></strong></summary>

```yaml
agent:
  name: sort_tracker_agent
  description: "SORT tracking with Ultralytics detector"

templates:
  - template_name: InputTemplate
    class_name: InputTemplate
    attributes: {}

  - template_name: VideoReaderCV2
    class_name: VideoReaderCV2
    template_input: InputTemplate
    attributes:
      video_file_path: "artifacts/demo_video.mp4"
      batch_size: -1

  - template_name: UltralyticsPredict
    class_name: UltralyticsPredict
    template_input: VideoReaderCV2
    attributes:
      model_class: YOLO
      model: yolo11n.pt
      task: detect
      prediction_params:
        conf: 0.7
        iou: 0.8

  - template_name: SORTTrackerInference
    class_name: SORTTrackerInference
    template_input: UltralyticsPredict
    attributes:
      track_activation_threshold: 0.25
      lost_track_buffer: 30
      minimum_consecutive_frames: 3
      minimum_iou_threshold: 0.3
      frame_rate: 30

  - template_name: BBoxDrawer
    class_name: BBoxDrawer
    template_input: SORTTrackerInference
    attributes:
      overwrite: true
      randomized_color: false
      draw_extra_labels: true

  - template_name: VideoWriterCV2
    class_name: VideoWriterCV2
    template_input: BBoxDrawer
    attributes:
      destination_path: "artifacts/tracked_result.mp4"
      height: -1
      width: -1
      fps: 30
```
</details>

<details>
<summary><strong><span style="font-size: 1.4em;">DeepSORT with DFINE</span></strong></summary>

```yaml
agent:
  name: deepsort_tracker_agent
  description: "DeepSORT tracking with DFINE detector"

templates:
  - template_name: InputTemplate
    class_name: InputTemplate
    attributes: {}

  - template_name: VideoReaderCV2
    class_name: VideoReaderCV2
    template_input: InputTemplate
    attributes:
      video_file_path: "artifacts/demo_video.mp4"
      batch_size: -1

  - template_name: DFINEInference
    class_name: DFINEInference
    template_input: VideoReaderCV2
    attributes:
      threshold: 0.5
      config_file: artifacts/configs/dfine/dfine_hgnetv2_n_coco.yml
      device: cuda
      pretrained_model:
        size: n
        variant: coco

  - template_name: DeepSORTTrackerInference
    class_name: DeepSORTTrackerInference
    template_input: DFINEInference
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
      reid_device: "cuda"

  - template_name: BBoxDrawer
    class_name: BBoxDrawer
    template_input: DeepSORTTrackerInference
    attributes:
      overwrite: true
      randomized_color: false
      draw_extra_labels: true

  - template_name: VideoWriterCV2
    class_name: VideoWriterCV2
    template_input: BBoxDrawer
    attributes:
      destination_path: "artifacts/tracked_result.mp4"
      height: -1
      width: -1
      fps: 30
```
</details>

**IMPORTANT**: The VideoReaderCV2, BBoxDrawer, and VideoWriterCV2 templates are part of the [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers), [sinapsis-data-visualization](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_visualization), and [sinapsis-data-writers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers) packages, respectively. The UltralyticsPredict template is part of [sinapsis-ultralytics](https://github.com/Sinapsis-AI/sinapsis-ultralytics) and DFINEInference is part of [sinapsis-dfine](https://github.com/Sinapsis-AI/sinapsis-dfine). To use these examples, ensure you have installed the corresponding packages.

To run the config, use the CLI:
```bash
sinapsis run your_config.yml
```

</details>

<h2 id="documentation">📙 Documentation</h2>

Documentation for this and other sinapsis packages is available on the [sinapsis website](https://docs.sinapsis.tech/docs)

Tutorials for different projects within sinapsis are available at [sinapsis tutorials page](https://docs.sinapsis.tech/tutorials)


<h2 id="license">🔍 License</h2>

This project is licensed under the AGPLv3 license, which encourages open collaboration and sharing. For more details, please refer to the [LICENSE](LICENSE) file.

For commercial use, please refer to our [official Sinapsis website](https://sinapsis.tech) for information on obtaining a commercial license.
