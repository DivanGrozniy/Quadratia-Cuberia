import json
from os.path import isfile

from GameField3D import *
from Robot3D import *

#SAVE COMMANDS
def SaveLevel(gamefield: GameField3D, robot: Robot3D, filename: str):
    file = open(filename, 'w')

    GridSize = [gamefield.Xsize, gamefield.Ysize, gamefield.Zsize]
    RobotInfo = [robot.x, robot.y, robot.z, robot.eyes, robot.head]

    FT = GetFigureTiles(gamefield)
    MT = GetMarkedTiles(gamefield)
    MW = GetMarkedWalls(gamefield)
    VMT = GetValueMarkedTiles(gamefield)
    VMW = GetValueMarkedWalls(gamefield)

    to_json = {"GameField3D size": GridSize,
               "Robot3D starting position": RobotInfo,
               "Figure Tiles": FT,
               "Marked Tiles": MT,
               "Marked Walls": MW,
               "Value Marked Tiles": VMT,
               "Value Marked Walls": VMW}
    json.dump(to_json, file, indent = 4)
    file.close()

def GetFigureTiles(gamefield: GameField3D) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()
    res = []

    for i in range(Xsize):
        for j in range(Ysize):
            for k in range(Zsize):
                coord = gamefield.get_coord(i, j, k)
                if gamefield.Cubes[coord].isFigure:
                    res.append([i, j, k])
    
    print("Figure Tiles:", end = " ")
    print(res)
    return res

def GetMarkedTiles(gamefield: GameField3D) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()
    res = []

    for i in range(Xsize):
        for j in range(Ysize):
            for k in range(Zsize):
                coord = gamefield.get_coord(i, j, k)
                if gamefield.Cubes[coord].Mark:
                    res.append([i, j, k])
    
    print("Marked Tiles:", end = " ")
    print(res)
    return res

def GetMarkedWalls(gamefield: GameField3D) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()
    res = []

    for i in range(Xsize):
        for j in range(Ysize):
            for k in range(Zsize):
                coord = gamefield.get_coord(i, j, k)
                WM = gamefield.Cubes[coord].WallMark
                for wall_id in range(len(WM)):
                    if WM[wall_id]:
                        res.append([i, j, k, wall_id])
    
    print("Marked Walls:", end = " ")
    print(res)
    return res

def GetValueMarkedTiles(gamefield: GameField3D) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()
    res = []

    for i in range(Xsize):
        for j in range(Ysize):
            for k in range(Zsize):
                coord = gamefield.get_coord(i, j, k)
                tile = gamefield.Cubes[coord]
                if tile.MarkValueFlag:
                    res.append([i, j, k, tile.MarkValue])
    
    print("Value Marked Tiles:", end = " ")
    print(res)
    return res

def GetValueMarkedWalls(gamefield: GameField3D) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()
    res = []

    for i in range(Xsize):
        for j in range(Ysize):
            for k in range(Zsize):
                coord = gamefield.get_coord(i, j, k)
                tile = gamefield.Cubes[coord]

                WMV = tile.WallMarkValue
                WMVF = tile.WallMarkValueFlag
                for wall_id in range(len(WMVF)):
                    if WMVF[wall_id]:
                        res.append([i, j, k, wall_id, WMV[wall_id]])
    
    print("Value Marked Walls:", end = " ")
    print(res)
    return res


#LOAD COMMANDS
def LoadLevel(gamefield: GameField3D, robot: Robot3D, filename: str):
    if not isfile(filename):
        print("FILE " + filename + " NOT FOUND")
        return gamefield, robot

    file = open(filename, 'r')
    Content = json.load(file)
    
    GridSize = Content['GameField3D size']
    new_x = GridSize[0]
    new_y = GridSize[1]
    new_z = GridSize[2]
    if new_x <= 0 or new_y <= 0 or new_z <= 0:
        print("LoadLevel: WRONG DATA: GridSize = " + str(GridSize))
        return gamefield, robot

    RobotInfo = Content['Robot3D starting position']
    FT = Content['Figure Tiles']
    MT = Content['Marked Tiles']
    MW = Content['Marked Walls']
    VMT = Content['Value Marked Tiles']
    VMW = Content['Value Marked Walls']

    gamefield.Xsize = new_x
    gamefield.Ysize = new_y
    gamefield.Zsize = new_z

    gamefield.Cubes = [0] * new_x * new_y * new_z
    for i in range(new_x):
        for j in range(new_y):
            for k in range(new_z):
                coord = gamefield.get_coord(i, j, k)
                gamefield.Cubes[coord] = Tile3D(gamefield.app)
    gamefield.SetCubesPosition()

    gamefield = SetFigureTiles(gamefield, FT)
    gamefield = SetMarkedTiles(gamefield, MT)
    gamefield = SetMarkedWalls(gamefield, MW)
    gamefield = SetValueMarkedTiles(gamefield, VMT)
    gamefield = SetValueMarkedWalls(gamefield, VMW)
    
    robot.set_gamefield(gamefield)
    ts = robot.tile_size
    robot.x, robot.y, robot.z, new_eyes, new_head = RobotInfo
    robot.pos = [ts*robot.x, ts*robot.y, ts*robot.z]

    #NEED TO MAKE ROBOT ROTATE
    robot.eyes = xp
    robot.head = yp

    while(robot.eyes != new_eyes and robot.head != new_head):
        #First adjust one parametr
        robot.TurnUp()

    if(robot.head == new_head):
        #Need to adjust eyes, just turn sideways
        while(robot.eyes != new_eyes):
            robot.TurnRight()
    elif(robot.eyes == new_eyes):
        #Need to adjust head, just rorate
        while(robot.head != new_head):
            robot.RotateRight()
    

    file.close()
    return gamefield, robot

def SetFigureTiles(gamefield: GameField3D, array: list[list[int]]) -> GameField3D:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()

    for elem in array:
        if type(elem) == list and len(elem) == 3:
            x = elem[0]
            y = elem[1]
            z = elem[2]
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize and z >= 0 and z < Zsize:
                coord = gamefield.get_coord(x, y, z)
                gamefield.Cubes[coord].isFigure = True
            else:
                print("SetFigureTiles - WRONG DATA: " + str(elem))
        else:
            print("SetFigureTiles - WRONG FORMAT" + str(elem))
                
    return gamefield

def SetMarkedTiles(gamefield: GameField3D, array: list[list[int]]) -> GameField3D:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()

    for elem in array:
        if type(elem) == list and len(elem) == 3:
            x = elem[0]
            y = elem[1]
            z = elem[2]
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize and z >= 0 and z < Zsize:
                coord = gamefield.get_coord(x, y, z)
                gamefield.Cubes[coord].Mark = True
            else:
                print("SetMarkedTiles - WRONG DATA" + str(elem))
        else:
            print("SetMarkedTiles - WRONG FORMAT" + str(elem))
    
    return gamefield

def SetMarkedWalls(gamefield: GameField3D, array: list[list[int]]) -> GameField3D:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()

    for elem in array:
        if type(elem) == list and len(elem) == 4:
            x = elem[0]
            y = elem[1]
            z = elem[2]
            wall_id = elem[3] % 6
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize and z >= 0 and z < Zsize:
                coord = gamefield.get_coord(x, y, z)
                gamefield.Cubes[coord].WallMark[wall_id] = True
            else:
                print("SetMarkedWalls - WRONG DATA" + str(elem))
        else:
            print("SetMarkedWalls - WRONG FORMAT" + str(elem))

    return gamefield

def SetValueMarkedTiles(gamefield: GameField3D, array: list[list[int]]) -> GameField3D:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()

    for elem in array:
        if type(elem) == list and len(elem) == 4:
            x = elem[0]
            y = elem[1]
            z = elem[2]
            value = elem[3]
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize and z >= 0 and z < Zsize and type(value) == int:
                coord = gamefield.get_coord(x, y, z)
                gamefield.Cubes[coord].MarkValueFlag = True
                gamefield.Cubes[coord].MarkValue = value
            else:
                print("SetValueMarkedTiles - WRONG DATA" + str(elem))
        else:
            print("SetValueMarkedTiles - WRONG FORMAT" + str(elem))

    return gamefield

def SetValueMarkedWalls(gamefield: GameField3D, array: list[list[int]]) -> GameField3D:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    Zsize = gamefield.get_Zsize()

    for elem in array:
        if type(elem) == list and len(elem) == 5:
            x = elem[0]
            y = elem[1]
            z = elem[2]
            wall_id = elem[3] % 6
            value = elem[4]
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize and z >= 0 and z < Zsize and type(value) == int:
                coord = gamefield.get_coord(x, y, z)
                gamefield.Cubes[coord].WallMarkValueFlag[wall_id] = True
                gamefield.Cubes[coord].WallMarkValue[wall_id] = value
            else:
                print("SetValueMarkedWalls - WRONG DATA" + str(elem))
        else:
            print("SetValueMarkedWalls - WRONG FORMAT" + str(elem))

    return gamefield


#LEVEL EDITOR COMMANDS
def SetGameFieldSize(gamefield: GameField3D, robot: Robot3D, new_x: int, new_y: int, new_z: int):
    if new_x <= 0 or new_y <= 0 or new_z<=0:
        print("SetGameFieldSize: WRONG DATA: new_x = " + str(new_x) + ", new_y = " + str(new_y) + ", new_z = " + str(new_z))
        return gamefield, robot

    FT = GetFigureTiles(gamefield)
    MT = GetMarkedTiles(gamefield)
    MW = GetMarkedWalls(gamefield)
    VMT = GetValueMarkedTiles(gamefield)
    VMW = GetValueMarkedWalls(gamefield)

    new_gf: GameField3D = gamefield
    new_gf.Xsize = new_x
    new_gf.Ysize = new_y
    new_gf.Zsize = new_z

    new_gf.Cubes = [0] * new_x * new_y * new_z
    for i in range(new_x):
        for j in range(new_y):
            for k in range(new_z):
                coord = new_gf.get_coord(i, j, k)
                new_gf.Cubes[coord] = Tile3D(new_gf.app)

    new_gf.SetCubesPosition()
    new_gf.Axes.update_vao(new_x, new_y, new_z)

    new_gf = SetFigureTiles(new_gf, FT)
    new_gf = SetMarkedTiles(new_gf, MT)
    new_gf = SetMarkedWalls(new_gf, MW)
    new_gf = SetValueMarkedTiles(new_gf, VMT)
    new_gf = SetValueMarkedWalls(new_gf, VMW)

    robot.set_gamefield(new_gf)

    return new_gf, robot

def SetRobotPosition(robot: Robot3D, new_x: int, new_y: int, new_z: int, new_eyes: int = xp, new_head: int = yp) -> Robot3D:
    if new_x < 0 or new_x >= robot.Xsize or new_y < 0 or new_y >= robot.Ysize or new_z < 0 or new_z >= robot.Zsize:
        print("SetRobotPosition: WRONG DATA: new_x = " + str(new_x) + ", new_y = " + str(new_y) + ", new_z = " + str(new_z))
        return robot
    
    robot.x = new_x
    robot.y = new_y
    robot.z = new_z
    robot.eyes = new_eyes % 6
    robot.head = new_head % 6

    return robot

def ToggleFigureTile(gamefield: GameField3D, x: int, y: int, z: int) -> GameField3D:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize or z < 0 or z >= gamefield.Zsize:
        print("ToggleFigureTile: WRONG DATA: x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))
        return gamefield

    coord = gamefield.get_coord(x, y, z)
    gamefield.Cubes[coord].isFigure = not gamefield.Cubes[coord].isFigure

    return gamefield

def ToggleMarkTile(gamefield: GameField3D, x: int, y: int, z: int) -> GameField3D:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize or z < 0 or z >= gamefield.Zsize:
        print("ToggleMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))
        return gamefield

    coord = gamefield.get_coord(x, y, z)
    gamefield.Cubes[coord].Mark = not gamefield.Cubes[coord].Mark

    return gamefield

def ToggleWallMark(gamefield: GameField3D, x: int, y: int, z: int, wall_id: int) -> GameField3D:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize or z < 0 or z >= gamefield.Zsize:
        print("ToggleWallMark: WRONG DATA: x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))
        return gamefield

    coord = gamefield.get_coord(x, y, z)
    gamefield.Cubes[coord].WallMark[wall_id] = not gamefield.Cubes[coord].WallMark[wall_id]

    return gamefield

def SetValueMarkTile(gamefield: GameField3D, x: int, y: int, z: int, value: int) -> GameField3D:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize or z < 0 or z >= gamefield.Zsize:
        print("SetValueMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))
        return gamefield

    coord = gamefield.get_coord(x, y, z)
    gamefield.Cubes[coord].MarkValueFlag = True
    gamefield.Cubes[coord].MarkValue = value

    return gamefield

def RemoveValueMarkTile(gamefield: GameField3D, x: int, y: int, z: int) -> GameField3D:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize or z < 0 or z >= gamefield.Zsize:
        print("RemoveValueMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))
        return gamefield

    coord = gamefield.get_coord(x, y, z)
    gamefield.Cubes[coord].MarkValueFlag = False
    gamefield.Cubes[coord].MarkValue = -999

    return gamefield

def SetValueWallMarkTile(gamefield: GameField3D, x: int, y: int, z: int, wall_id: int, value: int) -> GameField3D:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize or z < 0 or z >= gamefield.Zsize:
        print("SetValueWallMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))
        return gamefield

    coord = gamefield.get_coord(x, y, z)
    gamefield.Cubes[coord].WallMarkValueFlag[wall_id] = True
    gamefield.Cubes[coord].WallMarkValue[wall_id] = value

    return gamefield

def RemoveValueWallMarkTile(gamefield: GameField3D, x: int, y: int, z: int, wall_id: int) -> GameField3D:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize or z < 0 or z >= gamefield.Zsize:
        print("RemoveValueWallMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))
        return gamefield

    coord = gamefield.get_coord(x, y, z)
    gamefield.Cubes[coord].WallMarkValueFlag[wall_id] = False
    gamefield.Cubes[coord].WallMarkValue[wall_id] = -999

    return gamefield


