from Quadratia import *

app: QuadratiaEngine = QuadratiaEngine(screen_name = "Level 1", run_type = "PLAYER")

PROGRAM_SPEED = 2 #actions per second

def CommandTemplate(action, *args):
    app.get_time()
            
    #MAIN CODE HERE
    res = action(*args)

    app.render()
    app.delta_time = app.clock.tick(PROGRAM_SPEED)

    return res

#RANGE MODE
def FigureCheck(x: int, y: int) -> bool:
    return CommandTemplate(app.Vertun.CheckTileFigure, x, y)

#TILE MARKING
def MarkTileWithValue(value: int, x: int, y: int):
    CommandTemplate(app.Vertun.MarkTileWithValue, app.Field, value, x, y)
def CleanTileWithValue(x: int, y: int):
    CommandTemplate(app.Vertun.CleanTileWithValue, app.Field, x, y)
def CheckTileValueMark(x: int, y: int):
    return CommandTemplate(app.Vertun.ValueCheckTileMark, x, y)

def MarkWallWithValue(value: int, x: int, y: int, dx: int, dy: int):
    CommandTemplate(app.Vertun.MarkWallWithValue, app.Field, value, x, y, dx, dy)
def CleanWallWithValue(x: int, y: int, dx: int, dy: int):
    CommandTemplate(app.Vertun.CleanWallWithValue, app.Field, x, y, dx, dy)
def CheckWallValueMark(x: int, y: int, dx: int, dy: int):
    return CommandTemplate(app.Vertun.ValueCheckTileWallMark, x, y, dx, dy)




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

def MainProgram():
    TurnRight()
    
    while not CheckTileMark():
        if not WallCheck():
            Move()
        else:
            if app.Vertun.orientation == 1:
                TurnRight()
                Move()
                if CheckTileMark():
                    break
                TurnRight()
            elif app.Vertun.orientation == 3:
                TurnLeft()
                Move()
                if CheckTileMark():
                    break
                TurnLeft()

    print("Answer: [" + str(app.Vertun.x) + ", " + str(app.Vertun.y) + "]")
    return



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
    pg.quit()
                


