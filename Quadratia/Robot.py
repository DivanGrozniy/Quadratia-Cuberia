import pygame as pg
from GameField import *

DEFAULT_ORIENTATION = 0 #up
DEFAULT_WALL_CHECK = False

RENDER_SCALE = 0.8

class Robot:
    def __init__(self, screen: pg.surface.Surface, gamefield: GameField):
        self.screen: pg.surface.Surface = screen
        self.screen_rect: pg.rect.Rect = screen.get_rect()
        self.isClickedLMB: bool = False
        self.isClickedRMB: bool = False
        self.isClickedMMB: bool = False


        self.icons: list[pg.surface.Surface] = [pg.image.load('Icons/robot_up.png')] * 4
        self.icons[0] = pg.image.load('Icons/robot_up.png')
        self.icons[1] = pg.image.load('Icons/robot_right.png')
        self.icons[2] = pg.image.load('Icons/robot_down.png')
        self.icons[3] = pg.image.load('Icons/robot_left.png')

        self.image: pg.surface.Surface = self.icons[0]
        self.rect: pg.rect.Rect = self.image.get_rect()

        self.gamefield: GameField = gamefield
        self.Xsize: int = gamefield.get_Xsize()
        self.Ysize: int = gamefield.get_Ysize()
        self.tile_size: int = gamefield.tile_size

        self.x: int = 0
        self.y: int = 0

        self.orientation: int = DEFAULT_ORIENTATION

    def set_FieldSize(self):
        self.Xsize = self.gamefield.get_Xsize()
        self.Ysize = self.gamefield.get_Ysize()

    def set_image(self, i):
        self.image = self.icons[i]

    def set_gamefield(self, new_gf: GameField):
        self.gamefield = new_gf
        self.Xsize: int = new_gf.get_Xsize()
        self.Ysize: int = new_gf.get_Ysize()
        self.tile_size: int = new_gf.tile_size

        self.x = min(self.x, self.Xsize-1)
        self.y = min(self.y, self.Ysize-1)


    #BOOL MARKING
    def MarkTile(self, gamefield: GameField):
        j = self.x
        i = self.y
        
        gamefield.Tiles[i * self.Xsize + j].MarkTile()
        self.gamefield = gamefield
        print("ROBOT: Marked tile [" + str(j) + "," + str(i) + "]")

    def CleanTile(self, gamefield: GameField):
        j = self.x
        i = self.y

        gamefield.Tiles[i * self.Xsize + j].CleanTile()
        self.gamefield = gamefield
        print("ROBOT: Cleaned tile [" + str(j) + "," + str(i) + "]")

    def MarkWall(self, gamefield: GameField, border_check: bool = False):
        j = self.x
        i = self.y
        if border_check and (not self.WallCheck()):
            print("ROBOT: Cannot mark wall ahead")
            return

        gamefield.Tiles[i * self.Xsize + j].MarkWall(self.orientation)
        if self.orientation == 0: 
            #Look up
            if self.y != self.Ysize - 1: #world border
                i += 1
                gamefield.Tiles[i * self.Xsize + j].MarkWall(self.orientation + 2)
                i -= 1
        elif self.orientation == 1:
            #Look right
            if self.x != self.Xsize - 1: #world border
                j += 1
                gamefield.Tiles[i * self.Xsize + j].MarkWall(self.orientation + 2)
                j -= 1
        elif self.orientation == 2:
            #Look down
            if self.y != 0: #world border
                i -= 1
                gamefield.Tiles[i * self.Xsize + j].MarkWall(self.orientation + 2)
                i += 1
        elif self.orientation == 3:
            #Look left
            if self.x != 0: #world border
                j -= 1
                gamefield.Tiles[i * self.Xsize + j].MarkWall(self.orientation + 2)
                j += 1

        self.gamefield = gamefield
        print("ROBOT: Marked wall [" + str(j) + "," + str(i) + "], orientation = " + str(self.orientation))

    def CleanWall(self, gamefield: GameField, border_check: bool = False):
        j = self.x
        i = self.y
        if border_check and (not self.WallCheck()):
            print("ROBOT: Cannot clean wall ahead")
            return

        if not gamefield.Tiles[i * self.Xsize + j].WallMark[self.orientation]:
            return

        gamefield.Tiles[i * self.Xsize + j].CleanWall(self.orientation)
        if self.orientation == 0: 
            #Look up
            if self.y != self.Ysize - 1: #world border
                i += 1
                gamefield.Tiles[i * self.Xsize + j].CleanWall(self.orientation + 2)
        elif self.orientation == 1:
            #Look right
            if self.x != self.Xsize - 1: #world border
                j += 1
                gamefield.Tiles[i * self.Xsize + j].CleanWall(self.orientation + 2)
        elif self.orientation == 2:
            #Look down
            if self.y != 0: #world border
                i -= 1
                gamefield.Tiles[i * self.Xsize + j].CleanWall(self.orientation + 2)
                i += 1
        elif self.orientation == 3:
            #Look left
            if self.x != 0: #world border
                j -= 1
                gamefield.Tiles[i * self.Xsize + j].CleanWall(self.orientation + 2)
                j += 1

        self.gamefield = gamefield
        print("ROBOT: Cleaned wall [" + str(j) + "," + str(i) + "], orientation = " + str(self.orientation))

    def BoolCheckTileMark(self) -> bool:
        j = self.x
        i = self.y
        return self.gamefield.Tiles[i * self.Xsize + j].Mark

    def BoolCheckTileWallMark(self) -> bool:
        j = self.x
        i = self.y
        return self.gamefield.Tiles[i * self.Xsize + j].WallMark[self.orientation]

    #VALUE MARKING
    def MarkTileWithValue(self, gamefield: GameField, value: int, x_coord: int = -100, y_coord: int = -100):
        if x_coord == -100 or y_coord == -100:
            j = self.x
            i = self.y
        else:
            j = x_coord
            i = y_coord
        
        gamefield.Tiles[i * self.Xsize + j].MarkTileWithValue(value)
        self.gamefield = gamefield
        print("ROBOT: Marked tile [" + str(j) + "," + str(i) + "] with value " + str(value))

    def CleanTileWithValue(self, gamefield: GameField, x_coord: int = -100, y_coord: int = -100):
        if x_coord == -100 or y_coord == -100:
            j = self.x
            i = self.y
        else:
            j = x_coord
            i = y_coord
        
        gamefield.Tiles[i * self.Xsize + j].CleanTileWithValue()
        self.gamefield = gamefield
        print("ROBOT: Cleaned tile [" + str(j) + "," + str(i) + "] with value")

    def MarkWallWithValue(self, gamefield: GameField, value: int, x_coord: int = -100, y_coord: int = -100, dx: int = 0, dy: int = 0, border_check: bool = False):
        if x_coord == -100 or y_coord == -100 or (abs(dx) + abs(dy) != 1):
            j = self.x
            i = self.y
            ori = self.orientation
        else:
            j = x_coord
            i = y_coord
            if dx:
                ori = dx % 4
            if dy:
                ori = (dy - 1) % 4

        if border_check and (not self.WallCheck()):
            print("ROBOT: Cannot mark wall ahead")
            return

        gamefield.Tiles[i * self.Xsize + j].MarkWallWithValue(ori, value)
        if ori == 0: 
            #Look up
            if self.y != self.Ysize - 1: #world border
                i += 1
                gamefield.Tiles[i * self.Xsize + j].MarkWallWithValue(ori + 2, -999)
                i -= 1
        elif ori == 1:
            #Look right
            if self.x != self.Xsize - 1: #world border
                j += 1
                gamefield.Tiles[i * self.Xsize + j].MarkWallWithValue(ori + 2, -999)
                j -= 1
        elif ori == 2:
            #Look down
            if self.y != 0: #world border
                i -=1
                gamefield.Tiles[i * self.Xsize + j].MarkWallWithValue(ori + 2, -999)
                i += 1
        elif ori == 3:
            #Look left
            if self.x != 0: #world border
                j -= 1
                gamefield.Tiles[i * self.Xsize + j].MarkWallWithValue(ori + 2, -999)
                j += 1

        self.gamefield = gamefield
        print("ROBOT: Marked wall [" + str(j) + "," + str(i) + "], orientation = " + str(self.orientation))

    def CleanWallWithValue(self, gamefield: GameField, x_coord: int = -100, y_coord: int = -100, dx: int = 0, dy: int = 0, border_check: bool = False):
        if x_coord == -100 or y_coord == -100 or (abs(dx) + abs(dy) != 1):
            j = self.x
            i = self.y
            ori = self.orientation
        else:
            j = x_coord
            i = y_coord
            if dx:
                ori = dx % 4
            if dy:
                ori = (dy - 1) % 4

        if border_check and (not self.WallCheck()):
            print("ROBOT: Cannot clean wall ahead")
            return

        if not gamefield.Tiles[i * self.Xsize + j].WallMarkValueFlag[ori]:
            return

        gamefield.Tiles[i * self.Xsize + j].CleanWallWithValue(ori)
        if ori == 0: 
            #Look up
            if self.y != self.Ysize - 1: #world border
                i += 1
                gamefield.Tiles[i * self.Xsize + j].CleanWallWithValue(ori + 2)
        elif ori == 1:
            #Look right
            if self.x != self.Xsize - 1: #world border
                j += 1
                gamefield.Tiles[i * self.Xsize + j].CleanWallWithValue(ori + 2)
        elif ori == 2:
            #Look down
            if self.y != 0: #world border
                i -= 1
                gamefield.Tiles[i * self.Xsize + j].CleanWallWithValue(ori + 2)
                i += 1
        elif ori == 3:
            #Look left
            if self.x != 0: #world border
                j -= 1
                gamefield.Tiles[i * self.Xsize + j].CleanWallWithValue(ori + 2)
                j += 1

        self.gamefield = gamefield
        print("ROBOT: Cleaned wall [" + str(j) + "," + str(i) + "], orientation = " + str(self.orientation))

    def ValueCheckTileMark(self, x_coord: int = -100, y_coord: int = -100):
        if x_coord == -100 or y_coord == -100:
            j = self.x
            i = self.y
        else:
            j = x_coord
            i = y_coord

        if self.gamefield.Tiles[i * self.Xsize + j].MarkValueFlag:
            return self.gamefield.Tiles[i * self.Xsize + j].MarkValue
        else:
            return False

    def ValueCheckTileWallMark(self, x_coord: int = -100, y_coord: int = -100, dx: int = 0, dy: int = 0):
        if x_coord == -100 or y_coord == -100 or (abs(dx) + abs(dy) != 1):
            j = self.x
            i = self.y
            ori = self.orientation
        else:
            j = x_coord
            i = y_coord
            if dx:
                ori = dx % 4
            if dy:
                ori = (dy - 1) % 4

        if self.gamefield.Tiles[i * self.Xsize + j].WallMarkValueFlag[ori]:
            return self.gamefield.Tiles[i * self.Xsize + j].WallMarkValue[ori]
        else:
            return False

    #BORDER CHECKS
    def CheckTileFigure(self, x: int, y: int):
        if x < 0 or x >= self.Xsize or y < 0 or y >= self.Ysize:
            return False

        return self.gamefield.Tiles[y * self.Xsize + x].isFigure

    def WorldBorderCheck(self) -> bool:
        if self.orientation == 0: 
            #Look up
            return self.y == self.Ysize - 1

        elif self.orientation == 1:
            #Look right
            return self.x == self.Xsize - 1

        elif self.orientation == 2:
            #Look down
            return self.y == 0

        elif self.orientation == 3:
            #Look left
            return self.x == 0

    def WallCheck(self) -> bool:
        if self.orientation == 0: 
            #Look up
            if self.y == self.Ysize - 1: #world border
                return True
            else:
                return not self.CheckTileFigure(self.x, self.y + 1)

        elif self.orientation == 1:
            #Look right
            if self.x == self.Xsize - 1: #world border
                return True
            else:
                return not self.CheckTileFigure(self.x + 1, self.y)

        elif self.orientation == 2:
            #Look down
            if self.y == 0: #world border
                return True
            else:
                return not self.CheckTileFigure(self.x, self.y - 1)

        elif self.orientation == 3:
            #Look left
            if self.x == 0: #world border
                return True
            else:
                return not self.CheckTileFigure(self.x - 1, self.y)

    


    #MOVEMENT
    def Step(self, b_check: bool = DEFAULT_WALL_CHECK):
        if self.orientation == 0:
            self.move_up(b_check)
        elif self.orientation == 1:
            self.move_right(b_check)
        elif self.orientation == 2:
            self.move_down(b_check)
        elif self.orientation == 3:
            self.move_left(b_check)

    def TurnLeft(self):
        self.orientation = (self.orientation - 1) % 4
        self.set_image(self.orientation)
    def TurnRight(self):
        self.orientation = (self.orientation + 1) % 4
        self.set_image(self.orientation)
    def ResetOrientation(self):
        self.orientation = DEFAULT_ORIENTATION
            
    def move_right(self, border_check: bool = DEFAULT_WALL_CHECK):
        self.orientation = 1
        self.set_image(self.orientation)
        if (border_check and self.WallCheck()) or self.WorldBorderCheck():
            #WALL AHEAD, CANNOT MOVE
            return
        
        self.x += 1    

    def move_left(self, border_check: bool = DEFAULT_WALL_CHECK):
        self.orientation = 3
        self.set_image(self.orientation)
        if (border_check and self.WallCheck()) or self.WorldBorderCheck():
            #WALL AHEAD, CANNOT MOVE
            return
        
        self.x -= 1

    def move_up(self, border_check: bool = DEFAULT_WALL_CHECK):
        self.orientation = 0
        self.set_image(self.orientation)
        if (border_check and self.WallCheck()) or self.WorldBorderCheck():
            #WALL AHEAD, CANNOT MOVE
            return

        self.y += 1

    def move_down(self, border_check: bool = DEFAULT_WALL_CHECK):
        self.orientation = 2
        self.set_image(self.orientation)
        if (border_check and self.WallCheck()) or self.WorldBorderCheck():
            #WALL AHEAD, CANNOT MOVE
            return
        
        self.y -=1

    def render(self):
        #redline_width = 4
        #ts = self.tile_size - redline_width

        self.image = pg.transform.scale(self.image, (self.tile_size * RENDER_SCALE, self.tile_size * RENDER_SCALE))
        self.rect = self.image.get_rect()

        self.screen.fill((0,0,0,0))

        #pg.draw.polygon(self.image, (255, 0, 0), [[0, 0], [ts, 0], [ts, ts], [0, ts]], redline_width)
        self.rect.center = self.gamefield.Tiles[self.y * self.Xsize + self.x].rect.center
        
        self.screen.blit(self.image, self.rect)