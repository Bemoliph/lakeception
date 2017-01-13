# -*- coding: utf-8 -*-

import logging
import pygame

from lakeutils import asset_exists, get_abs_asset_path

LOGGER = logging.getLogger()


class Audio(object):
    u"""Convenience wrapper around PyGame to help play sounds and manage music."""

    def __init__(self):
        LOGGER.debug(u'Initializing Audio.')
        
        try:
            pygame.mixer.init()
        except pygame.error:
            LOGGER.warning(u'Failed to initialize audio!')
        else:
            # pygame's music.get_busy() only considers if the music is actually
            # stopped, so pauses need to be tracked manually.
            self.is_music_paused = False
            self.current_music = None

            self.play_music(u'audio/waves.ogg')

    @classmethod
    def pre_init(cls):
        u"""Configures pygame audio.  Must be called before pygame.init()"""
        LOGGER.debug(u'Pre-Initializing Audio.')
        
        # TODO: Load audio settings from config file; detect frequency?
        pygame.mixer.pre_init(
            frequency=44100,
            size=16,
            channels=2,  # Stereo
            buffer=4096,
        )

    def play_sound(self, asset_path, loops=0, max_time=0, fadein_time=0):
        u"""
        Plays an audio file as a "sound".  Useful for voice tracks or sound effects.

        Several sounds can play at once, but PyGame will forcibly stop an existing sound to make room for the new one
        when too many sounds are playing simultaneously.

        :param asset_path: Location of audio file, relative to assets folder.
        :param loops: Number of times to repeat the sound, INCLUDING the first play.  ``-1`` repeats indefinitely.
        :param max_time: Cuts off playback after the given time, in milliseconds.
        :param fadein_time: Fade-in time for the sound, in milliseconds.
        :return: pygame.mixer.Sound, pygame.mixer.Channel
        """
        if pygame.mixer.get_init() and asset_exists(asset_path):
            LOGGER.debug(u'Playing sound: %s', asset_path)
            sound = pygame.mixer.Sound(get_abs_asset_path(asset_path))
            channel = sound.play(loops, max_time, fadein_time)
            
            return sound, channel
    
    def play_music(self, asset_path, loops=0, start_at=0.0, fadeout_time=1000):
        u"""
        Plays an audio file as "music".  Useful for long running audio.

        PyGame only allows playing one music track at a time.  Music tracks are streamed rather than loaded entirely
        into memory before playing, so longer or larger audio files safe here.

        :param asset_path: Location of audio file, relative to assets folder.
        :param loops: Number of times to repeat the music AFTER the first play.  ``-1`` repeats indefinitely.
        :param start_at: When to start within the track.  Seconds for most formats.  Pattern Order Number for MOD.
        :param fadeout_time: Time over which already-playing music fades out, in milliseconds.
        """
        if pygame.mixer.get_init() and asset_exists(asset_path):
            if self.is_playing_music() and fadeout_time:
                LOGGER.debug(u'Fading out current music over %sms', fadeout_time)
                pygame.mixer.music.fadeout(fadeout_time)
            
            LOGGER.debug(u'Playing music: %s', asset_path)
            pygame.mixer.music.load(get_abs_asset_path(asset_path))
            pygame.mixer.music.play(loops, start_at)
            
            self.is_music_paused = False
            self.current_music = asset_path
    
    def stop_music(self):
        u"""Stops any currently playing music."""
        LOGGER.debug(u'Stopping music.')
        pygame.mixer.music.stop()
    
    def pause_music(self):
        u"""Pauses any currently playing music."""
        LOGGER.debug(u'Pausing music.')
        pygame.mixer.music.pause()
        self.is_music_paused = True
    
    def unpause_music(self):
        u"""Un-pauses any currently paused music."""
        LOGGER.debug(u'Unpausing music.')
        pygame.mixer.music.unpause()
        self.is_music_paused = False
    
    def is_playing_music(self):
        u"""Determines if the music is playing, or paused or stopped."""
        return not self.is_music_paused and pygame.mixer.music.get_busy()
