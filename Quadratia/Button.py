import pygame as pg

from GameField import *
from Robot import *
from EditorFunctions import *

DEFAULT_BUTTON_WIDTH = 50
DEFAULT_BUTTON_HEIGHT = 50
DEFAULT_BUTTON_COLOR = [100, 200, 200]

FONT_SIZE = 36
FONT_COLOR = [0, 0, 0]

LEVELS_DIR = "Levels/"

class Button:
    def __init__(self, screen: pg.surface.Surface, x: int = 0, y: int = 0, width: int = DEFAULT_BUTTON_WIDTH, height: int = DEFAULT_BUTTON_HEIGHT):
        self.screen: pg.surface.Surface = screen
        self.screen_rect: pg.rect.Rect = screen.get_rect()
        self.isClickedLMB: bool = False
        self.isClickedRMB: bool = False
        self.isClickedMMB: bool = False

        if not pg.font.get_init():
            pg.font.init()
        self.text_font: pg.font.Font = pg.font.Font(None, FONT_SIZE)
        self.text_color = FONT_COLOR

        self.surf: pg.surface.Surface = pg.Surface((width, height))
        self.rect: pg.rect.Rect = self.surf.get_rect()
        self.rect.center = (x, y)

    def set_color(self, new_color: list[int] = DEFAULT_BUTTON_COLOR):
        self.surf.fill(new_color)
        
    def set_text(self, text: str):

        text_surf = self.text_font.render(text, True, self.text_color)
        text_pos = text_surf.get_rect()
        text_pos[0] += FONT_SIZE * 0.15
        text_pos[1] += FONT_SIZE * 0.4
        #text_pos.center = self.rect.center

        self.surf.blit(text_surf, text_pos)

    def isReadyToAction(self, mouse_pos) -> bool:
        return bool(self.isClickedLMB and self.rect.collidepoint(mouse_pos))

    def render(self):
        #self.set_color()
        #self.set_text()

        self.screen.blit(self.surf, self.rect)

class PlusButton(Button):
    def __init__(self, screen, x=0, y=0, width=DEFAULT_BUTTON_WIDTH, height=DEFAULT_BUTTON_HEIGHT):
        super().__init__(screen, x=x, y=y, width=width, height=height)

        #self.surf: pg.surface.Surface = pg.image.load('Icons/Plus_Icon.png')
        #self.rect: pg.rect.Rect = self.surf.get_rect()

    def action(self, gamefield: GameField, robot: Robot, coord):
        new_x = gamefield.Xsize
        new_y = gamefield.Ysize

        if coord == 'x' or coord == 0:
            new_x += 1
        elif coord == 'y' or coord == 1:
            new_y += 1

        return SetGameFieldSize(gamefield, robot, new_x, new_y)

class MinusButton(Button):
    def __init__(self, screen, x=0, y=0, width=DEFAULT_BUTTON_WIDTH, height=DEFAULT_BUTTON_HEIGHT):
        return super().__init__(screen, x=x, y=y, width=width, height=height)

    def action(self, gamefield: GameField, robot: Robot, coord):
        new_x = gamefield.Xsize
        new_y = gamefield.Ysize

        if coord == 'x' or coord == 0:
            new_x -= 1
        elif coord == 'y' or coord == 1:
            new_y -= 1

        return SetGameFieldSize(gamefield, robot, new_x, new_y)

class TextWindow(Button):
    def __init__(self, screen, x=0, y=0, width=DEFAULT_BUTTON_WIDTH, height=DEFAULT_BUTTON_HEIGHT):
        self.current_text: str = ""
        self.isActive: bool = False

        return super().__init__(screen, x=x, y=y, width=width, height=height)

    def add_letter(self, letter):
        self.current_text += letter

    def erase_letter(self):
        if self.current_text != "":
            self.current_text = self.current_text[:-1]

    def get_json_filename(self):
        if self.current_text == "":
            return self.current_text
        
        if len(self.current_text) > 5 and self.current_text[-5:] == ".json":
            return LEVELS_DIR + self.current_text
        else:
            return LEVELS_DIR + self.current_text + ".json"

    
    def render(self):
        self.set_color([220, 220, 220])
        self.set_text(self.current_text)

        self.screen.blit(self.surf, self.rect)


