# -*- coding: utf-8 -*-

import os

import gradio as gr
from helpers.download_configs import download_configs_folder
from sinapsis.webapp.agent_gradio_helper import (
    add_logo_and_title,
    css_header,
    init_image_inference,
)
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP

DFINE_CONFIG_DOWNLOAD = os.environ.get("DFINE_CONFIG_DOWNLOAD", False)
DFINE_CONFIGS_PATH = "artifacts/configs"
CONFIG_FILE = (
    AGENT_CONFIG_PATH
    or "packages/sinapsis_supervision/src/sinapsis_supervision/configs/bytetrack_ultralytics_demo_real_time.yml"
)


def realtime_demo() -> gr.Blocks:
    with gr.Blocks(css=css_header()) as demo:
        add_logo_and_title("Sinapsis ByteTrack + DFINE (Realtime)")
        init_image_inference(
            CONFIG_FILE,
            "",
            True,
            app_message="Allow access to your camera and press the record button to enable real-time inference.",
        )
    return demo


if __name__ == "__main__":
    if DFINE_CONFIG_DOWNLOAD and not os.path.exists(DFINE_CONFIGS_PATH):
        download_configs_folder(path=DFINE_CONFIGS_PATH)

    demo = realtime_demo()
    demo.launch(share=bool(GRADIO_SHARE_APP))
