<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis CoTracker
<br>
</h1>

<h4 align="center">Templates for multi-object tracking and visualization using the CoTracker model</h4>

<p align="center">
<a href="#installation">🐍  Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#license"> 🔍 License </a>
</p>

The `siinapsis-cotracker` module provides a robust and flexible implementation for multi-object tracking using the [**CoTracker**](https://cotracker3.github.io/) model. It enables users to easily configure and run **tracking pipelines** for video input processing and visualization tasks.

<h2 id="installation"> 🐍  Installation </h2>

Install using your package manager of choice. We encourage the use of <code>uv</code>

> [!WARNING]
> ```cotracker``` dependency is required to install ```sinapsis-cotracker```

<h4> UV instructions</h4>

Install cotracker in your working environment as follows:

```bash
uv pip install git+https://github.com/facebookresearch/co-tracker.git
```
then install sinapsis-cotracker
```bash
uv pip install sinapsis-cotracker --extra-index-url https://pypi.sinapsis.tech
```

<h4> Raw pip instructions</h4>

Install cotracker in your working environment as follows:
```bash
pip install git+https://github.com/facebookresearch/co-tracker.git
```
then install sinapsis-cotracker
```bash
pip install sinapsis-cotracker --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Features</h2>

<h3> Templates Supported</h3>

The **Sinapsis CoTracker** module offers a set of templates for multi-object tracking and visualization using the **CoTracker** model. These templates enable users to perform both online and offline tracking, process video inputs, and visualize tracking results on video frames. The templates in this package include functionality for:

- **CoTrackerOffline**: Handles offline multi-object tracking with customizable parameters for segmentation, grid size, and backward tracking.
- **CoTrackerOnline**: Supports real-time object tracking with advanced grid query and support grid features.
- **CoTrackerVisualizer**: Visualizes tracking results with customizable trace, line width, and visualization modes.

> [!TIP]
> Use CLI command ``` sinapsis info --all-template-names``` to show a list with all the available Template names installed with Sinapsis CoTracker.

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***CoTrackerOffline*** use ```sinapsis info --example-template-config CoTrackerOffline``` to produce the following example config:

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: CoTrackerOffline
  class_name: CoTrackerOffline
  template_input: InputTemplate
  attributes:
    device: '`replace_me:typing.Literal[''cuda'', ''cpu'']`'
    generic_key_field: CoTrackerResults
    model_cache_dir: /home/cv/.cache/sinapsis
    model_variant: '`replace_me:typing.Literal[''baseline'', ''scaled'']`'
    use_segmentation_mask: false
    grid_size: '`replace_me:<class ''int''>`'
    grid_query_frame: 0
    backward_tracking: false
```

<details>
<summary><strong><span style="font-size: 1.25em;">📚 Example Usage</span></strong></summary>

Below is an example YAML configuration for processing a video file and visualizing tracking results using **Sinapsis CoTracker** templates. This setup loads a video with the **VideoReaderCV2**, performs real-time object tracking with the **CoTrackerOnline** template, visualizes the results with the **CoTrackerVisualizer**, and saves the output as a new video file using the **VideoWriterCV2**.
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

This configuration defines an **agent** and a sequence of **templates** for video processing, object tracking, and visualization.

**IMPORTANT**: The VideoReaderCV2 and VideoWriterCV2 templates are part of the [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers) and [sinapsis-data-writers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers) packages, respectively. To use this example, ensure that you have installed these packages.


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



