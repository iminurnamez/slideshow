from itertools import cycle

import pygame as pg

from .. import tools, prepare
from ..components.animation import Animation


class Viewing(tools._State):
    def __init__(self):
        super(Viewing, self).__init__()
        self.fade = True
        
    def startup(self, persistent):
        self.persist = persistent
        self.images = cycle(self.persist["images"])
        self.view_time = 5000
        self.timer = 0
        self.animations = pg.sprite.Group()
        self.next_image()


    def next_image(self):
        self.animations.empty()
        self.base_image = next(self.images)
        self.base_rect = self.base_image.get_rect()
        self.rect = self.base_rect.fit(prepare.SCREEN_RECT)
        self.img_width, self.img_height = self.rect.size
        final_w = int(self.img_width * 1.2)
        final_h = int(self.img_height * 1.2)
        ani = Animation(img_width=final_w, img_height=final_h,
                                duration=self.view_time, round_values=True)
        ani.start(self)
        self.animations.add(ani)
        if self.fade:
            self.alpha = 0
            dur = self.view_time // 4
            ani3 = Animation(alpha=255, duration=dur)
            ani3.start(self)
            ani3.callback = self.fade_out
            
            self.animations.add(ani3)
        
    def fade_out(self):
        self.alpha = 255
        dur = self.view_time//4
        delay_ = self.view_time - (self.timer + dur)        
        ani2 = Animation(alpha=0, duration=dur, delay=delay_)          
        ani2.start(self)
        self.animations.add(ani2)
        
    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_UP:
                self.view_time *= .9
            elif event.key == pg.K_DOWN:
                self.view_time *= 1.1
            elif event.key == pg.K_f:
                self.fade = not self.fade
                self.animations.empty()
                self.alpha = 255
                
    def update(self, dt):
        self.animations.update(dt)
        self.timer += dt
        if self.timer >= self.view_time:
            self.timer -= self.view_time
            self.next_image()
        self.rect.size = (self.img_width // 2) * 2, (self.img_height // 2) * 2
        self.rect.center = prepare.SCREEN_RECT.center
        self.image = pg.transform.smoothscale(self.base_image, self.rect.size)
        self.image.set_alpha(self.alpha)
        
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.image, self.rect)
        