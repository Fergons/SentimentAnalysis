# -*- coding: utf-8 -*-
# file: deploy_demo.py
# time: 2021/10/10
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

import gradio as gr
import pandas as pd

from pyabsa import ATEPCCheckpointManager

aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(checkpoint='multilingual',
                                                               auto_device=True  # False means load model on CPU
                                                               )


def inference(text):
    result = aspect_extractor.extract_aspect(inference_source=[text],
                                             save_result=False,
                                             print_result=False,
                                             pred_sentiment=True)

    result = pd.DataFrame({
        'aspect': result[0]['aspect'],
        'sentiment': result[0]['sentiment']
    })

    return result


if __name__ == '__main__':
    inference(test_set[0])
