import pygame as pg
import numpy as np
import sys
import random

from GameField import *
from Controls import *
from Robot import *
from EditorFunctions import *
from EditorControls import *
from Button import *

BACKGROUND_COLOR = [70, 44, 133]
SCREEN_SIZE_DEFAULT = [1280, 720]
SCREEN_NAME_DEFAULT = "Quadratia"

RENDER_SHIFT = [0, 0]


class QuadratiaEngine:
    def __init__(self, screen_size = SCREEN_SIZE_DEFAULT, screen_name = SCREEN_NAME_DEFAULT, run_type = "EDITOR"):
        pg.init()
        pg.font.init()

        self.run_type = run_type

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        self.screen = pg.display.set_mode(SCREEN_SIZE_DEFAULT)
        self.screen.fill(BACKGROUND_COLOR)
        pg.display.set_caption(SCREEN_NAME_DEFAULT)

        self.FieldSurf = pg.Surface(SCREEN_SIZE_DEFAULT, pg.SRCALPHA)
        self.FieldSurf = self.FieldSurf.convert_alpha()
        self.RobotSurf = pg.Surface(SCREEN_SIZE_DEFAULT, pg.SRCALPHA)
        self.RobotSurf = self.RobotSurf.convert_alpha()

        self.Field = GameField(self.FieldSurf, 6, 5)
        self.Vertun = Robot(self.RobotSurf, self.Field)

        self.Vertun.rect.center = self.Field.Tiles[0].rect.center

        if self.run_type == "EDITOR":
            self.ButtonSurf = pg.Surface(SCREEN_SIZE_DEFAULT, pg.SRCALPHA)
            self.ButtonSurf = self.ButtonSurf.convert_alpha()

            self.XPlusButton: PlusButton = PlusButton(self.ButtonSurf, 1200, 100)
            self.XPlusButton.set_color([0, 255, 0])
            self.XPlusButton.set_text("X++")
            self.XMinusButton: MinusButton = MinusButton(self.ButtonSurf, 1100, 100)
            self.XMinusButton.set_color([255, 0, 0])
            self.XMinusButton.set_text("X--")

            self.YPlusButton: PlusButton = PlusButton(self.ButtonSurf, 1200, 200)
            self.YPlusButton.set_color([0, 255, 0])
            self.YPlusButton.set_text("Y++")
            self.YMinusButton: MinusButton = MinusButton(self.ButtonSurf, 1100, 200)
            self.YMinusButton.set_color([255, 0, 0])
            self.YMinusButton.set_text("Y--")

            self.FileNameButton: TextWindow = TextWindow(self.ButtonSurf, 1150, 550, 200, 50)

            self.SaveButton: Button = Button(self.ButtonSurf, 1100, 650, 100, 50)
            self.SaveButton.set_color()
            self.SaveButton.set_text("SAVE")
            self.LoadButton: Button = Button(self.ButtonSurf, 1225, 650, 100, 50)
            self.LoadButton.set_color()
            self.LoadButton.set_text("LOAD")

            self.ValueMarkInputButton: TextWindow = TextWindow(self.ButtonSurf, 1150, 300, 150, 50)
            self.TileMarkButton: Button = Button(self.ButtonSurf, 1100, 400, 75, 50)
            self.TileMarkButton.set_color([255, 128, 0])
            self.TileMarkButton.set_text("VM T")
            self.WallMarkButton: Button = Button(self.ButtonSurf, 1200, 400, 75, 50)
            self.WallMarkButton.set_color([255, 128, 0])
            self.WallMarkButton.set_text("VM W")


            self.Buttons: list = [self.XPlusButton, self.XMinusButton, self.YPlusButton, self.YMinusButton, 
                                 self.FileNameButton, self.SaveButton, self.LoadButton, 
                                 self.ValueMarkInputButton, self.TileMarkButton, self.WallMarkButton]



    def check_events(self) -> bool:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                self.Field = ToggleFigureTile(self.Field, self.Vertun.x, self.Vertun.y)
                self.Vertun.set_gamefield(self.Field)
            elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.Field, self.Vertun = SetGameFieldSize(self.Field, self.Vertun, random.randint(0, 16), random.randint(0, 16))
        
            elif event.type == pg.KEYDOWN and event.key == pg.K_v:
                GetFigureTiles(self.Field)
                GetMarkedTiles(self.Field)
                GetMarkedWalls(self.Field)
                GetValueMarkedTiles(self.Field)
                GetValueMarkedWalls(self.Field)

            elif event.type == pg.KEYDOWN and event.key == pg.K_l:
                self.Field, self.Vertun = LoadLevel(self.Field, self.Vertun, "Levels/Level1.json")
            elif event.type == pg.KEYDOWN and event.key == pg.K_k:
                self.Field, self.Vertun = LoadLevel(self.Field, self.Vertun, "Levels/Level3.json")
            elif event.type == pg.KEYDOWN and event.key == pg.K_j:
                self.Field, self.Vertun = LoadLevel(self.Field, self.Vertun, "Levels/Test.json")


            #BOOL MARKING
            elif event.type == pg.KEYDOWN and event.key == pg.K_1:
                self.Vertun.MarkTile(self.Field)
            elif event.type == pg.KEYDOWN and event.key == pg.K_2:
                self.Vertun.CleanTile(self.Field)
            elif event.type == pg.KEYDOWN and event.key == pg.K_3:
                self.Vertun.MarkWall(self.Field)
            elif event.type == pg.KEYDOWN and event.key == pg.K_4:
                self.Vertun.CleanWall(self.Field)
        
    
            #VALUE MARKING
            elif event.type == pg.KEYDOWN and event.key == pg.K_5:
                self.Vertun.MarkTileWithValue(self.Field, random.randint(0, 100))
            elif event.type == pg.KEYDOWN and event.key == pg.K_6:
                self.Vertun.CleanTileWithValue(self.Field)
            elif event.type == pg.KEYDOWN and event.key == pg.K_7:
                self.Vertun.MarkWallWithValue(self.Field, random.randint(0, 100))
            elif event.type == pg.KEYDOWN and event.key == pg.K_8:
                self.Vertun.CleanWallWithValue(self.Field)

        

            #MOVEMENT
            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.Vertun.Step()
            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.Vertun.TurnLeft()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.Vertun.TurnRight()

            elif event.type == pg.KEYDOWN and event.key == pg.K_w:
                self.Vertun.move_up()
            elif event.type == pg.KEYDOWN and event.key == pg.K_d:
                self.Vertun.move_right()
            elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                self.Vertun.move_down()
            elif event.type == pg.KEYDOWN and event.key == pg.K_a:
                self.Vertun.move_left()        
            
            #EXIT    
            elif event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return False

        return True



    def render(self):
        # clear framebuffer
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.FieldSurf, RENDER_SHIFT)
        self.screen.blit(self.RobotSurf, RENDER_SHIFT)
        if self.run_type == "EDITOR":
            self.screen.blit(self.ButtonSurf, RENDER_SHIFT)


        # render scene
        self.Field.render()
        self.Vertun.render()
        if self.run_type == "EDITOR":
            for i in range(len(self.Buttons)):
                self.Buttons[i].render()
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        running: bool = True
        while running:
            self.get_time()
            
            if self.run_type == "EDITOR":
                running = EditorEvents(self.screen, self.Field, self.Vertun, self.Buttons)
            if self.run_type == "DEBUG":
                running = self.check_events()

            self.render()
            self.delta_time = self.clock.tick(60)

        pg.quit()

 
if __name__ == '__main__':
    random.seed()

    app = QuadratiaEngine(run_type = "EDITOR")
    app.run()

