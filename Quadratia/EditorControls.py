import pygame as pg
import json
import random

from GameField import *
from Robot import *
from EditorFunctions import *
from Button import *

def EditorEvents(screen: pg.surface.Surface, GF: GameField, R: Robot, Buttons: list) -> bool:
    for event in pg.event.get():
        #Check if we are texting into FileNameButton:
        if Buttons[4].isActive:
            #if we are texting into ValueMarkInputButton -> cannot input here
            if (Buttons[7].isActive) or (event.type == pg.KEYDOWN and event.key == pg.K_RETURN):
                #Exit typing
                print("FileNameButton: EXITING TYPING MODE")
                Buttons[4].isActive = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                Buttons[4].erase_letter()
            elif event.type == pg.KEYDOWN:
                Buttons[4].add_letter(event.unicode)

        #Check if we are texting into ValueMarkInputButton:
        elif Buttons[7].isActive:
            #if we are texting into FileNameButton -> cannot input here
            if (Buttons[4].isActive) or (event.type == pg.KEYDOWN and event.key == pg.K_RETURN):
                #Exit typing
                print("ValueMarkInputButton: EXITING TYPING MODE")
                Buttons[7].isActive = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                Buttons[7].erase_letter()
            elif event.type == pg.KEYDOWN and (isNumPressed(event)):
                Buttons[7].add_letter(event.unicode)







        #EXIT    
        elif event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            return False


        elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]: #LMB Pressed
            mouse_pos = pg.mouse.get_pos()
            print("Mouse position is " + str(mouse_pos))

            for i in range(len(GF.Tiles)):
                GF.Tiles[i].isClickedLMB = GF.Tiles[i].rect.collidepoint(mouse_pos)

            R.isClickedLMB = R.rect.collidepoint(mouse_pos)

            for i in range(len(Buttons)):
                Buttons[i].isClickedLMB = Buttons[i].rect.collidepoint(mouse_pos)

        elif event.type == pg.MOUSEBUTTONUP and not pg.mouse.get_pressed()[0]: #LMB Released
            mouse_pos = pg.mouse.get_pos()

            #LMB on Tile -> Toggle isFigure
            for i in range(len(GF.Tiles)):
                if GF.Tiles[i].isClickedLMB and GF.Tiles[i].rect.collidepoint(mouse_pos):
                    GF.Tiles[i].isClickedLMB = False
                    x = i % GF.Xsize
                    y = i // GF.Xsize
                    GF = ToggleFigureTile(GF, x, y)

            #LMB on PlusButtons -> inc grid size
            if Buttons[0].isReadyToAction(mouse_pos):
                Buttons[0].isClickedLMB = False
                GF, R = Buttons[0].action(GF, R, 'x')
            if Buttons[2].isReadyToAction(mouse_pos):
                Buttons[2].isClickedLMB = False
                GF, R = Buttons[2].action(GF, R, 'y')

            #LMB on MinusButtons -> dec grid size
            if Buttons[1].isReadyToAction(mouse_pos):
                Buttons[1].isClickedLMB = False
                GF, R = Buttons[1].action(GF, R, 'x')
            if Buttons[3].isReadyToAction(mouse_pos):
                Buttons[3].isClickedLMB = False
                GF, R = Buttons[3].action(GF, R, 'y')

            #LMB on FileNameButton -> start texting inside of it
            if Buttons[4].isReadyToAction(mouse_pos):
                print("FileNameButton: ENTERING TYPING MODE")
                Buttons[4].isClickedLMB = False
                Buttons[4].isActive = True

            #LBM on SaveButton -> Save config in file
            if Buttons[5].isReadyToAction(mouse_pos):
                Buttons[5].isClickedLMB = False
                filename = Buttons[4].get_json_filename()
                if filename == "":
                    print("CANNOT SAVE CONFIG: EMPY FILENAME")
                else:
                    print("SAVING CONFIG INTO " + filename)
                    SaveLevel(GF, R, filename)

            #LBM on LoadButton -> Load config from file
            if Buttons[6].isReadyToAction(mouse_pos):
                Buttons[6].isClickedLMB = False
                filename = Buttons[4].get_json_filename()
                if filename == "":
                    print("CANNOT LOAD CONFIG: EMPTY FILENAME")
                else:
                    print("LOADING CONFIG FROM " + filename)
                    GF, R = LoadLevel(GF, R, filename)

            #LMB on ValueMarkInputButton -> start texting inside of it
            if Buttons[7].isReadyToAction(mouse_pos):
                print("ValueMarkInputButton: ENTERING TYPING MODE")
                Buttons[7].isClickedLMB = False
                Buttons[7].isActive = True

            #LBM on TileMarkButton -> Mark/Clean tile with value
            if Buttons[8].isReadyToAction(mouse_pos):
                Buttons[8].isClickedLMB = False
                value_str = Buttons[7].current_text
                if value_str == "":
                    #Clean tile
                    R.CleanTileWithValue(GF)
                else:
                    R.MarkTileWithValue(GF, int(value_str))

            #LBM on WallMarkButton -> Mark/Clean tile with value
            if Buttons[9].isReadyToAction(mouse_pos):
                Buttons[9].isClickedLMB = False
                value_str = Buttons[7].current_text
                if value_str == "":
                    #Clean tile
                    R.CleanWallWithValue(GF)
                else:
                    R.MarkWallWithValue(GF, int(value_str))
            










        elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2]: #RMB Pressed
            mouse_pos = pg.mouse.get_pos()
            print("Mouse position is " + str(mouse_pos))

            for i in range(len(GF.Tiles)):
                GF.Tiles[i].isClickedRMB = GF.Tiles[i].rect.collidepoint(mouse_pos)

            R.isClickedRMB = R.rect.collidepoint(mouse_pos)

            for i in range(len(Buttons)):
                Buttons[i].isClickedRMB = Buttons[i].rect.collidepoint(mouse_pos)

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
        elif event.type == pg.KEYDOWN and event.key == pg.K_f:
            GF = ToggleFigureTile(GF, R.x, R.y)

        elif event.type == pg.KEYDOWN and event.key == pg.K_m:
            GF = ToggleMarkTile(GF, R.x, R.y)
        elif event.type == pg.KEYDOWN and event.key == pg.K_w:
            GF = ToggleWallMark(GF, R.x, R.y, R.orientation)
        

        #MOVEMENT
        elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
            R.Step()
        elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            R.TurnLeft()
        elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            R.TurnRight()
        

    return True



def isNumPressed(event) -> bool:
    if event.key == pg.K_1 or event.key == pg.K_2 or event.key == pg.K_3 or event.key == pg.K_4 or event.key == pg.K_5:
        return True
    elif event.key == pg.K_6 or event.key == pg.K_7 or event.key == pg.K_8 or event.key == pg.K_9 or event.key == pg.K_0:
        return True
    elif event.key == pg.K_KP1 or event.key == pg.K_KP2 or event.key == pg.K_KP3 or event.key == pg.K_KP4 or event.key == pg.K_KP5:
        return True
    elif event.key == pg.K_KP6 or event.key == pg.K_KP7 or event.key == pg.K_KP8 or event.key == pg.K_KP9 or event.key == pg.K_KP0:
        return True
    else:
        return False