<h1 align="center">
<br>
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a>
<br>
Sinapsis Trackers
<br>
</h1>

<h4 align="center">Mono repo with modular packages for multi-object tracking using advanced algorithms. </h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#packages">📦 Packages</a> •
<a href="#webapps">🌐 Webapps</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#license">🔍 License</a>
</p>


<h2 id="installation">🐍 Installation</h2>

This mono repo consists of modular packages for implementing and visualizing multi-object tracking using various tracking algorithms and models:

* <code>sinapsis-cotracker</code>
* <code>sinapsis-supervision</code>

Install using your package manager of choice. We encourage the use of <code>uv</code>

<h3> sinapsis-cotracker </h3>

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

<h3>sinapsis-supervision</h3>

<h4> UV instructions</h4>

Install sinapsis-supervision
```bash
uv pip install sinapsis-supervision --extra-index-url https://pypi.sinapsis.tech
```

<h4> Raw pip instructions</h4>

Install sinapsis-supervision
```bash
pip install sinapsis-supervision --extra-index-url https://pypi.sinapsis.tech
```

<h3>(Optional) Install packages with all additional dependencies</h3>

> [!IMPORTANT]
Templates in each package may require extra dependencies. For development, we recommend installing the package with all the optional dependencies:

```bash
  uv pip install sinapsis-cotracker[all] --extra-index-url https://pypi.sinapsis.tech

  uv pip install sinapsis-supervision[all] --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-cotracker[all] --extra-index-url https://pypi.sinapsis.tech

  pip install sinapsis-supervision[all] --extra-index-url https://pypi.sinapsis.tech
```

> [!TIP]
> You can also install all the packages within this project:

```bash
  uv pip install sinapsis-tracker[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="packages">📦 Packages</h2>

This repository is organized into modular packages, each designed for specific integration with different tracking models, including CoTracker and ByteTrack. These packages provide ready-to-use templates for applications like object tracking, multi-object tracking, and result visualization in real-time or offline.

Below is an overview of the available packages:
<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">Sinapsis Cotrackers</span></strong></summary>

This sinapsis package provides a robust implementation for multi-object tracking with the Facebook Research's Co-Tracker model. It includes:

- Templates for multi-object tracking using **Co-Tracker**, offering flexible **offline**, **online**, and **visualization** modes.
- Efficient processing and visualization of tracking results directly on video frames for clear output.
- Tools for handling dynamic tracking across frames, including padding, line width, and trace settings.


For specific instructions and further details, see the [README.md](https://github.com/Sinapsis-AI/sinapsis-trackers/blob/main/packages/sinapsis_cotracker/README.md).
</details>
<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">Sinapsis Supervision</span></strong></summary>

This Sinapsis package provides a comprehensive solution for object tracking with the ByteTrack algorithm. It includes:

- A template for object tracking using **ByteTrack**, designed to handle real-time multi-object tracking in videos.
- Detection processing and updates with configurable parameters for track activation, matching, and occlusion handling, improving accuracy and stability.

For more details, see the [README.md](https://github.com/Sinapsis-AI/sinapsis-trackers/blob/main/packages/sinapsis_supervision/README.md).

</details>

For more details, see the [official documentation](https://docs.sinapsis.tech/docs)

<h2 id="webapps">🌐 Webapps</h2>
The webapps included in this project showcase the modularity of the templates, in this case for multi-object tracking and visualization tasks.

> [!IMPORTANT]
> To run the app, you first need to clone this repo:

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-trackers.git
cd sinapsis-trackers
```

> [!NOTE]
> If you'd like to enable external app sharing in Gradio, `export GRADIO_SHARE_APP=True`

> [!NOTE]
> Agent configuration can be updated through the `AGENT_CONFIG_PATH` environment var. You can check the available configurations in each package configs folder.

<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>

**IMPORTANT**: This Docker image depends on the `sinapsis-nvidia:base` image. For detailed instructions, please refer to the [Sinapsis README](https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker).

1. **Build the sinapsis-trackers image**:
```bash
docker compose -f docker/compose.yaml build
```
2. **Start the container**:

For sinapsis-cotracker
```bash
docker compose -f docker/compose_tracker.yaml up sinapsis-cotracker-gradio -d
```

For sinapsis-supervision with default bytetrack-ultralytics demo
```bash
docker compose -f docker/compose_tracker.yaml up sinapsis-supervision-gradio -d
```

For sinapsis-supervision with bytetrack-dfine demo

```bash
export DFINE_CONFIG_DOWNLOAD=True
export AGENT_CONFIG_PATH=/app/sinapsis_supervision/configs/bytetrack_dfine_demo.yml
docker compose -f docker/compose_tracker.yaml up sinapsis-supervision-gradio -d
```

3. **Check the status**:

For sinapsis-cotracker
```bash
docker logs -f sinapsis-cotracker-gradio
```

For sinapsis-supervision
```bash
docker logs -f sinapsis-supervision-gradio
```



4. **The logs will display the URL to access the webapp, e.g.,**:
```bash
Running on local URL:  http://127.0.0.1:7860
```
**NOTE**: The local URL can be different, please check the logs

5. **To stop the app**:
```bash
docker compose -f docker/compose_tracker.yaml down
```
</details>

<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">📦 UV</span></strong></summary>
To run the webapp using the <code>uv</code> package manager, please:

1. **Create the virtual environment and sync the dependencies**:

```bash
uv sync --frozen --extra cotracker
```

2. **Install the sinapsis-trackers package**:



```bash
uv pip install sinapsis-trackers[all] --extra-index-url https://pypi.sinapsis.tech
```

3. **Run the webapp**:

For demo running default [cotracker-online](https://github.com/sinapsis-ai/sinapsis-trackers/blob/fix-deps/packages/sinapsis_cotracker/src/sinapsis_cotracker/configs/cotracker_online.yml) agent config.

```bash
uv run webapps/tracking_demo.py
```

For demo running [bytrack-ultralytics](https://github.com/sinapsis-ai/sinapsis-trackers/blob/fix-deps/packages/sinapsis_supervision/src/sinapsis_supervision/configs/bytetrack_ultralytics_demo.yml) agent config.
```bash
export AGENT_CONFIG_PATH="packages/sinapsis_supervision/src/sinapsis_supervision/configs/bytetrack_ultralytics_demo.yml"
uv run webapps/tracking_demo.py
```

For demo running [bytrack-dfine](https://github.com/sinapsis-ai/sinapsis-trackers/blob/fix-deps/packages/sinapsis_supervision/src/sinapsis_supervision/configs/bytetrack_dfine_demo.yml) agent config.
```bash
export DFINE_CONFIG_DOWNLOAD=True
export AGENT_CONFIG_PATH="packages/sinapsis_supervision/src/sinapsis_supervision/configs/bytetrack_dfine_demo.yml"
uv run webapps/tracking_demo.py
```

4. **The terminal will display the URL to access the webapp, e.g.**:
```bash
Running on local URL:  http://127.0.0.1:7860
```

**NOTE**: The local URL can be different, please check the output of the terminal.

</details>


<h2 id="documentation">📙 Documentation</h2>

Documentation is available on the [sinapsis website](https://docs.sinapsis.tech/docs)

Tutorials for different projects within sinapsis are available at [sinapsis tutorials page](https://docs.sinapsis.tech/tutorials)

<h2 id="license">🔍 License</h2>

This project is licensed under the AGPLv3 license, which encourages open collaboration and sharing. For more details, please refer to the [LICENSE](LICENSE) file.

For commercial use, please refer to our [official Sinapsis website](https://sinapsis.tech) for information on obtaining a commercial license.




