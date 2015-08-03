# -*- coding: utf-8 -*-
import os


AUDIO_DIR = os.path.join(
    os.path.dirname(__file__), "..", "audio",
)


def get_audio_files():
    """
    Returns
    -------
    generator of str
    """
    for filename in os.listdir(AUDIO_DIR):
        path = os.path.abspath(os.path.join(AUDIO_DIR, filename))
        if filename.endswith(".ogg") and os.path.isfile(path):
            yield path
