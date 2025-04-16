# -*- coding: utf-8 -*-

import os

import gradio as gr
from helpers.download_configs import download_configs_folder
from sinapsis.webapp.agent_gradio_helper import add_logo_and_title, css_header, lambda_init_agent
from sinapsis.webapp.agent_webapp_utils import infer_video
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP

DFINE_CONFIG_DOWNLOAD = os.environ.get("DFINE_CONFIG_DOWNLOAD", False)
DFINE_CONFIGS_PATH = "artifacts/configs"
CONFIG_PATH = AGENT_CONFIG_PATH or "packages/sinapsis_cotracker/src/sinapsis_cotracker/configs/cotracker_online.yml"


def create_demo() -> gr.Blocks:
    """Creates and returns the Gradio Blocks demo interface.

    Returns:
        gr.Blocks: The Gradio Blocks object containing the entire interface.
    """
    with gr.Blocks(title="Sinapsis Video Tracking Demo", css=css_header()) as app:
        add_logo_and_title("Sinapsis Video Tracking Demo")
        fn = lambda_init_agent(infer_video, CONFIG_PATH)
        gr.Interface(
            fn,
            inputs=[
                gr.Video(label="input video", format="mp4"),
            ],
            outputs=gr.Video(label="output video", interactive=True, autoplay=True),
            live=False,
            flagging_mode="never",
            submit_btn="Predict",
            article="Upload a video or use your camera to run tracking inferences.",
        )
    return app


if __name__ == "__main__":
    if DFINE_CONFIG_DOWNLOAD and not os.path.exists(DFINE_CONFIGS_PATH):
        download_configs_folder(path=DFINE_CONFIGS_PATH)

    demo = create_demo()
    demo.launch(share=GRADIO_SHARE_APP)
