import os

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.title = Label("Choose Gallery", {"midtop": prepare.SCREEN_RECT.midtop},
                                 font_size=32)
        self.make_buttons()
        
    def load_directories(self):
        dirs = []
        p = os.path.join("images")
        names = os.listdir(p)
        for name in names:
            dirs.append(name)
        return dirs
        
    def load_directory(self, directory):
        images = []
        for name in os.listdir(directory):
            img = pg.image.load(os.path.join(directory, name)).convert()
            images.append(img)
        self.persist["images"] = images
        self.done = True
        self.next = "GALLERY"
        
    def make_buttons(self):
        thumb_size = 128, 128
        self.buttons = ButtonGroup()
        dirs = self.load_directories()
        left = 50
        top = 80
        h_space = 30
        v_space = 30
        for d in dirs:
            p = os.path.join("images", d)
            first = os.listdir(p)[0]
            img = pg.image.load(os.path.join(p, first)).convert()
            thumb = pg.transform.smoothscale(img, thumb_size)
            label = Label(d, {"midtop": (thumb_size[0] // 2, thumb_size[1])},
                               font_size=16, text_color="gray90", fill_color="gray20")
            final = pg.Surface((thumb_size[0], thumb_size[1] + label.rect.height))
            pg.draw.rect(final, pg.Color("gray20"), final.get_rect())
            final.blit(thumb, (0, 0))
            final.blit(label.image, label.rect)
            
            pg.draw.rect(final, pg.Color("gray80"), final.get_rect(), 2)
            Button((left, top), self.buttons, idle_image=final,
                       button_size=final.get_size(), call=self.load_directory,
                       args=os.path.join("images", d))
            left += thumb_size[0] + h_space
            if left + thumb_size[0] > prepare.SCREEN_SIZE[0]:
                top += thumb_size[1] + v_space
    
    def startup(self, persistent):
        self.persist = persistent
        
    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.buttons.get_event(event)
            
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        surface.fill(pg.Color("gray10"))
        self.title.draw(surface)
        self.buttons.draw(surface)