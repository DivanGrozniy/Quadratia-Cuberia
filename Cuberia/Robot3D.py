import pygame as pg
import moderngl as mgl
import numpy as np
import glm
import random

from GameField3D import *

DEFAULT_ROBOT_COLOR = [0.5, 0.2, 0.7]
EYES_ROBOT_COLOR = [0.7, 0, 0]
HEAD_ROBOT_COLOR = [0, 0.7, 0]

xp = 1
xm = 4
yp = 5
ym = 0
zp = 2
zm = 3

DEFAULT_EYES = xp
DEFAULT_HEAD = yp
DEFAULT_WALL_CHECK = False

class Robot3D:
    def __init__(self, app, gamefield: GameField3D, pos = [0, 0, 0], rot = [0, 0, 0], scale = [0.5, 0.5, 0.5]):
        self.app = app
        self.ctx = app.ctx

        self.gamefield: GameField3D = gamefield
        self.Xsize: int = gamefield.get_Xsize()
        self.Ysize: int = gamefield.get_Ysize()
        self.Zsize: int = gamefield.get_Zsize()
        self.tile_size: int = gamefield.tile_size

        self.x: int = 0
        self.y: int = 0
        self.z: int = 0

        self.eyes: int = DEFAULT_EYES
        self.head: int = DEFAULT_HEAD

        self.polygons_vbo = self.get_polygons_vbo()
        self.polygons_shader_program = self.get_shader_program("robot")
        self.polygons_vao = self.get_polygons_vao()
        
        self.camera = self.app.camera

        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_martix()

        self.polygons_update()

    #VBO    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for poly_or_line in indices for ind in poly_or_line]
        return np.array(data, dtype='f4')

    def get_polygons_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -0.5,  0.5), (0.75,  0.5,  0.25), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -0.5, -0.5), (0.75, 0.5, -0.25)]

        polygons_indices = [(0, 6, 1), (0, 5, 6),
                            (1, 7, 2), (1, 6, 7), #eyes
                            (0, 2, 3), (0, 1, 2),
                            (6, 5, 4), (4, 7, 6),
                            (3, 4, 5), (3, 5, 0),
                            (3, 7, 4), (3, 2, 7) #head
                           ]

        polygons_color = []
        for id in range(6):
            if id == 1: #eyes
                color = EYES_ROBOT_COLOR
            elif id == 5: #head
                color = HEAD_ROBOT_COLOR
            else:
                color = DEFAULT_ROBOT_COLOR
                #color = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]

            for _ in range(3 * 2):
                polygons_color.append(color)


        polygons_color = np.array(polygons_color, dtype='f4')

        vertex_data = self.get_data(vertices, polygons_indices)

        vertex_data = np.hstack([vertex_data, polygons_color])

        return vertex_data

    def get_polygons_vbo(self):
        vd = self.get_polygons_vertex_data()
        poly_vbo = self.ctx.buffer(vd)
        return poly_vbo


    #SHADERS
    def get_shader_program(self, shader_name: str):
        with open(SHADERS_DIR + shader_name + ".vert") as file:
            v_sh = file.read()

        with open(SHADERS_DIR + shader_name + ".frag") as file:
            f_sh = file.read()

        program = self.ctx.program(vertex_shader = v_sh, fragment_shader = f_sh)
        return program

    #VAO
    def get_polygons_vao(self):
        poly_vao = self.ctx.vertex_array(self.polygons_shader_program, [(self.polygons_vbo, "3f 3f", "in_vertex_pos", "in_polygons_color")])
        return poly_vao

    #RENDER
    def get_model_martix(self):
        m_model = glm.mat4()

        # translate
        m_model = glm.translate(m_model, self.pos)

        # rotate
        m_model = glm.rotate(m_model, self.rot[0], glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot[1], glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot[2], glm.vec3(0, 0, 1))

        # scale
        m_model = glm.scale(m_model, self.scale)

        return m_model

    def polygons_update(self):
        self.polygons_shader_program['m_proj'].write(self.camera.m_proj)
        self.polygons_shader_program['m_view'].write(self.camera.m_view)
        self.polygons_shader_program['m_model'].write(self.m_model)

    def render(self):
        self.m_model = self.get_model_martix()
        self.polygons_update()
        self.polygons_vao.render(mgl.TRIANGLES)

    def destroy(self):
        self.polygons_vbo.release()
        self.polygons_shader_program.release()
        self.polygons_vao.release()


    def set_FieldSize(self):
        self.Xsize = self.gamefield.get_Xsize()
        self.Ysize = self.gamefield.get_Ysize()
        self.Zsize: int = gamefield.get_Zsize()

    def set_gamefield(self, new_gf: GameField3D):
        self.gamefield = new_gf
        self.Xsize: int = new_gf.get_Xsize()
        self.Ysize: int = new_gf.get_Ysize()
        self.Zsize: int = new_gf.get_Zsize()
        self.tile_size: int = new_gf.tile_size

        self.x = min(self.x, self.Xsize-1)
        self.y = min(self.y, self.Ysize-1)
        self.z = min(self.z, self.Zsize-1)



    #BORDER CHECKS
    def CheckTileFigure(self, x: int, y: int, z: int) -> bool:
        if x < 0 or x >= self.Xsize or y < 0 or y >= self.Ysize or z < 0 or z >= self.Zsize:
            return False

        coord = self.gamefield.get_coord(x, y, z)
        return self.gamefield.Cubes[coord].isFigure

    def WorldBorderCheck(self) -> bool:
        if self.eyes == xp: 
            return self.x == self.Xsize - 1
        elif self.eyes == xm:
            return self.x == 0

        elif self.eyes == yp: 
            return self.y == self.Ysize - 1
        elif self.eyes == ym:
            return self.y == 0

        elif self.eyes == zp: 
            return self.z == self.Zsize - 1
        elif self.eyes == zm:
            return self.z == 0

    def WallCheck(self) -> bool:
        if self.WorldBorderCheck():
            return True

        if self.eyes == xp: 
            return not self.CheckTileFigure(self.x + 1, self.y, self.z)
        elif self.eyes == xm:
            return not self.CheckTileFigure(self.x - 1, self.y, self.z)

        elif self.eyes == yp: 
            return not self.CheckTileFigure(self.x, self.y + 1, self.z)
        elif self.eyes == ym:
            return not self.CheckTileFigure(self.x, self.y - 1, self.z)

        elif self.eyes == zp: 
            return not self.CheckTileFigure(self.x, self.y, self.z + 1)
        elif self.eyes == zm:
            return not self.CheckTileFigure(self.x, self.y, self.z - 1)



    #MOVEMENT
    def Step(self, border_check: bool = DEFAULT_WALL_CHECK):
        if (border_check and self.WallCheck()) or self.WorldBorderCheck():
            #WALL AHEAD, CANNOT MOVE
            return

        if self.eyes == xp: 
            self.x += 1    
        elif self.eyes == xm:
            self.x -= 1

        elif self.eyes == yp: 
            self.y += 1
        elif self.eyes == ym:
            self.y -= 1

        elif self.eyes == zp: 
            self.z += 1
        elif self.eyes == zm:
            self.z -= 1

        ts = self.tile_size
        self.pos = [ts*self.x, ts*self.y, ts*self.z]

    def TurnRight(self):
        if self.head == xp: 
            eye_walls = [ym, zp, yp, zm]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i+1) % 4]
                    break

            self.rot[0] -= glm.radians(90)
        elif self.head == xm:
            eye_walls = [ym, zp, yp, zm]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i-1) % 4]
                    break

            self.rot[0] += glm.radians(90)

        elif self.head == yp: 
            eye_walls = [xp, zp, xm, zm]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i+1) % 4]
                    break

            self.rot[1] -= glm.radians(90)
        elif self.head == ym:
            eye_walls = [xp, zp, xm, zm]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i-1) % 4]
                    break

            self.rot[1] += glm.radians(90)

        elif self.head == zp: 
            eye_walls = [xp, ym, xm, yp]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i+1) % 4]
                    break

            self.rot[2] -= glm.radians(90)      #BUGGED
        elif self.head == zm:
            eye_walls = [xp, ym, xm, yp]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i-1) % 4]
                    break

            self.rot[2] += glm.radians(90)      #BUGGED

    def TurnLeft(self):
        if self.head == xp: 
            eye_walls = [ym, zp, yp, zm]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i-1) % 4]
                    break

            self.rot[0] += glm.radians(90)
        elif self.head == xm:
            eye_walls = [ym, zp, yp, zm]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i+1) % 4]
                    break

            self.rot[0] -= glm.radians(90)

        elif self.head == yp: 
            eye_walls = [xp, zp, xm, zm]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i-1) % 4]
                    break

            self.rot[1] += glm.radians(90)
        elif self.head == ym:
            eye_walls = [xp, zp, xm, zm]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i+1) % 4]
                    break

            self.rot[1] -= glm.radians(90)

        elif self.head == zp: 
            eye_walls = [xp, ym, xm, yp]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i-1) % 4]
                    break

            self.rot[2] += glm.radians(90)      #BUGGED
        elif self.head == zm:
            eye_walls = [xp, ym, xm, yp]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i+1) % 4]
                    break

            self.rot[2] -= glm.radians(90)      #BUGGED

    def TurnUp(self):
        old_eyes = self.eyes
        old_head = self.head

        self.eyes = old_head
        self.head = abs(5 - old_eyes)

        self.rot[2] += glm.radians(90)

    def TurnDown(self):
        old_eyes = self.eyes
        old_head = self.head

        self.eyes = abs(5 - old_head)
        self.head = old_eyes

        self.rot[2] -= glm.radians(90)

    def RotateRight(self):
        if self.eyes == xp: 
            head_walls = [yp, zp, ym, zm]
            for i in range(4):
                if self.head == head_walls[i]:
                    self.head = head_walls[(i+1) % 4]
                    break

            self.rot[0] += glm.radians(90)
        elif self.eyes == xm:
            head_walls = [yp, zp, ym, zm]
            for i in range(4):
                if self.head == head_walls[i]:
                    self.head = head_walls[(i-1) % 4]
                    break

            self.rot[0] -= glm.radians(90)

        elif self.eyes == yp: 
            head_walls = [xp, zm, xm, zp]
            for i in range(4):
                if self.head == head_walls[i]:
                    self.head = head_walls[(i+1) % 4]
                    break

            self.rot[1] += glm.radians(90)
        elif self.eyes == ym:
            head_walls = [xp, zm, xm, zp]
            for i in range(4):
                if self.head == head_walls[i]:
                    self.head = head_walls[(i-1) % 4]
                    break

            self.rot[1] -= glm.radians(90)

        elif self.eyes == zp: 
            eye_walls = [xm, ym, xp, yp]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i+1) % 4]
                    break

            self.rot[2] += glm.radians(90)      #BUGGED
        elif self.eyes == zm:
            eye_walls = [xm, ym, xp, yp]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i-1) % 4]
                    break

            self.rot[2] -= glm.radians(90)      #BUGGED

    def RotateLeft(self):
        if self.eyes == xp: 
            head_walls = [yp, zp, ym, zm]
            for i in range(4):
                if self.head == head_walls[i]:
                    self.head = head_walls[(i-1) % 4]
                    break

            self.rot[0] -= glm.radians(90)
        elif self.eyes == xm:
            head_walls = [yp, zp, ym, zm]
            for i in range(4):
                if self.head == head_walls[i]:
                    self.head = head_walls[(i+1) % 4]
                    break

            self.rot[0] += glm.radians(90)

        elif self.eyes == yp: 
            head_walls = [xp, zm, xm, zp]
            for i in range(4):
                if self.head == head_walls[i]:
                    self.head = head_walls[(i-1) % 4]
                    break

            self.rot[1] -= glm.radians(90)
        elif self.eyes == ym:
            head_walls = [xp, zm, xm, zp]
            for i in range(4):
                if self.head == head_walls[i]:
                    self.head = head_walls[(i+1) % 4]
                    break

            self.rot[1] += glm.radians(90)

        elif self.eyes == zp: 
            eye_walls = [xm, ym, xp, yp]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i-1) % 4]
                    break

            self.rot[2] -= glm.radians(90)      #BUGGED
        elif self.eyes == zm:
            eye_walls = [xm, ym, xp, yp]
            for i in range(4):
                if self.eyes == eye_walls[i]:
                    self.eyes = eye_walls[(i+1) % 4]
                    break

            self.rot[2] += glm.radians(90)      #BUGGED

    def ResetOrientation(self):
        self.eyes = xp
        self.head = yp

        rot = [0, 0, 0]
        self.rot = glm.vec3([glm.radians(a) for a in rot])


    #BOOL MARKING
    def MarkTile(self, gamefield: GameField3D):
        i = self.x
        j = self.y
        k = self.z
        coord = gamefield.get_coord(i, j, k)
        
        gamefield.Cubes[coord].MarkTile()
        self.gamefield = gamefield
        print("ROBOT: Marked tile [" + str(i) + "," + str(j) + "," + str(k) + "]")

    def CleanTile(self, gamefield: GameField3D):
        i = self.x
        j = self.y
        k = self.z
        coord = gamefield.get_coord(i, j, k)

        gamefield.Cubes[coord].CleanTile()
        self.gamefield = gamefield
        print("ROBOT: Cleaned tile [" + str(i) + "," + str(j) + "," + str(k) + "]")

    def MarkWall(self, gamefield: GameField3D, border_check: bool = False):
        i = self.x
        j = self.y
        k = self.z
        coord = gamefield.get_coord(i, j, k)

        if border_check and (not self.WallCheck()):
            print("ROBOT: Cannot mark wall ahead")
            return

        gamefield.Cubes[coord].MarkWall(self.eyes)

        self.gamefield = gamefield
        print("ROBOT: Marked wall [" + str(i) + "," + str(j) + "," + str(k) + "], [eyes/head] = " + str(self.eyes) + " " + str(self.head))

    def CleanWall(self, gamefield: GameField3D, border_check: bool = False):
        i = self.x
        j = self.y
        k = self.z
        coord = gamefield.get_coord(i, j, k)

        if border_check and (not self.WallCheck()):
            print("ROBOT: Cannot clean wall ahead")
            return

        if not gamefield.Cubes[coord].WallMark[self.eyes]:
            return

        gamefield.Cubes[coord].CleanWall(self.eyes)

        self.gamefield = gamefield
        print("ROBOT: Cleaned wall [" + str(i) + "," + str(j) + "," + str(k) + "], [eyes/head] = " + str(self.eyes) + " " + str(self.head))

    def BoolCheckTileMark(self) -> bool:
        i = self.x
        j = self.y
        k = self.z
        coord = self.gamefield.get_coord(i, j, k)

        return self.gamefield.Cubes[coord].Mark

    def BoolCheckTileWallMark(self) -> bool:
        i = self.x
        j = self.y
        k = self.z
        coord = self.gamefield.get_coord(i, j, k)

        return self.gamefield.Cubes[coord].WallMark[self.eyes]


    #VALUE MARKING
    def MarkTileWithValue(self, gamefield: GameField3D, value: int, x_coord: int = -100, y_coord: int = -100, z_coord: int = -100):
        if x_coord == -100 or y_coord == -100 or z_coord == -100:
            i = self.x
            j = self.y
            k = self.z
        else:
            i = x_coord
            j = y_coord
            k = z_coord

        coord = gamefield.get_coord(i, j, k)        
        gamefield.Cubes[coord].MarkTileWithValue(value)
        self.gamefield = gamefield

        print("ROBOT: Marked tile [" + str(i) + "," + str(j) + "," + str(k) + "] with value " + str(value))

    def CleanTileWithValue(self, gamefield: GameField3D, x_coord: int = -100, y_coord: int = -100, z_coord: int = -100):
        if x_coord == -100 or y_coord == -100 or z_coord == -100:
            i = self.x
            j = self.y
            k = self.z
        else:
            i = x_coord
            j = y_coord
            k = z_coord

        coord = gamefield.get_coord(i, j, k)        
        gamefield.Cubes[coord].CleanTileWithValue()
        self.gamefield = gamefield

        print("ROBOT: Cleaned tile [" + str(i) + "," + str(j) + "," + str(k) + "] with value")

    def MarkWallWithValue(self, gamefield: GameField3D, value: int, x_coord: int = -100, y_coord: int = -100, z_coord: int = -100, dx: int = 0, dy: int = 0, dz: int = 0, border_check: bool = False):
        if x_coord == -100 or y_coord == -100 or z_coord == -100 or (abs(dx) + abs(dy) + abs(dz) != 1):
            i = self.x
            j = self.y
            k = self.z
            ori = self.eyes
        else:
            i = x_coord
            j = y_coord
            k = z_coord

            if dx == 1:
                ori = xp
            if dx == -1:
                ori = xm
            if dy == 1:
                ori = yp
            if dy == -1:
                ori = ym
            if dz == 1:
                ori = zp
            if dz == -1:
                ori = zm

        coord = gamefield.get_coord(i, j, k)        
        gamefield.Cubes[coord].MarkWallWithValue(ori, value)
        self.gamefield = gamefield

        print("ROBOT: Marked wall [" + str(i) + "," + str(j) + "," + str(k) + "] with value " + str(value) + ", eyes/head == " + str(self.eyes) + "/ " + str(self.head))

    def CleanWallWithValue(self, gamefield: GameField3D, x_coord: int = -100, y_coord: int = -100, z_coord: int = -100, dx: int = 0, dy: int = 0, dz: int = 0, border_check: bool = False):
        if x_coord == -100 or y_coord == -100 or z_coord == -100 or (abs(dx) + abs(dy) + abs(dz) != 1):
            i = self.x
            j = self.y
            k = self.z
            ori = self.eyes
        else:
            i = x_coord
            j = y_coord
            k = z_coord

            if dx == 1:
                ori = xp
            if dx == -1:
                ori = xm
            if dy == 1:
                ori = yp
            if dy == -1:
                ori = ym
            if dz == 1:
                ori = zp
            if dz == -1:
                ori = zm

        coord = gamefield.get_coord(i, j, k)        
        gamefield.Cubes[coord].CleanWallWithValue(self.eyes)
        self.gamefield = gamefield

        print("ROBOT: Cleaned wall [" + str(i) + "," + str(j) + "," + str(k) + "] with value, eyes/head == " + str(self.eyes) + "/ " + str(self.head))

    def ValueCheckTileMark(self, x_coord: int = -100, y_coord: int = -100, z_coord: int = -100):
        if x_coord == -100 or y_coord == -100 or z_coord == -100:
            i = self.x
            j = self.y
            k = self.z
        else:
            i = x_coord
            j = y_coord
            k = z_coord

        coord = self.gamefield.get_coord(i, j, k) 
        if self.gamefield.Cubes[coord].MarkValueFlag:
            return self.gamefield.Cubes[coord].MarkValue
        else:
            return False

    def ValueCheckTileWallMark(self, x_coord: int = -100, y_coord: int = -100, z_coord: int = -100, dx: int = 0, dy: int = 0, dz: int = 0, border_check: bool = False):
        if x_coord == -100 or y_coord == -100 or z_coord == -100 or (abs(dx) + abs(dy) + abs(dz) != 1):
            i = self.x
            j = self.y
            k = self.z
            ori = self.eyes
        else:
            i = x_coord
            j = y_coord
            k = z_coord

            if dx == 1:
                ori = xp
            if dx == -1:
                ori = xm
            if dy == 1:
                ori = yp
            if dy == -1:
                ori = ym
            if dz == 1:
                ori = zp
            if dz == -1:
                ori = zm

        coord = self.gamefield.get_coord(i, j, k)
        if self.gamefield.Cubes[coord].WallMarkValueFlag[ori]:
            return self.gamefield.Cubes[coord].WallMarkValue[ori]
        else:
            return False
