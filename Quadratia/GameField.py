import pygame as pg
import numpy as np

DEFAULT_TILE_SIZE = 100
DEFAULT_XSIZE = 5
DEFAULT_YSIZE = 5

AXIS_FONT_SIZE = 36
AXIS_WIDTH = 3
AXIS_COLOR = [255, 255, 0]

TILE_MARK_FONT_SIZE = 25
TILE_WALL_MARK_FONT_SIZE = 25
TILE_MARK_FONT_COLOR = [0, 0, 0]
TILE_WALL_MARK_FONT_COLOR = [0, 0, 0]

DEFAULT_TILE_COLOR = [255, 255, 255]
DEFAULT_WALL_COLOR = [0, 0, 0]
WALL_WIDTH = 5
FIGURE_TILE_COLOR = [128, 0, 255]

MARKED_TILE_COLOR = [255, 0, 0]
MARKED_WALL_COLOR = [255, 0, 0]
MARKED_WALL_WIDTH = 5
MARK_SIZE_PERCENT = 0.7

VALUE_MARKED_TILE_COLOR = [255, 128, 0]
VALUE_MARKED_WALL_COLOR = [255, 128, 0]
VALUE_MARKED_WALL_WIDTH = 3
VALUE_MARK_SIZE_PERCENT = 0.5

SHIFT = DEFAULT_TILE_SIZE / 4

class GameField:
    def __init__(self, screen: pg.surface.Surface, Xsize: int = DEFAULT_XSIZE, Ysize: int = DEFAULT_YSIZE, auto_recalculate_size: bool = True):
        self.screen: pg.surface.Surface = screen
        self.screen_rect: pg.rect.Rect = screen.get_rect()
        self.Xsize: int = Xsize
        self.Ysize: int = Ysize

        if not pg.font.get_init():
            pg.font.init()
        self.axis_font: pg.font.Font = pg.font.Font(None, AXIS_FONT_SIZE)

        self.Tiles: list[Tile] = [Tile(screen)] * Xsize * Ysize
        self.tile_size: int = DEFAULT_TILE_SIZE

        for i in range(self.Ysize):
            for j in range(self.Xsize):
                self.Tiles[i * self.Xsize + j] = Tile(screen, self.tile_size)

        if auto_recalculate_size:
            self.RecalculateTileSize()
        else:
            self.SetTilesPosition()

    def RecalculateTileSize(self):
        scr_w = self.screen.get_width()
        scr_h = self.screen.get_height()

        new_size = min(scr_w / self.Xsize, scr_h / self.Ysize) * 0.8
        self.tile_size = new_size
        #print("New tile size = " + str(self.tile_size))

        self.SetTileSize(new_size)
        self.SetTilesPosition()

    def SetTileSize(self, new_size: int = DEFAULT_TILE_SIZE):
        for i in range(self.Ysize):
            for j in range(self.Xsize):
                self.Tiles[i * self.Xsize + j].tile_size = new_size
                self.Tiles[i * self.Xsize + j].surf = pg.Surface((new_size, new_size))
                self.Tiles[i * self.Xsize + j].rect = self.Tiles[i * self.Xsize + j].surf.get_rect()

    def SetTileFigure(self, x: int, y: int, flag: bool):
        self.Tiles[y * self.Xsize + x].isFigure = flag

    def SetTilesPosition(self):
        for i in range(self.Ysize):
            for j in range(self.Xsize):
                self.Tiles[i * self.Xsize + j].rect[0] = SHIFT + self.screen.get_rect().x + self.tile_size*j
                self.Tiles[i * self.Xsize + j].rect[1] = SHIFT + self.screen.get_rect().y + self.tile_size*(self.Ysize - 1 - i)
                #print("for [" + str(j) + "," + str(i) + "]" + str(self.Tiles[i * self.Xsize + j].rect))
                
    def render(self):
        self.screen.fill((0,0,0,0))

        for i in range(self.Ysize):
            for j in range(self.Xsize):
                self.Tiles[i * self.Xsize + j].render()
        self.DrawAxes()

    def DrawAxes(self):
        axis_x_len = self.Xsize * self.tile_size
        axis_y_len = self.Ysize * self.tile_size

        axis_x_start = np.array(self.Tiles[0].rect.bottomleft) + np.array([-WALL_WIDTH, WALL_WIDTH])
        axis_x_end = np.array(self.Tiles[self.Xsize - 1].rect.bottomright) + np.array([25, WALL_WIDTH])

        pg.draw.line(self.screen, AXIS_COLOR, axis_x_start, axis_x_end, AXIS_WIDTH)
        pg.draw.line(self.screen, AXIS_COLOR, axis_x_end, axis_x_end + np.array([-10, -10]), AXIS_WIDTH)
        pg.draw.line(self.screen, AXIS_COLOR, axis_x_end, axis_x_end + np.array([-10, 10]), AXIS_WIDTH)

        for j in range(self.Xsize):
            text_pos = axis_x_start + np.array([self.tile_size * 0.5 + self.tile_size * j, AXIS_FONT_SIZE * 0.5])
            self.screen.blit(self.axis_font.render(str(j), True, AXIS_COLOR), text_pos)

        axis_y_start = axis_x_start
        axis_y_end = np.array(self.Tiles[(self.Ysize - 1) * self.Xsize].rect.topleft) + np.array([-WALL_WIDTH, -25])

        pg.draw.line(self.screen, AXIS_COLOR, axis_y_start, axis_y_end, AXIS_WIDTH)
        pg.draw.line(self.screen, AXIS_COLOR, axis_y_end, axis_y_end + np.array([-10, 10]), AXIS_WIDTH)
        pg.draw.line(self.screen, AXIS_COLOR, axis_y_end, axis_y_end + np.array([10, 10]), AXIS_WIDTH)

        for i in range(self.Ysize):
            text_pos = axis_y_start + np.array([-AXIS_FONT_SIZE * 0.5, -self.tile_size * 0.75 - self.tile_size * i])
            self.screen.blit(self.axis_font.render(str(i), True, AXIS_COLOR), text_pos)

    
                    
    def get_Xsize(self):
        return self.Xsize

    def get_Ysize(self):
        return self.Ysize


class Tile:
    def __init__(self, screen: pg.surface.Surface, t_size: int = DEFAULT_TILE_SIZE):
        self.screen: pg.surface.Surface = screen
        self.screen_rect: pg.rect.Rect = screen.get_rect()
        self.isClickedLMB: bool = False
        self.isClickedRMB: bool = False
        self.isClickedMMB: bool = False

        if not pg.font.get_init():
            pg.font.init()
        self.mark_font: pg.font.Font = pg.font.Font(None, TILE_MARK_FONT_SIZE)
        self.wall_mark_font: pg.font.Font = pg.font.Font(None, TILE_WALL_MARK_FONT_SIZE)

        self.tile_size = t_size

        self.surf: pg.surface.Surface = pg.Surface((self.tile_size + WALL_WIDTH/2, self.tile_size + WALL_WIDTH/2))
        self.rect: pg.rect.Rect = self.surf.get_rect()
        self.set_color()

        self.isFigure: bool = False

        self.Mark: bool = False
        self.WallMark: list[bool] = [False] * 4

        self.MarkValueFlag: bool = False
        self.MarkValue: int = -999
        self.WallMarkValueFlag: list[bool] = [False] * 4
        self.WallMarkValue: list[int] = [-999] * 4   

    def set_color(self, new_color: list[int] = DEFAULT_TILE_COLOR):
        self.surf.fill(new_color)

    def set_border_color(self, new_color: list[int] = DEFAULT_WALL_COLOR):
        ts = self.tile_size
        pg.draw.polygon(self.surf, new_color, [[0, 0], [ts, 0], [ts, ts], [0, ts]], WALL_WIDTH)
        
    def set_wall_color(self, wall_id: int, new_color: list[int] = DEFAULT_WALL_COLOR, width: int = WALL_WIDTH):
        ts = self.tile_size
        id = wall_id % 4

        if id == 0:
            #Upper wall
            pg.draw.polygon(self.surf, new_color, [[0, 0], [ts, 0]], width)
        elif id == 1:
            #Right wall
            pg.draw.polygon(self.surf, new_color, [[ts, 0], [ts, ts]], width)
        elif id == 2:
            #Down wall
            pg.draw.polygon(self.surf, new_color, [[0, ts], [ts, ts]], width)
        elif id == 3:
            #Left wall
            pg.draw.polygon(self.surf, new_color, [[0, 0], [0, ts]], width)


    #BOOL MARKING
    def MarkTile(self):
        self.Mark = True

    def CleanTile(self):
        self.Mark = False

    def MarkWall(self, wall_id: int):
        self.WallMark[wall_id % 4] = True

    def CleanWall(self, wall_id: int):
        self.WallMark[wall_id % 4] = False

    #VALUE MARKING
    def MarkTileWithValue(self, value: int):
        self.MarkValueFlag = True
        self.MarkValue = value

        #print("TILE: Marked tile with value " + str(value))

    def CleanTileWithValue(self):
        self.MarkValueFlag = False
        self.MarkValue = -999

    def MarkWallWithValue(self, wall_id: int, value: int):
        self.WallMarkValueFlag[wall_id % 4] = True
        self.WallMarkValue[wall_id % 4] = value

        #print("TILE: Marked tile wall " + str(wall_id % 4) + " with value " + str(value))

    def CleanWallWithValue(self, wall_id: int):
        self.WallMarkValueFlag[wall_id % 4] = False
        self.WallMarkValue[wall_id % 4] = -999

    
        
        
        
        
        
    def render(self):
        #Tile color
        if self.isFigure:
            self.set_color(FIGURE_TILE_COLOR)
        else:
            self.set_color(DEFAULT_TILE_COLOR)

        #Draw black borders
        self.set_border_color()

        #Draw bool tile mark
        if self.Mark:
            ts = self.tile_size * MARK_SIZE_PERCENT
            shift = self.tile_size * (1 - MARK_SIZE_PERCENT) * 0.5

            plgn = [[0, 0], [ts, 0], [ts, ts], [0, ts]]
            sharr = [[shift, shift]] * 4

            plgn = np.array(plgn) + np.array(sharr)
            pg.draw.polygon(self.surf, MARKED_TILE_COLOR, plgn)

        #Draw value tile mark
        if self.MarkValueFlag:
            ts = self.tile_size * VALUE_MARK_SIZE_PERCENT
            shift = self.tile_size * (1 - VALUE_MARK_SIZE_PERCENT) * 0.5

            plgn = [[0, 0], [ts, 0], [ts, ts], [0, ts]]
            sharr = [[shift, shift]] * 4

            plgn = np.array(plgn) + np.array(sharr)

            pg.draw.polygon(self.surf, VALUE_MARKED_TILE_COLOR, plgn)

            text = self.mark_font.render(str(self.MarkValue), True, TILE_MARK_FONT_COLOR)
            text_pos = np.array([self.tile_size / 2, self.tile_size / 2]) + np.array([-text.get_rect().width / 2, -text.get_rect().height / 2])
            self.surf.blit(text, text_pos)

        #Draw bool wall marks
        for ori in range(4):
            if self.WallMark[ori]:
                self.set_wall_color(ori, MARKED_WALL_COLOR, MARKED_WALL_WIDTH)

        #Draw value wall marks
        ts = self.tile_size
        for ori in range(4):
            if self.WallMarkValueFlag[ori]:
                self.set_wall_color(ori, VALUE_MARKED_WALL_COLOR, VALUE_MARKED_WALL_WIDTH)

                if self.WallMarkValue[ori] != -999:
                    text = self.wall_mark_font.render(str(self.WallMarkValue[ori]), True, TILE_WALL_MARK_FONT_COLOR)

                    if ori == 0:
                        #Upper wall
                        text_pos = np.array([ts/2, 0]) + np.array([-text.get_rect().width / 2, text.get_rect().height / 2])
                    elif ori == 1:
                        #Right wall
                        text_pos = np.array([ts, ts/2]) + np.array([-text.get_rect().width, -text.get_rect().height / 2])
                    elif ori == 2:
                        #Down wall
                        text_pos = np.array([ts/2, ts]) + np.array([-text.get_rect().width / 2, -text.get_rect().height])
                    elif ori == 3:
                        #Left wall
                        text_pos = np.array([0, ts/2]) + np.array([text.get_rect().width / 2, -text.get_rect().height / 2])

                    self.surf.blit(text, text_pos)
        
        self.screen.blit(self.surf, self.rect)
    