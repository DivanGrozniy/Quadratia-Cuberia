import json
from os.path import isfile

from GameField import *
from Robot import *

#SAVE COMMANDS
def SaveLevel(gamefield: GameField, robot: Robot, filename: str):
    file = open(filename, 'w')

    GridSize = [gamefield.Xsize, gamefield.Ysize]
    RobotInfo = [robot.x, robot.y, robot.orientation]

    FT = GetFigureTiles(gamefield)
    MT = GetMarkedTiles(gamefield)
    MW = GetMarkedWalls(gamefield)
    VMT = GetValueMarkedTiles(gamefield)
    VMW = GetValueMarkedWalls(gamefield)

    to_json = {"GameField size": GridSize,
               "Robot starting position": RobotInfo,
               "Figure Tiles": FT,
               "Marked Tiles": MT,
               "Marked Walls": MW,
               "Value Marked Tiles": VMT,
               "Value Marked Walls": VMW}
    json.dump(to_json, file, indent = 4)
    file.close()

def GetFigureTiles(gamefield: GameField) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    res = []

    for i in range(Ysize):
        for j in range(Xsize):
            if gamefield.Tiles[i * Xsize + j].isFigure:
                res.append([j, i])
    
    print("Figure Tiles:", end = " ")
    print(res)
    return res

def GetMarkedTiles(gamefield: GameField) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    res = []

    for i in range(Ysize):
        for j in range(Xsize):
            if gamefield.Tiles[i * Xsize + j].Mark:
                res.append([j, i])
    
    print("Marked Tiles:", end = " ")
    print(res)
    return res

def GetMarkedWalls(gamefield: GameField) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    res = []
    

    for i in range(Ysize):
        for j in range(Xsize):
            WM = gamefield.Tiles[i * Xsize + j].WallMark
            for ori in range(len(WM)):
                if WM[ori]:
                    res.append([j, i, ori])
    
    print("Marked Walls:", end = " ")
    print(res)
    return res

def GetValueMarkedTiles(gamefield: GameField) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    res = []

    for i in range(Ysize):
        for j in range(Xsize):
            tile = gamefield.Tiles[i * Xsize + j]
            if tile.MarkValueFlag:
                res.append([j, i, tile.MarkValue])
    
    print("Value Marked Tiles:", end = " ")
    print(res)
    return res

def GetValueMarkedWalls(gamefield: GameField) -> list:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    res = []
    

    for i in range(Ysize):
        for j in range(Xsize):
            tile = gamefield.Tiles[i * Xsize + j]
            WMV = tile.WallMarkValue
            WMVF = tile.WallMarkValueFlag
            for ori in range(len(WMVF)):
                if WMVF[ori]:
                    res.append([j, i, ori, WMV[ori]])
    
    print("Value Marked Walls:", end = " ")
    print(res)
    return res


#LOAD COMMANDS
def LoadLevel(gamefield: GameField, robot: Robot, filename: str):
    if not isfile(filename):
        print("FILE " + filename + " NOT FOUND")
        return gamefield, robot

    file = open(filename, 'r')
    Content = json.load(file)
    
    GridSize = Content['GameField size']
    new_x = GridSize[0]
    new_y = GridSize[1]
    if new_x <= 0 or new_y <= 0:
        print("LoadLevel: WRONG DATA: GridSize = " + str(GridSize))
        return gamefield, robot

    RobotInfo = Content['Robot starting position']
    FT = Content['Figure Tiles']
    MT = Content['Marked Tiles']
    MW = Content['Marked Walls']
    VMT = Content['Value Marked Tiles']
    VMW = Content['Value Marked Walls']

    gamefield.Xsize = new_x
    gamefield.Ysize = new_y

    gamefield.Tiles = [Tile(gamefield.screen)] * new_x * new_y
    for i in range(new_y):
        for j in range(new_x):
            gamefield.Tiles[i * new_x + j] = Tile(gamefield.screen, gamefield.tile_size)
    gamefield.RecalculateTileSize() 
    
    gamefield = SetFigureTiles(gamefield, FT)
    gamefield = SetMarkedTiles(gamefield, MT)
    gamefield = SetMarkedWalls(gamefield, MW)
    gamefield = SetValueMarkedTiles(gamefield, VMT)
    gamefield = SetValueMarkedWalls(gamefield, VMW)
    
    robot.x, robot.y, robot.orientation = RobotInfo
    robot.image = robot.icons[robot.orientation]
    robot.set_gamefield(gamefield)

    file.close()
    return gamefield, robot

def SetFigureTiles(gamefield: GameField, array: list[list[int]]) -> GameField:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    for elem in array:
        if type(elem) == list and len(elem) == 2:
            x = elem[0]
            y = elem[1]
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize:
                gamefield.Tiles[y * Xsize + x].isFigure = True
            else:
                print("SetFigureTiles - WRONG DATA: " + str(elem))
        else:
            print("SetFigureTiles - WRONG FORMAT" + str(elem))
                
    return gamefield

def SetMarkedTiles(gamefield: GameField, array: list[list[int]]) -> GameField:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    for elem in array:
        if type(elem) == list and len(elem) == 2:
            x = elem[0]
            y = elem[1]
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize:
                gamefield.Tiles[y * Xsize + x].Mark = True
            else:
                print("SetMarkedTiles - WRONG DATA" + str(elem))
        else:
            print("SetMarkedTiles - WRONG FORMAT" + str(elem))
    
    return gamefield

def SetMarkedWalls(gamefield: GameField, array: list[list[int]]) -> GameField:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    for elem in array:
        if type(elem) == list and len(elem) == 3:
            x = elem[0]
            y = elem[1]
            ori = elem[2] % 4
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize:
                gamefield.Tiles[y * Xsize + x].WallMark[ori] = True
            else:
                print("SetMarkedWalls - WRONG DATA" + str(elem))
        else:
            print("SetMarkedWalls - WRONG FORMAT" + str(elem))

    return gamefield

def SetValueMarkedTiles(gamefield: GameField, array: list[list[int]]) -> GameField:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    for elem in array:
        if type(elem) == list and len(elem) == 3:
            x = elem[0]
            y = elem[1]
            value = elem[2]
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize and type(value) == int:
                gamefield.Tiles[y * Xsize + x].MarkValueFlag = True
                gamefield.Tiles[y * Xsize + x].MarkValue = value
            else:
                print("SetValueMarkedTiles - WRONG DATA" + str(elem))
        else:
            print("SetValueMarkedTiles - WRONG FORMAT" + str(elem))

    return gamefield

def SetValueMarkedWalls(gamefield: GameField, array: list[list[int]]) -> GameField:
    Xsize = gamefield.get_Xsize()
    Ysize = gamefield.get_Ysize()
    for elem in array:
        if type(elem) == list and len(elem) == 4:
            x = elem[0]
            y = elem[1]
            ori = elem[2] % 4
            value = elem[3]
            if x >= 0 and x < Xsize and y >= 0 and y < Ysize and type(value) == int:
                gamefield.Tiles[y * Xsize + x].WallMarkValueFlag[ori] = True
                gamefield.Tiles[y * Xsize + x].WallMarkValue[ori] = value
            else:
                print("SetValueMarkedWalls - WRONG DATA" + str(elem))
        else:
            print("SetValueMarkedWalls - WRONG FORMAT" + str(elem))

    return gamefield


#LEVEL EDITOR COMMANDS
def SetGameFieldSize(gamefield: GameField, robot: Robot, new_x: int, new_y: int):
    if new_x <= 0 or new_y <= 0:
        print("SetGameFieldSize: WRONG DATA: new_x = " + str(new_x) + ", new_y = " + str(new_y))
        return gamefield, robot

    FT = GetFigureTiles(gamefield)
    MT = GetMarkedTiles(gamefield)
    MW = GetMarkedWalls(gamefield)
    VMT = GetValueMarkedTiles(gamefield)
    VMW = GetValueMarkedWalls(gamefield)

    new_gf: GameField = gamefield
    new_gf.Xsize = new_x
    new_gf.Ysize = new_y

    new_gf.Tiles = [Tile(new_gf.screen)] * new_x * new_y
    for i in range(new_y):
        for j in range(new_x):
            new_gf.Tiles[i * new_x + j] = Tile(new_gf.screen, new_gf.tile_size)
    new_gf.SetTilesPosition()

    new_gf = SetFigureTiles(new_gf, FT)
    new_gf = SetMarkedTiles(new_gf, MT)
    new_gf = SetMarkedWalls(new_gf, MW)
    new_gf = SetValueMarkedTiles(new_gf, VMT)
    new_gf = SetValueMarkedWalls(new_gf, VMW)

    new_gf.RecalculateTileSize()
    robot.set_gamefield(new_gf)

    return new_gf, robot

def SetRobotPosition(robot: Robot, new_x: int, new_y: int, new_ori: int = 0) -> Robot:
    if new_x < 0 or new_x >= robot.Xsize or new_y < 0 or new_y >= robot.Ysize:
        print("SetRobotPosition: WRONG DATA: new_x = " + str(new_x) + ", new_y = " + str(new_y))
        return robot
    
    robot.x = new_x
    robot.y = new_y
    robot.orientation = new_ori % 4

    return robot

def ToggleFigureTile(gamefield: GameField, x: int, y: int) -> GameField:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize:
        print("ToggleFigureTile: WRONG DATA: x = " + str(x) + ", y = " + str(y))
        return gamefield

    gamefield.Tiles[y * gamefield.Xsize + x].isFigure = not gamefield.Tiles[y * gamefield.Xsize + x].isFigure

    return gamefield

def ToggleMarkTile(gamefield: GameField, x: int, y: int) -> GameField:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize:
        print("ToggleMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y))
        return gamefield

    gamefield.Tiles[y * gamefield.Xsize + x].Mark = not gamefield.Tiles[y * gamefield.Xsize + x].Mark

    return gamefield

def ToggleWallMark(gamefield: GameField, x: int, y: int, ori: int) -> GameField:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize:
        print("ToggleWallMark: WRONG DATA: x = " + str(x) + ", y = " + str(y))
        return gamefield

    gamefield.Tiles[y * gamefield.Xsize + x].WallMark[ori] = not gamefield.Tiles[y * gamefield.Xsize + x].WallMark[ori]

    return gamefield

def SetValueMarkTile(gamefield: GameField, x: int, y: int, value: int) -> GameField:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize:
        print("SetValueMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y))
        return gamefield

    gamefield.Tiles[y * gamefield.Xsize + x].MarkValueFlag = True
    gamefield.Tiles[y * gamefield.Xsize + x].MarkValue = value

    return gamefield

def RemoveValueMarkTile(gamefield: GameField, x: int, y: int) -> GameField:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize:
        print("RemoveValueMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y))
        return gamefield

    gamefield.Tiles[y * gamefield.Xsize + x].MarkValueFlag = False
    gamefield.Tiles[y * gamefield.Xsize + x].MarkValue = -999

    return gamefield

def SetValueWallMarkTile(gamefield: GameField, x: int, y: int, ori: int, value: int) -> GameField:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize:
        print("SetValueMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y))
        return gamefield

    gamefield.Tiles[y * gamefield.Xsize + x].WallMarkValueFlag[ori] = True
    gamefield.Tiles[y * gamefield.Xsize + x].WallMarkValue[ori] = value

    return gamefield

def RemoveValueWallMarkTile(gamefield: GameField, x: int, y: int, ori: int) -> GameField:
    if x < 0 or x >= gamefield.Xsize or y < 0 or y >= gamefield.Ysize:
        print("RemoveValueMarkTile: WRONG DATA: x = " + str(x) + ", y = " + str(y))
        return gamefield

    gamefield.Tiles[y * gamefield.Xsize + x].WallMarkValueFlag[ori] = False
    gamefield.Tiles[y * gamefield.Xsize + x].WallMarkValue[ori] = -999

    return gamefield

