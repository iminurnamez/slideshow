import os
import pygame as pg
from . import tools



ORIGINAL_CAPTION = "Game"

pg.mixer.pre_init(44100, -16, 1, 512)

pg.init()
info = pg.display.Info()
SCREEN_SIZE = (info.current_w, info.current_h)
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE, pg.NOFRAME)
SCREEN_RECT = SCREEN.get_rect()


FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
