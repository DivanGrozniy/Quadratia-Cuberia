from Cuberia import *

app: CuberiaEngine = CuberiaEngine(screen_name = "Level 1", run_type = "PLAYER")

PROGRAM_SPEED = 5 #actions per second

def CommandTemplate(action, *args):
    app.get_time()
            
    app.camera.update()

    #MAIN CODE HERE
    res = action(*args)

    app.render()
    app.delta_time = app.clock.tick(PROGRAM_SPEED)

    return res

#RANGE MODE
def FigureCheck(x: int, y: int, z: int) -> bool:
    return CommandTemplate(app.Vertun.CheckTileFigure, x, y, z)

#TILE MARKING
def MarkTileWithValue(value: int, x: int, y: int, z: int):
    CommandTemplate(app.Vertun.MarkTileWithValue, app.Field, value, x, y, z)
def CleanTileWithValue(x: int, y: int, z: int):
    CommandTemplate(app.Vertun.CleanTileWithValue, app.Field, x, y, z)
def CheckTileValueMark(x: int, y: int, z: int):
    return CommandTemplate(app.Vertun.ValueCheckTileMark, x, y, z)

def MarkWallWithValue(value: int, x: int, y: int, z: int, dx: int, dy: int, dz: int):
    CommandTemplate(app.Vertun.MarkWallWithValue, app.Field, value, x, y, z, dx, dy, dz)
def CleanWallWithValue(x: int, y: int, z: int, dx: int, dy: int, dz: int):
    CommandTemplate(app.Vertun.CleanWallWithValue, app.Field, x, y, z, dx, dy, dz)
def CheckWallValueMark(x: int, y: int, z: int, dx: int, dy: int, dz: int):
    return CommandTemplate(app.Vertun.ValueCheckTileWallMark, x, y, z, dx, dy, dz)




#MELEE MODE
#VERTUN MOVEMENT
def WallCheck() -> bool:
    return CommandTemplate(app.Vertun.WallCheck)

def Move():
    CommandTemplate(app.Vertun.Step)

def TurnRight():
    CommandTemplate(app.Vertun.TurnRight)
def TurnLeft():
    CommandTemplate(app.Vertun.TurnLeft)
def TurnUp():
    CommandTemplate(app.Vertun.TurnUp)
def TurnDown():
    CommandTemplate(app.Vertun.TurnDown)

def RotateLeft():
    CommandTemplate(app.Vertun.RotateLeft)
def RotateRight():
    CommandTemplate(app.Vertun.RotateRight)

def ResetOrientation():
    CommandTemplate(app.Vertun.ResetOrientation)


#VERTUN MARKING
def MarkTile():
    CommandTemplate(app.Vertun.MarkTile, app.Field)
def CleanTile():
    CommandTemplate(app.Vertun.CleanTile, app.Field)
def CheckTileMark() -> bool:
    return CommandTemplate(app.Vertun.BoolCheckTileMark)

def MarkWall():
    CommandTemplate(app.Vertun.MarkWall, app.Field, True)
def CleanWall():
    CommandTemplate(app.Vertun.CleanWall, app.Field, True)
def CheckWallMark() -> bool:
    return CommandTemplate(app.Vertun.BoolCheckTileWallMark)

def MarkTileWithValue(value: int):
    CommandTemplate(app.Vertun.MarkTileWithValue, app.Field, value)
def CleanTileWithValue():
    CommandTemplate(app.Vertun.CleanTileWithValue, app.Field)
def CheckTileValueMark():
    return CommandTemplate(app.Vertun.ValueCheckTileMark)

def MarkWallWithValue(value: int):
    CommandTemplate(app.Vertun.MarkWallWithValue, app.Field, value)
def CleanWallWithValue():
    CommandTemplate(app.Vertun.CleanWallWithValue, app.Field)
def CheckWallValueMark():
    return CommandTemplate(app.Vertun.ValueCheckTileWallMark)


#Student's program
LEVEL_NAME = "Level3" + ".json"

def RunToWall():
    while not WallCheck():
        Move()

def MainProgram():
    for _ in range(2):
        ResetOrientation()
        MarkTile()

        for _ in range(4):
            RunToWall()
            MarkTile()
            TurnRight()

        TurnUp()
        RunToWall()
    
    



if __name__ == '__main__':
    app.Field, app.Vertun = LoadLevel(app.Field, app.Vertun, LEVELS_DIR + LEVEL_NAME)

    MainProgram()
    
    
    print("Program finished. Press ESC")
    wait = True
    while wait:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                wait = False
                break

        app.get_time()   
        app.camera.update()
        app.render()
        app.delta_time = app.clock.tick(60)
    pg.quit()
                


