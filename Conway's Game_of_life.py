import random
import pygame as p
#import Cell



WORLD_SIZE = 600  # pixels
ROWS = COLS = 20  # smaller number will make cells larger
SQ_WIDTH = WORLD_SIZE // COLS  # how many pixels per side of square


def cellUpdate(isAlive=False,aliveNextFrame = None,neighboringCells = None):
    # start empty, the populate this with object surrounding this cell
    if neighboringCells is None:
        neighboringCells=[]
    # count the alive neighbors from the list above
    aliveNeighbors = 0
    age = 0  # countinuous length of time since previous death
    for cell in neighboringCells:
        if cell[0]:
            aliveNeighbors += 1

    # if fewer than two neighboring cells, this cell dies
    if isAlive and aliveNeighbors < 2:
        aliveNextFrame = False

    # if this cell is alive and has between 2 and 3 neighboringCells, cell continues to live
    elif isAlive and aliveNeighbors == 2:
        aliveNextFrame = True

    elif isAlive and aliveNeighbors == 3:
        aliveNextFrame = True

    # if this cell is alive and has more than 3 neighboringCells, it dies
    elif isAlive and aliveNeighbors > 3:

        aliveNextFrame = False

    # if this cell is dead but has 3 neighboringCells it come alive
    else:

        if aliveNeighbors == 3:
            aliveNextFrame = True

        else:
            aliveNextFrame = False

    return [isAlive,aliveNextFrame,neighboringCells]

def cellNewGen(cellObject):
        cellObject[0] = cellObject[1]
def drawButton(screen, label, colors, x1, x2, y1, y2, font):
        x = 70
        y = 40
        p.draw.rect(screen, colors, (x1, x2, y1, y2))
        font = p.font.SysFont(font, 20)
        screen.blit(font.render(label, True, 'black'), (x1 + x, x2 + y, y1 + x, y2 + y))


def checkClick(screen, label, colors, x1, x2, y1, y2, font):
    click = p.mouse.get_pos()
    buttonRect = p.draw.rect(screen, colors, (x1, x2, y1, y2))
    if buttonRect.collidepoint(click):
        return True

def main():
    global Start
    p.init()
    screen = p.display.set_mode((WORLD_SIZE, WORLD_SIZE + 100))
    clock = p.time.Clock()
    aliveCells = generateRandCoords()
    world = initializeWorld(aliveCells)
    calculateNeighbors(world)
    Start = False
    done = False
    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                done = True
            if event.type == p.MOUSEBUTTONDOWN:

                if checkClick(screen, 'start', 'green', 0, 600, 200, 700, 'Arial'):  # start button
                    Start = True
                elif checkClick(screen, 'stop', 'red', 400, 600, 700, 300, 'Arial'):  # stop button
                    Start = False
                elif checkClick(screen, 'reset', 'yellow', 200, 600, 200, 700, 'Arial'):  # reset button
                    Start = False
                    # updateWorld(world)  # MUST COME FIRST
                    # newGen(world)  # MUST HAPPEN AFTER UPDATE

                    drawWorld(screen, world)
                    buttons(screen)
                    aliveCells = generateRandCoords()
                    world = initializeWorld(aliveCells)
                    calculateNeighbors(world)

        buttons(screen)

        if Start == True:
            drawWorld(screen, world)
            #print("world[2][0][0] :{}".format(world[2][0][0]))
            updateWorld(world)  # MUST COME FIRST
            newGen(world)  # MUST HAPPEN AFTER UPDATE


        p.display.flip()
        clock.tick(2)

    p.quit()


def generateRandCoords():
    aliveCells = []
    r = random.randint(0, 600)
    for i in range(r):
        aliveCells.append((random.randint(0, ROWS - 1), random.randint(0, COLS - 1)))
    return aliveCells


# return list of rand coords
# Warning - might generate repeats in the list - is that okay?

def initializeWorld(aliveCellCoordinates):
    world = []  # create a 2D list of all cell objects
    for row in range(ROWS):
        world.append([])  # creates a blank row to put cells into
        for col in range(COLS):
            if (col, row) in aliveCellCoordinates:
                world[row].append(cellUpdate(isAlive=True))  # create alive cell object and append to the row list
            else:
                world[row].append(cellUpdate(isAlive=False))

    return world


def drawWorld(screen, world):
    for r in range(ROWS):
        for c in range(COLS):
            #print("world[r][c][0]:{}".format(world[r][c][0]))
            if world[r][c][0]:  # particular cells is alive
                color = 'turquoise'
            else:  # cell is not alive
                color = 'lavender'
            p.draw.rect(screen, "white",
                             (c * SQ_WIDTH, r * SQ_WIDTH, SQ_WIDTH, SQ_WIDTH))
            # border of the square
            p.draw.rect(screen, "gray",
                             (c * SQ_WIDTH, r * SQ_WIDTH, SQ_WIDTH, SQ_WIDTH), 1)
            if world[r][c][0]:
                # draw a dot in a cell
                p.draw.circle(screen, "black", (c * SQ_WIDTH + SQ_WIDTH // 2,
                                                     r * SQ_WIDTH + SQ_WIDTH // 2), SQ_WIDTH / 3)

# p.draw.rect(screen, 'lavender', (4 * SQ_WIDTH, 1 * SQ_WIDTH, SQ_WIDTH, SQ_WIDTH)) lavender is dead
# p.draw.rect(screen, 'turquoise', (4 * SQ_WIDTH, 2 * SQ_WIDTH, SQ_WIDTH, SQ_WIDTH)) turquoise is alive

def updateWorld(world):
    for r in world:
        for c in r:
            nc = cellUpdate(c[0],c[1],c[2])
            c[1]=nc[1]
            c[2]=nc[2]

def newGen(world):
    for r in world:
        for c in r:
            c[0]=c[1]


def calculateNeighbors(world):
    for r in range(ROWS):
        for c in range(COLS):
            currentCell = world[r][c]
            neighboringCoords = [(c - 1, r - 1), (c, r - 1), (c + 1, r - 1),
                                 (c - 1, r), (c + 1, r),
                                 (c - 1, r + 1), (c, r + 1), (c + 1, r + 1)]
            #print(neighboringCoords)
            for coord in neighboringCoords:
                # check if the coordinates are in the world (not negative or off the boundaries)
                if coord[0] in range(COLS) and coord[1] in range(ROWS):
                    # append that neighbor to the list (update neighboringCells field of each cell)
                    currentCell[2].append(world[coord[1]][coord[0]])
                    #print(currentCell[2])
            #exit()

def buttons(screen):
    #global start, stop, reset
    drawButton(screen, 'start', 'green', 0, 600, 200, 700, 'Arial')
    drawButton(screen, 'stop', 'red', 400, 600, 700, 300, 'Arial')
    drawButton(screen, 'reset', 'yellow', 200, 600, 200, 700, 'Arial')


if __name__ == '__main__':
    main()