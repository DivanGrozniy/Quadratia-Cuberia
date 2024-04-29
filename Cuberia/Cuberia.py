import pygame as pg
import moderngl as mgl
import sys
import random

from camera import Camera

from Cube import *
from GameField3D import *
from Robot3D import *
from Editor3DFunctions import *

SCREEN_SIZE_DEFAULT = [1200, 700]
SCREEN_NAME_DEFAULT = "Cuberia"

AXES_WIDTH = 5

LEVELS_DIR = "Levels3D/"

class CuberiaEngine:
    def __init__(self, screen_size = SCREEN_SIZE_DEFAULT, screen_name = SCREEN_NAME_DEFAULT, run_type = "EDITOR"):
        # init pygame modules
        pg.init()
        # window size and name
        self.screen_size = screen_size
        self.screen_name = screen_name
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.screen_size, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption(self.screen_name)

        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw'

        #self.ctx.enable(flags = mgl.DEPTH_TEST)
        self.ctx.enable(flags = mgl.CULL_FACE)
        self.ctx.enable(flags = mgl.BLEND)

        # create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        
        self.camera = Camera(self)
        self.camera.position = glm.vec3([12, 8, 10])
        self.camera.yaw = -155
        self.camera.pitch = -17



        self.ctx.line_width = AXES_WIDTH
        
        self.run_type = run_type

        self.Field: GameField3D = GameField3D(self)
        #Figure = [0, 1, 2, 4, 5, 7, 15]
        #for i in Figure:
        #    self.Field.Cubes[i].isFigure = True

        self.Vertun: Robot3D = Robot3D(self, self.Field)

    def get_json_filename(self, text) -> str:
        if text == "":
            return text
        
        if len(text) > 5 and text[-5:] == ".json":
            return LEVELS_DIR + text
        else:
            return LEVELS_DIR + text + ".json" 

    def check_events(self) -> bool:
        if self.run_type == "DEBUG":
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    return False

                elif event.type == pg.KEYDOWN and event.key == pg.K_1:
                    self.Vertun.MarkTile(self.Field)
                elif event.type == pg.KEYDOWN and event.key == pg.K_2:
                    self.Vertun.CleanTile(self.Field)
                elif event.type == pg.KEYDOWN and event.key == pg.K_3:
                    self.Vertun.MarkWall(self.Field)
                elif event.type == pg.KEYDOWN and event.key == pg.K_4:
                    self.Vertun.CleanWall(self.Field)

                elif event.type == pg.KEYDOWN and event.key == pg.K_5:
                    self.Vertun.MarkTileWithValue(self.Field, random.randint(0, 100))
                elif event.type == pg.KEYDOWN and event.key == pg.K_6:
                    self.Vertun.CleanTileWithValue(self.Field)
                elif event.type == pg.KEYDOWN and event.key == pg.K_7:
                    self.Vertun.MarkWallWithValue(self.Field, random.randint(0, 100))
                elif event.type == pg.KEYDOWN and event.key == pg.K_8:
                    self.Vertun.CleanWallWithValue(self.Field)
                elif event.type == pg.KEYDOWN and event.key == pg.K_9:
                    v = self.Vertun.ValueCheckTileMark()
                    print("Tile ValueMark == " + str(v))
                elif event.type == pg.KEYDOWN and event.key == pg.K_0:
                    v = self.Vertun.ValueCheckTileWallMark()
                    print("Wall ValueMark == " + str(v))

            
                #ROBOT MOVEMENT
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP5:
                    self.Vertun.Step()
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP4:
                    self.Vertun.TurnLeft()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP6:
                    self.Vertun.TurnRight()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP8:
                    self.Vertun.TurnUp()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP2:
                    self.Vertun.TurnDown()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP7:
                    self.Vertun.RotateLeft()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP9:
                    self.Vertun.RotateRight()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP0:
                    self.Vertun.ResetOrientation()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))

            
        if self.run_type == "EDITOR":
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    return False

                #CHANGE GRID SIZE
                elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                    nx = input("Input new XSize: ")
                    if nx == "":
                        print("CANCEL: change grid size")
                        continue

                    ny = input("Input new YSize: ")
                    if ny == "":
                        print("CANCEL: change grid size")
                        continue

                    nz = input("Input new ZSize: ")
                    if nz == "":
                        print("CANCEL: change grid size")
                        continue

                    self.Field, self.Vertun = SetGameFieldSize(self.Field, self.Vertun, int(nx), int(ny), int(nz))


                #MARKING
                elif event.type == pg.KEYDOWN and event.key == pg.K_f:
                    self.Field = ToggleFigureTile(self.Field, self.Vertun.x, self.Vertun.y, self.Vertun.z)
                    self.Vertun.set_gamefield(self.Field)

                elif event.type == pg.KEYDOWN and event.key == pg.K_1:
                    self.Field = ToggleMarkTile(self.Field, self.Vertun.x, self.Vertun.y, self.Vertun.z)
                    self.Vertun.set_gamefield(self.Field)

                elif event.type == pg.KEYDOWN and event.key == pg.K_2:
                    self.Field = ToggleWallMark(self.Field, self.Vertun.x, self.Vertun.y, self.Vertun.z, self.Vertun.eyes)
                    self.Vertun.set_gamefield(self.Field)

                elif event.type == pg.KEYDOWN and event.key == pg.K_3:
                    if self.Vertun.ValueCheckTileMark() == False:
                        value = input("Input integer value for Tile Mark: ")
                        if value != "":  
                            self.Vertun.MarkTileWithValue(self.Field, int(value))
                    else:
                        self.Vertun.CleanTileWithValue(self.Field)

                elif event.type == pg.KEYDOWN and event.key == pg.K_4:
                    if self.Vertun.ValueCheckTileWallMark() == False:
                        value = input("Input integer value for Wall Mark: ")
                        if value != "":
                            self.Vertun.MarkWallWithValue(self.Field, int(value))
                    else:
                        self.Vertun.CleanWallWithValue(self.Field)

                elif event.type == pg.KEYDOWN and event.key == pg.K_0:
                    print("Tile ValueMark == " + str(self.Vertun.ValueCheckTileMark()))
                    print("Wall ValueMark == " + str(self.Vertun.ValueCheckTileWallMark()))

                
                


                #SAVE/OPEN LEVEL
                elif event.type == pg.KEYDOWN and event.key == pg.K_i:
                    filename = self.get_json_filename(input("Enter filename for SAVING config: "))
                    if filename == "":
                        print("CANNOT SAVE CONFIG: EMPY FILENAME")
                    else:
                        print("SAVING CONFIG INTO " + filename)
                        SaveLevel(self.Field, self.Vertun, filename)

                elif event.type == pg.KEYDOWN and event.key == pg.K_l:
                    filename = self.get_json_filename(input("Enter filename for LOADING config: "))
                    if filename == "":
                        print("CANNOT LOAD CONFIG: EMPTY FILENAME")
                    else:
                        print("LOADING CONFIG FROM " + filename)
                        self.Field, self.Vertun = LoadLevel(self.Field, self.Vertun, filename)

                elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                    GetFigureTiles(self.Field)
                    GetMarkedTiles(self.Field)
                    GetMarkedWalls(self.Field)
                    GetValueMarkedTiles(self.Field)
                    GetValueMarkedWalls(self.Field)
                
                elif event.type == pg.KEYDOWN and event.key == pg.K_k:
                    print("Camera pos: " + str(self.camera.position))
                    print("Camera angles: yaw == " + str(self.camera.yaw) + ", pitch == " + str(self.camera.pitch))

            
                #ROBOT MOVEMENT
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP5:
                    self.Vertun.Step()
                    print("Robot coordinates: [" + str(self.Vertun.x) + ", " + str(self.Vertun.y) + ", " + str(self.Vertun.z) + "]")
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP4:
                    self.Vertun.TurnLeft()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP6:
                    self.Vertun.TurnRight()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP8:
                    self.Vertun.TurnUp()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP2:
                    self.Vertun.TurnDown()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP7:
                    self.Vertun.RotateLeft()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP9:
                    self.Vertun.RotateRight()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))
                elif event.type == pg.KEYDOWN and event.key == pg.K_KP0:
                    self.Vertun.ResetOrientation()
                    print("Robot ori: eyes == " + str(self.Vertun.eyes) + ", head == " + str(self.Vertun.head))


        return True
                

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.Field.render()
        self.Vertun.render()
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        running: bool = True
        while running:
            self.get_time()
            
            self.camera.update()
            running = self.check_events()

            self.render()
            self.delta_time = self.clock.tick(60)

        pg.quit()


if __name__ == '__main__':
    random.seed(2024)

    app = CuberiaEngine()
    app.run()
