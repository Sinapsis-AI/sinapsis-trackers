<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Supervision
<br>
</h1>

<h4 align="center">Templates for multi-object tracking using the ByteTrack model</h4>

<p align="center">
<a href="#installation">🐍  Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#license"> 🔍 License </a>
</p>

The `sinapsis-supervision` module offers a powerful and flexible implementation for multi-object tracking using the [**ByteTrack**](https://github.com/ifzhang/ByteTrack) algorithm. It allows users to easily configure and run **tracking pipelines** for video input processing, object detection, and tracking tasks.

<h2 id="installation"> 🐍  Installation </h2>

Install using your package manager of choice. We encourage the use of <code>uv</code>

Example with <code>uv</code>:

```bash
  uv pip install sinapsis-supervision --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-supervision --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Features</h2>

<h3> Templates Supported</h3>

The **Sinapsis ByteTrack** module provides a template for multi-object tracking using the **ByteTrack** algorithm. Currently, the package includes the following template:

- **ByteTrack**: A template for tracking objects across video frames, with customizable parameters for track activation, matching thresholds, and occlusion handling.

> [!TIP]
> Use CLI command ``` sinapsis info --all-template-names``` to show a list with all the available Template names installed with Sinapsis Supervision.

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***ByteTrack*** use ```sinapsis info --example-template-config ByteTrack``` to produce the following example config:

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: ByteTrack
  class_name: ByteTrack
  template_input: InputTemplate
  attributes:
    track_activation_threshold: 0.2
    lost_track_buffer: 30
    minimum_matching_threshold: 0.7
    frame_rate: 30
    minimum_consecutive_frames: 1
```

<details>
<summary><strong><span style="font-size: 1.25em;">📚 Example Usage</span></strong></summary>

Below is an example YAML configuration for processing a video file and visualizing tracking results using the **Sinapsis Supervision** template. This configuration loads a video with the **VideoReaderCV2**, performs object detection and real-time tracking with the **UltralyticsPredict** and **ByteTrack** templates, draws bounding boxes around detected objects with the **BBoxDrawer**, and saves the output as a new video file using the **VideoWriterCV2**.

<details>
<summary ><strong><span style="font-size: 1.4em;">Config</span></strong></summary>

```yaml
agent:
  name: cotracker_agent

templates:
  - template_name: InputTemplate
    class_name: InputTemplate
    attributes: {}

  - template_name : VideoReaderCV2
    class_name: VideoReaderCV2
    template_input: InputTemplate
    attributes:
      video_file_path : "artifacts/palace.mp4"
      batch_size: 16

  - template_name: CoTrackerOnline
    class_name: CoTrackerOnline
    template_input: VideoReaderCV2
    attributes:
      model_variant: baseline
      device: cuda
      grid_size: 15

  - template_name: CoTrackerVisualizer
    class_name: CoTrackerVisualizer
    template_input: CoTrackerOnline
    attributes:
      device : cuda
      linewidth: 3
      overwrite: true

  - template_name: VideoWriterCV2
    class_name: VideoWriterCV2
    template_input: CoTrackerVisualizer
    attributes:
      destination_path: "artifacts/result.mp4"
      height: -1
      width: -1
      fps: 30
```
</details>

This configuration defines an **agent** and a sequence of **templates** for video processing, object detection, real-time tracking, and visualization.

**IMPORTANT**: The VideoReaderCV2, BBoxDrawer, and VideoWriterCV2 templates are part of the [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers), [sinapsis-data-visualization](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_visualization), and [sinapsis-data-writers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers) packages, respectively. To use this example, ensure that you have installed these packages.


To run the config, use the CLI:
```bash
sinapsis run name_of_config.yml
```

</details>

<h2 id="documentation">📙 Documentation</h2>

Documentation for this and other sinapsis packages is available on the [sinapsis website](https://docs.sinapsis.tech/docs)

Tutorials for different projects within sinapsis are available at [sinapsis tutorials page](https://docs.sinapsis.tech/tutorials)


<h2 id="license">🔍 License</h2>

This project is licensed under the AGPLv3 license, which encourages open collaboration and sharing. For more details, please refer to the [LICENSE](LICENSE) file.

For commercial use, please refer to our [official Sinapsis website](https://sinapsis.tech) for information on obtaining a commercial license.
