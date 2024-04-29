import pygame as pg
import sys
import random

from GameField import *
from Robot import *
from EditorFunctions import *


def ControlsEvents(screen: pg.surface.Surface, GF: GameField, R: Robot):
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_m:
            GF.SetTileFigure(R.x, R.y, True)
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
            GF, R = SetGameFieldSize(GF, R, random.randint(0, 16), random.randint(0, 16))
        
        #elif event.type == pg.KEYDOWN and event.key == pg.K_t:
            #GF.RecalculateTileSize()
            #R.set_gamefield(GF)


        elif event.type == pg.KEYDOWN and event.key == pg.K_v:
            GetFigureTiles(GF)
            GetMarkedTiles(GF)
            GetMarkedWalls(GF)
            GetValueMarkedTiles(GF)
            GetValueMarkedWalls(GF)

        elif event.type == pg.KEYDOWN and event.key == pg.K_b:
            '''
            FT = [[4, 0], [1, 1], [2, 1], [3, 1], [4, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [2, 3], [3, 3], [2, 4]]
            MT = [[4, 0], [1, 2], [2, 2], [2, 4]]
            MW = [[0, 1, 0], [4, 1, 1], [5, 1, 3], [0, 2, 0], [0, 2, 2], [0, 2, 3], [0, 3, 2]]
            VMT = [[4, 1, 2], [0, 2, 90], [1, 2, 25], [2, 3, 91]]
            VMW = [[4, 0, 1, 13], [4, 0, 2, 3], [5, 0, 3, -999], [1, 3, 1, -999], [2, 3, 3, 34], [1, 4, 1, -999], [2, 4, 0, 61], [2, 4, 1, 94], [2, 4, 3, 1], [3, 4, 3, -999]]
            GF = SetFigureTiles(GF, FT)
            GF = SetMarkedTiles(GF, MT)
            GF = SetMarkedWalls(GF, MW)
            GF = SetValueMarkedTiles(GF, VMT)
            GF = SetValueMarkedWalls(GF, VMW)

            '''
            SaveLevel(GF, R, "Levels/Test.json")

        elif event.type == pg.KEYDOWN and event.key == pg.K_l:
            GF, R = LoadLevel(GF, R, "Levels/Level1.json")
        elif event.type == pg.KEYDOWN and event.key == pg.K_k:
            GF, R = LoadLevel(GF, R, "Levels/Level2.json")



        if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]: #LMB Pressed
            mouse_pos = pg.mouse.get_pos()
            print("Mouse position is " + str(mouse_pos))

            for i in range(len(GF.Tiles)):
                GF.Tiles[i].isClickedLMB = GF.Tiles[i].rect.collidepoint(mouse_pos)

            R.isClickedLMB = R.rect.collidepoint(mouse_pos)

            #for i in range(len(Buttons)):
                #Buttons[i].isClickedLMB = Buttons[i].rect.collidepoint(mouse_pos)

        if event.type == pg.MOUSEBUTTONUP and not pg.mouse.get_pressed()[0]: #LMB Released
            mouse_pos = pg.mouse.get_pos()

            #LMB on Tile -> Toggle isFigure
            for i in range(len(GF.Tiles)):
                if GF.Tiles[i].isClickedLMB and GF.Tiles[i].rect.collidepoint(mouse_pos):
                    GF.Tiles[i].isClickedLMB = False
                    x = i % GF.Xsize
                    y = i // GF.Xsize
                    GF = ToggleFigureTile(GF, x, y)

        if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2]: #RMB Pressed
            mouse_pos = pg.mouse.get_pos()
            print("Mouse position is " + str(mouse_pos))

            for i in range(len(GF.Tiles)):
                GF.Tiles[i].isClickedRMB = GF.Tiles[i].rect.collidepoint(mouse_pos)

            R.isClickedRMB = R.rect.collidepoint(mouse_pos)

            #for i in range(len(Buttons)):
                #Buttons[i].isClickedRMB = Buttons[i].rect.collidepoint(mouse_pos)

        elif event.type == pg.MOUSEBUTTONUP and not pg.mouse.get_pressed()[2]: #RMB Released
            mouse_pos = pg.mouse.get_pos()

            #RMB on Tile -> Toggle Mark
            for i in range(len(GF.Tiles)):
                if GF.Tiles[i].isClickedRMB and GF.Tiles[i].rect.collidepoint(mouse_pos):
                    GF.Tiles[i].isClickedRMB = False
                    x = i % GF.Xsize
                    y = i // GF.Xsize
                    GF = ToggleMarkTile(GF, x, y)


        #BOOL MARKING
        elif event.type == pg.KEYDOWN and event.key == pg.K_1:
            R.MarkTile(GF)
        elif event.type == pg.KEYDOWN and event.key == pg.K_2:
            R.CleanTile(GF)
        elif event.type == pg.KEYDOWN and event.key == pg.K_3:
            R.MarkWall(GF)
        elif event.type == pg.KEYDOWN and event.key == pg.K_4:
            R.CleanWall(GF)
        
    
        #VALUE MARKING
        elif event.type == pg.KEYDOWN and event.key == pg.K_5:
            R.MarkTileWithValue(GF, random.randint(0, 100))
        elif event.type == pg.KEYDOWN and event.key == pg.K_6:
            R.CleanTileWithValue(GF)
        elif event.type == pg.KEYDOWN and event.key == pg.K_7:
            R.MarkWallWithValue(GF, random.randint(0, 100))
        elif event.type == pg.KEYDOWN and event.key == pg.K_8:
            R.CleanWallWithValue(GF)

        

        #MOVEMENT
        elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
            R.Step()
        elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            R.TurnLeft()
        elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            R.TurnRight()

        elif event.type == pg.KEYDOWN and event.key == pg.K_w:
            R.move_up()
        elif event.type == pg.KEYDOWN and event.key == pg.K_d:
            R.move_right()
        elif event.type == pg.KEYDOWN and event.key == pg.K_s:
            R.move_down()
        elif event.type == pg.KEYDOWN and event.key == pg.K_a:
            R.move_left()        
            
        #EXIT    
        elif event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_x):
            return False

    return True
