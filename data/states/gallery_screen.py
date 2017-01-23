import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup


class GallerySlot(object):
    def __init__(self, topleft, size, thumbnail):
        self.thumb_size = size
        self.rect = pg.Rect(topleft, size)
        self.img_rect = self.rect.copy()
        self.thumbnail = thumbnail
        self.grabbed = False

    def get_event(self, event):
        to_place = None
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.rect.collidepoint((x, y)):
                self.grab_point = x - self.rect.left, y - self.rect.top
                self.grabbed = True
        elif event.type == pg.MOUSEBUTTONUP:
            if self.grabbed:
                self.grabbed = False
                to_place = True
        return to_place
        
    def update(self, mouse_pos):
        if self.grabbed:
            x, y = mouse_pos
            self.img_rect.left = x - self.grab_point[0]
            self.img_rect.top = y - self.grab_point[1]
        
    def draw(self, surface):
        pg.draw.rect(surface, pg.Color("white"), self.rect.inflate((2, 2)), 2)
        surface.blit(self.thumbnail, self.img_rect)

        
class GalleryScreen(tools._State):
    def __init__(self):
        super(GalleryScreen, self).__init__()
        cx = prepare.SCREEN_RECT.centerx
        self.instruction = Label("Drag and drop thumbnails to change order",
                                          {"midtop": (cx, 0)}, font_size=24,
                                          text_color="gray80")
        self.buttons = ButtonGroup()
        bw, bh = 120, 30
        Button((cx - (bw//2), prepare.SCREEN_RECT.bottom - (bh + 10)),
                  self.buttons, button_size=(bw, bh), text="START",
                  text_color="gray80", font_size=32, fill_color="gray20",
                  hover_fill_color="gray30", hover_text="START",
                  hover_text_color="gray90", call=self.next_state)

    def next_state(self, *args):
        self.persist["images"] = self.images
        self.done = True
        self.next = "VIEWING"        
        
    def startup(self, persistent):
        self.persist = persistent
        self.images = self.persist["images"]
        self.make_slots()
        
    def make_slots(self):
        thumb_size = 64, 64
        self.slots = {}
        left, top = 50, 50
        h_space = 30
        v_space = 20
        for i, image in enumerate(self.images):
            thumb = pg.transform.smoothscale(image, thumb_size)
            self.slots[i] = GallerySlot((left, top), thumb_size, thumb)
            left += thumb_size[0] + h_space
            if left + thumb_size[0] > prepare.SCREEN_RECT.right:
                top += thumb_size[1] + v_space
                left = 50
                
    def get_event(self, event):
        self.buttons.get_event(event)
        for num, slot in self.slots.items():
            to_place = slot.get_event(event)
            if to_place:
                for i, s in self.slots.items():
                    if slot.img_rect.colliderect(s.rect):
                        if i >= num:
                            left = self.images[:num]
                            right = self.images[num + 1:i + 1]
                            end = self.images[i + 1:]
                            imgs = left + right + [self.images[num]] + end
                        elif i < num:
                            left = self.images[:i]
                            right = self.images[i:]
                            right.remove(self.images[num])
                            imgs = left + [self.images[num]] + right
                        self.images = imgs
                        for j, image in enumerate(self.images):
                            current = self.slots[j]
                            current.thumbnail = pg.transform.smoothscale(image, current.thumb_size)
                            current.img_rect = current.rect.copy()
                        return
                else:
                    slot.img_rect = slot.rect.copy()
                    return
                return
                            
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        for slot in self.slots.values():
            slot.update(mouse_pos)
        
    def draw(self, surface):
        surface.fill(pg.Color("gray10"))
        for slot in self.slots.values():
            slot.draw(surface)
        self.instruction.draw(surface)
        self.buttons.draw(surface)        