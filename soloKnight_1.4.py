#! python3
# soloKnight.py - A game where you have to move your player and kill the enemies
# Eneies can move by 1 'block' on heach axis (they can go UP and RIGHT in the same turn, but the can't go UP and UP or RIGHT and RIGHT in the same turn)
# The player can move only by one 'block'
# You kill the enemies by going on top of them
# The enemies kill you by going on top of you
# If the player tries to go OoB he/she loses the turn
import random, os

def cls():
    if os.system("clear") == 1:
        os.system("cls")
    else:
        os.system("clear")
    
def blankGrid(grid):                        #Clears the grid, preaparing it for updates
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid [i][j] = '.'
    
def printMap(grid):         #Prints the map
    print('HOW TO READ THE MAP:\n\t[*]EMPTY SPACE = \'.\'\n\t[*]PLAYER = \'X\'\t\t(ONE MOVE ON ONE AXIS)\n\t[*]KNIGHT = \'K\' \'J\'\t(ONE MOVE ON EACH AXIS)\n')
    for i in range(len(grid)):
        print('', end='\t')
        for j in range(len(grid[i])):
            print(grid[i][j], end=' ')
        print('')

def randomPlacement(grid, units):           #Places every unit at the start of the game on the grid
    possible_locations = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            possible_locations.append([y,x])
    random.shuffle(possible_locations)
    for u in units:
        unit_location = possible_locations.pop()
        units[u][1] = unit_location[0]
        units[u][2] = unit_location[1]
        units[u][3] = True

def placeUnit(grid, unit):                      #Updates the unit's placement
    if unit[3]:
        grid[unit[1]][unit[2]] = unit[0]

def calcPosition(unit, unitMove):               #Moves the unit and check if its out of bounds, if it is, it skips the turn
    if unitMove == 'UP' or unitMove == 'W':
        if (unit[1] - 1) >= 0:
            return (unit[1] - 1, unit[2])
        else:
            return (unit[1], unit[2])
        
    elif unitMove == 'DOWN' or unitMove == 'S':
        if (unit[1] + 1) <= 7:
            return (unit[1] + 1, unit[2])
        else:
            return (unit[1], unit[2])
        
    elif unitMove == 'LEFT' or unitMove == 'A':
        if (unit[2] - 1) >= 0:
            return (unit[1], unit[2] - 1)
        else:
            return (unit[1], unit[2])
        
    elif unitMove == 'RIGHT' or unitMove == 'D':
        if (unit[2] + 1) <= 8:
            return (unit[1], unit[2] + 1)
        else:
            return (unit[1], unit[2])

def playerTurn(units, moves):           #Player's turn
    while True:                         #Keeps asking input until its valid
        print('\nMOVEMENT OPTIONS:\n\t[*]UP\t/ W\n\t[*]DOWN\t/ S\n\t[*]LEFT\t/ A\n\t[*]RIGHT/ D\n\n\t\t>>', end=' ')
        playerMove = input()
        if playerMove.upper() in moves:
            units['player'][1], units['player'][2] = calcPosition(units['player'], playerMove.upper())
            break


def enemyTurn(units):               #Enemy's turn
    for u in units:                     #Every unit moves trying to reach the player on both axis
        if units[u][3] and units[u][0] != units['player'][0]:
            if units[u][1] > units['player'][1]:
                units[u][1], units[u][2] = calcPosition(units[u], 'UP')
            elif units[u][1] < units['player'][1]:
                units[u][1], units[u][2] = calcPosition(units[u], 'DOWN')
            if not calcKill(units[u], units['player']):
                return False
            if units[u][2] > units['player'][2]:
                units[u][1], units[u][2] = calcPosition(units[u], 'LEFT')
            elif units[u][2] < units['player'][2]:
                units[u][1], units[u][2] = calcPosition(units[u], 'RIGHT')
            if not calcKill(units[u], units['player']):
                return False
    return True

def calcKill(attack, defend):            #Checks if a unit killed someone
    if attack[1] == defend[1] and attack[2] == defend[2]:     #If unit is on top of some unit
        return False
    else:
        return True

def keepLoop(units):    #Check if the game neeed to be running
    if enemiesDead(units) or not units['player'][3]:          #If all enemies/player are/is dead, stop looping
        return False
    else:
        return True

def enemiesDead(units):             #Returns False if all enemies are not dead
    unitsAlive = 0
    for u in units:
        if units[u][0] != units['player'][0]:
            if units[u][3]:
                unitsAlive += 1
    if unitsAlive > 0:
        return False
    else:
        return True

game = True
while(game):
    grid = [['.' for _ in range(9)] for _ in range(8)]
    moves = ('UP', 'W', 'DOWN', 'A', 'LEFT', 'S', 'RIGHT', 'D')       #Tuples of all movement option
    units = {'player':['X', 0, 0, False], 'knight1':['K', 0, 0, False], 'knight2':['J', 0, 0, False]}        #Dictonary of all units(standard unit form: [Symbol, Y, X, Status(False == Dead)])

    randomPlacement(grid, units)

    while(keepLoop(units)):                  #Start game loop
        cls()
        blankGrid(grid)                         
        for u in units:                         #Updates every unit's position
            placeUnit(grid, units[u])
        printMap(grid)

        playerTurn(units, moves)
        for u in units:
            if units[u][0] != units['player'][0] and units[u][3]:
                units[u][3] = calcKill(units['player'], units[u])           #Checks kills before enemy turn
        if not keepLoop(units):
            break
        units['player'][3] = enemyTurn(units)       #Play enemy turn and check player status

    cls()                   #end game screen
    blankGrid(grid)
    for u in units:                         #Updates every unit's position for the end game
            placeUnit(grid, units[u])
    for i in range(len(grid)):
        print('', end='\t')
        for j in range(len(grid[i])):
            print(grid[i][j], end=' ')
        print('')
    if units['player'][3]:
        print('\n\t   +-YOU-WON-+')
    else:
        print('\n\t   --YOU-LOST--')
    choice = 'X'
    while(choice.upper() != 'Y' and choice.upper() != 'N'):         #Play again ?
        print('\tPLAY-AGAIN-? (Y/N)\n\t>>', end=' ')
        choice = input()
    if choice.upper() != 'Y':
        game = False
