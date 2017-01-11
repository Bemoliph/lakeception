# -*- coding: utf-8 -*-

import logging
import pygame

from lakeutils import asset_exists, get_file_path

LOGGER = logging.getLogger()


class Audio(object):
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
    
    @staticmethod
    def pre_init():
        LOGGER.debug(u'Pre-Initializing Audio.')
        
        # TODO: Load audio settings from config file; detect frequency?
        pygame.mixer.pre_init(
            frequency=44100,
            size=16,
            channels=2,
            buffer=4096,
        )
    
    def play_sound(self, asset_path):
        if pygame.mixer.get_init() and asset_exists(asset_path):
            LOGGER.debug(u'Playing sound: %s', asset_path)
            sound = pygame.mixer.Sound(get_file_path(asset_path))
            channel = sound.play()
            
            return sound, channel
    
    def play_music(self, asset_path, fadeout_time=1000):
        if pygame.mixer.get_init() and asset_exists(asset_path):
            if self.is_playing_music() and fadeout_time:
                LOGGER.debug(u'Fading out music over %sms', fadeout_time)
                pygame.mixer.music.fadeout(fadeout_time)
            
            LOGGER.debug(u'Playing music: %s', asset_path)
            pygame.mixer.music.load(get_file_path(asset_path))
            pygame.mixer.music.play(loops=-1)
            
            self.is_music_paused = False
            self.current_music = asset_path
    
    def stop_music(self):
        LOGGER.debug(u'Stopping music.')
        pygame.mixer.music.stop()
    
    def pause_music(self):
        LOGGER.debug(u'Pausing music.')
        pygame.mixer.music.pause()
        self.is_music_paused = True
    
    def unpause_music(self):
        LOGGER.debug(u'Unpausing music.')
        pygame.mixer.music.unpause()
        self.is_music_paused = False
    
    def is_playing_music(self):
        return not self.is_music_paused and pygame.mixer.music.get_busy()
