import pygame as pg
import moderngl as mgl
import numpy as np
import glm

from Cube import *

xp = 1
xm = 4
yp = 5
ym = 0
zp = 2
zm = 3

DEFAULT_XSIZE = 3
DEFAULT_YSIZE = 5
DEFAULT_ZSIZE = 7

RENDER_OFFSET = 0.02

class XYZAxes:
    def __init__(self, app, Xsize: int = DEFAULT_XSIZE, Ysize: int = DEFAULT_YSIZE, Zsize: int = DEFAULT_ZSIZE, 
                 pos = [0, 0, 0], rot = [0, 0, 0], scale = [1, 1, 1]):
        self.app = app
        self.ctx = app.ctx
        
        self.Xsize: int = 2 * Xsize
        self.Ysize: int = 2 * Ysize
        self.Zsize: int = 2 * Zsize

        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("axes")
        self.vao = self.get_vao()


        self.camera = self.app.camera

        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_martix()

    def get_vertex_data(self):
        vertex_data = [(0,0,0), (self.Xsize + 2, 0, 0),
                       (0,0,0), (0, self.Ysize + 2, 0),
                       (0,0,0), (0, 0, self.Zsize + 2)]
        vertex_data = np.array(vertex_data, dtype='f4')

        colors = [(1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1)]
        colors = np.array(colors, dtype='f4')

        vertex_data = np.hstack([vertex_data, colors])

        return vertex_data
        
    def get_vbo(self):
        vd = self.get_vertex_data()
        vbo = self.ctx.buffer(vd)
        return vbo

    def get_shader_program(self, shader_name: str):
        with open(SHADERS_DIR + shader_name + ".vert") as file:
            v_sh = file.read()

        with open(SHADERS_DIR + shader_name + ".frag") as file:
            f_sh = file.read()

        program = self.ctx.program(vertex_shader = v_sh, fragment_shader = f_sh)
        return program
    
    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, "3f 3f", "in_vertex_pos", "in_color")])
        return vao

    def get_model_martix(self):
        m_model = glm.mat4()

        # translate
        m_model = glm.translate(m_model, self.pos)

        # rotate
        m_model = glm.rotate(m_model, self.rot[2], glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot[1], glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot[0], glm.vec3(1, 0, 0))

        # scale
        m_model = glm.scale(m_model, self.scale)

        return m_model

    def update_vao(self, Xsize: int, Ysize: int, Zsize: int):
        self.vbo.release()
        self.vao.release()

        self.Xsize: int = 2 * Xsize
        self.Ysize: int = 2 * Ysize
        self.Zsize: int = 2 * Zsize

        self.vbo = self.get_vbo()
        self.vao = self.get_vao()
    
    def update(self):
        self.m_model = self.get_model_martix()

        self.shader_program['m_proj'].write(self.camera.m_proj)
        self.shader_program['m_view'].write(self.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render(mgl.LINES)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()


class GameField3D:
    def __init__(self, app, Xsize: int = DEFAULT_XSIZE, Ysize: int = DEFAULT_YSIZE, Zsize: int = DEFAULT_ZSIZE):
        self.app = app
        self.ctx = app.ctx

        self.Xsize: int = Xsize
        self.Ysize: int = Ysize
        self.Zsize: int = Zsize

        self.Axes = XYZAxes(app, Xsize, Ysize, Zsize, pos = [-1.1, -1.1, -1.1])

        self.Cubes: list[Tile3D] = [0] * Xsize * Ysize * Zsize
        for i in range(self.Xsize):
            for j in range(self.Ysize):
                for k in range(self.Zsize):
                    coord = self.get_coord(i, j, k)
                    self.Cubes[coord] = Tile3D(app)
        self.tile_size = self.Cubes[0].tile_size

        self.SetCubesPosition()

    def get_coord(self, x: int, y:int, z: int):
        return x + y * self.Xsize + z * self.Xsize * self.Ysize;

    def SetCubesPosition(self):
        r_o = RENDER_OFFSET
        ts = self.tile_size
        for i in range(self.Xsize):
            for j in range(self.Ysize):
                for k in range(self.Zsize):
                    coord = self.get_coord(i, j, k)
                    self.Cubes[coord].pos = (ts*i + r_o*(i-1), ts*j + r_o*(j-1), ts*k + r_o*(k-1))

    def render(self):
        self.Axes.render()
        for i in range(self.Xsize):
            for j in range(self.Ysize):
                for k in range(self.Zsize):
                    coord = self.get_coord(i, j, k)
                    if self.Cubes[coord].isFigure:
                        self.Cubes[coord].render(True)

    def destroy(self):
        for i in range(self.Xsize):
            for j in range(self.Ysize):
                for k in range(self.Zsize):
                    coord = self.get_coord(i, j, k)
                    self.Cubes[coord].destroy()

    def get_Xsize(self):
        return self.Xsize

    def get_Ysize(self):
        return self.Ysize

    def get_Zsize(self):
        return self.Zsize