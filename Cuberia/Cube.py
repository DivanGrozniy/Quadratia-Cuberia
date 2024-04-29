import pygame as pg
import moderngl as mgl
import numpy as np
import glm

import random

SHADERS_DIR = "Shaders/"

DEFAULT_LINES_COLOR = (0, 0.5, 0.5)
DEFAULT_MARKED_LINES_COLOR = (1, 0, 0)
DEFAULT_VALUE_MARKED_LINES_COLOR = (1, 1, 0)

DEFAULT_POLYGONS_COLOR = (0.5, 0.5, 0.5, 0.3)
DEFAULT_MARKED_POLYGONS_COLOR = (1, 0, 0, 0.5)
DEFAULT_VALUE_MARKED_POLYGONS_COLOR = (1, 1, 0, 0.8)


class Tile3D:
    def __init__(self, app, pos = [0, 0, 0], rot = [0, 0, 0], scale = [1, 1, 1]):
        self.app = app
        self.ctx = app.ctx

        self.tile_size = 2 * scale[0]

        self.isFigure: bool = False

        self.Mark: bool = False
        self.WallMark: list[bool] = [False] * 6

        #self.Mark = bool(random.randint(0, 1))
        #for id in range(6):
        #    self.WallMark[id] = bool(random.randint(0, 1))

        self.MarkValueFlag: bool = False
        self.MarkValue: int = -999
        self.WallMarkValueFlag: list[bool] = [False] * 6
        self.WallMarkValue: list[int] = [-999] * 6


        self.polygons_color = DEFAULT_POLYGONS_COLOR
        self.marked_polygons_color = DEFAULT_MARKED_POLYGONS_COLOR
        self.value_marked_polygons_color = DEFAULT_VALUE_MARKED_POLYGONS_COLOR

        self.lines_color = DEFAULT_LINES_COLOR
        self.marked_lines_color = DEFAULT_MARKED_LINES_COLOR
        self.value_marked_lines_color = DEFAULT_VALUE_MARKED_LINES_COLOR

        self.polygons_vbo = self.get_polygons_vbo()
        self.polygons_shader_program = self.get_shader_program("cube_poly")
        self.polygons_vao = self.get_polygons_vao()

        self.lines_vbo = self.get_lines_vbo()
        self.lines_shader_program = self.get_shader_program("cube_line")
        self.lines_vao = self.get_lines_vao()

        
        self.camera = self.app.camera

        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_martix()

        self.polygons_update()
        self.lines_update()

    #VBO    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for poly_or_line in indices for ind in poly_or_line]
        return np.array(data, dtype='f4')

    def get_polygons_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        #polygons_indices = [(0, 2, 3), (0, 1, 2),
        #           (1, 7, 2), (1, 6, 7),
        #           (6, 5, 4), (4, 7, 6),
        #           (3, 4, 5), (3, 5, 0),
        #           (3, 7, 4), (3, 2, 7),
        #           (0, 6, 1), (0, 5, 6)]

        #color = self.polygons_color
        #polygons_color = [color] * 3 * len(polygons_indices)
        #polygons_color = np.array(polygons_color, dtype='f4')


        polygons_indices = [(0, 6, 1), (0, 5, 6), (0, 1, 6), (0, 6, 5),
                            (1, 7, 2), (1, 6, 7), (1, 2, 7), (1, 7, 6),
                            (0, 2, 3), (0, 1, 2), (0, 3, 2), (0, 2, 1),
                            (6, 5, 4), (4, 7, 6), (6, 4, 5), (4, 6, 7),
                            (3, 4, 5), (3, 5, 0), (3, 5, 4), (3, 0, 5),
                            (3, 7, 4), (3, 2, 7), (3, 4, 7), (3, 7, 2)
                           ]

        polygons_color = []
        for id in range(6):
            if self.WallMark[id] and self.WallMarkValueFlag[id]:
                color = np.array(self.marked_polygons_color) + np.array(self.value_marked_polygons_color)
                color = color / np.linalg.norm(color)
                color = color.tolist()
            elif self.WallMark[id]:
                color = self.marked_polygons_color
            elif self.WallMarkValueFlag[id]:
                color = self.value_marked_polygons_color
            else:
                color = self.polygons_color

            for _ in range(3 * 4):
                polygons_color.append(color)
        polygons_color = np.array(polygons_color, dtype='f4')

        #print("POLYGONS COLOR")
        #print(polygons_color)

        vertex_data = self.get_data(vertices, polygons_indices)

        vertex_data = np.hstack([vertex_data, polygons_color])

        #print("VERTEX DATA")
        #print(vertex_data)

        return vertex_data

    def get_lines_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        lines_indices = [(0, 1), (1, 6), (6, 5), (5, 0),
                        (0, 3), (1, 2), (6, 7), (5, 4),
                        (3, 2), (2, 7), (7, 4), (4, 3)]
        
        if self.Mark and self.MarkValueFlag:
            color = np.array(self.marked_lines_color) + np.array(self.value_marked_lines_color)
            color = color / np.linalg.norm(color)
            color = color.tolist()
        elif self.Mark:
            color = self.marked_lines_color
        elif self.MarkValueFlag:
            color = self.value_marked_lines_color
        else:
            color = self.lines_color

        lines_color = [color] * 2 * len(lines_indices)
        lines_color = np.array(lines_color, dtype='f4')

        vertex_data = self.get_data(vertices, lines_indices)

        vertex_data = np.hstack([vertex_data, lines_color])

        return vertex_data

    def get_polygons_vbo(self):
        vd = self.get_polygons_vertex_data()
        poly_vbo = self.ctx.buffer(vd)
        return poly_vbo

    def get_lines_vbo(self):
        vd = self.get_lines_vertex_data()
        line_vbo = self.ctx.buffer(vd)
        return line_vbo


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
        poly_vao = self.ctx.vertex_array(self.polygons_shader_program, [(self.polygons_vbo, "3f 4f", "in_vertex_pos", "in_polygons_color")])
        return poly_vao

    def get_lines_vao(self):
        line_vao = self.ctx.vertex_array(self.lines_shader_program, [(self.lines_vbo, "3f 3f", "in_vertex_pos", "in_lines_color")])
        return line_vao

    #RENDER
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

    def polygons_update(self):
        self.polygons_shader_program['m_proj'].write(self.camera.m_proj)
        self.polygons_shader_program['m_view'].write(self.camera.m_view)
        self.polygons_shader_program['m_model'].write(self.m_model)

    def lines_update(self):
        self.lines_shader_program['m_proj'].write(self.camera.m_proj)
        self.lines_shader_program['m_view'].write(self.camera.m_view)
        self.lines_shader_program['m_model'].write(self.m_model)

    def polygons_render(self):
        self.polygons_vbo.release()
        self.polygons_vao.release()

        self.polygons_vbo = self.get_polygons_vbo()
        self.polygons_vao = self.get_polygons_vao()
        self.polygons_update()

        self.polygons_vao.render(mgl.TRIANGLES)

    def polygons_destroy(self):
        self.polygons_vbo.release()
        self.polygons_shader_program.release()
        self.polygons_vao.release()

    def lines_render(self):
        self.lines_vbo.release()
        self.lines_vao.release()

        self.lines_vbo = self.get_lines_vbo()
        self.lines_vao = self.get_lines_vao()
        self.lines_update()

        self.lines_vao.render(mgl.LINES)

    def lines_destroy(self):
        self.lines_vbo.release()
        self.lines_shader_program.release()
        self.lines_vao.release()

    def render(self, poly_flag = True):
        self.m_model = self.get_model_martix()
        if poly_flag:
            self.polygons_render()
        self.lines_render()

    def destroy(self):
        self.polygons_destroy()
        self.lines_destroy()



        

    #BOOL MARKING
    def MarkTile(self):
        self.Mark = True

    def CleanTile(self):
        self.Mark = False

    def MarkWall(self, wall_id: int):
        self.WallMark[wall_id % 6] = True

    def CleanWall(self, wall_id: int):
        self.WallMark[wall_id % 6] = False

    #VALUE MARKING
    def MarkTileWithValue(self, value: int):
        self.MarkValueFlag = True
        self.MarkValue = value

        #print("TILE: Marked tile with value " + str(value))

    def CleanTileWithValue(self):
        self.MarkValueFlag = False
        self.MarkValue = -999

    def MarkWallWithValue(self, wall_id: int, value: int):
        self.WallMarkValueFlag[wall_id % 6] = True
        self.WallMarkValue[wall_id % 6] = value

        #print("TILE: Marked tile wall " + str(wall_id % 6) + " with value " + str(value))

    def CleanWallWithValue(self, wall_id: int):
        self.WallMarkValueFlag[wall_id % 6] = False
        self.WallMarkValue[wall_id % 6] = -999