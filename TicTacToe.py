import pygame
import sys
import random
import copy


def CheckVictory(status):
    sums = [0, 0, 0, 0, 0, 0, 0, 0]
    tot = 0
    for i in range(3):
        for j in range(3):
            value = status[i][j]
            tot += value
            sums[i] += value
            sums[j+3] += value
            if i == j:
                sums[6] += value
            if i+j == 2:
                sums[7] += value
    if 12 in sums:  # gana X player
        return 1
    if 9 in sums:  # gana O computer
        return 3
    if tot > 30:  # empate
        return 2
    return 0


def Movement(status, move, isPlayer):
    newStatus = copy.deepcopy(status)
    newStatus[move[0]][move[1]] = 3 + int(isPlayer)
    victory = CheckVictory(newStatus)
    if victory != 0:
        return victory-2
    empties = []
    suma = []
    for i in range(3):
        for j in range(3):
            if newStatus[i][j] == 0:
                empties.append([i, j])
    for x in empties:
        suma.append(Movement(newStatus, x, not(isPlayer)))

    if isPlayer:
        return max(suma)
    return min(suma)


def DoMovement():
    global status
    move = []
    zeros = []
    posibilities = []
    for i in range(3):
        for j in range(3):
            if status[i][j] == 0:
                zeros.append([i, j])

    if len(zeros) == 8:
        if status[1][1] == 0:
            status[1][1] = 3
        else:
            status[random.choice((0, 2))][random.choice((0, 2))] = 3
    else:
        for p in zeros:
            posibility = Movement(status, p, False)
            posibilities.append(posibility)
        for i in range(len(posibilities)):
            if posibilities[i] == max(posibilities):
                move = zeros[i]
                status[move[0]][move[1]] = 3
                return


def Reset():
    global status
    for i in range(3):
        for j in range(3):
            status[i][j] = 0


# init
pygame.init()
clock = pygame.time.Clock()

# main window
Width = 640
Height = 480
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Tic Tac Toe")


# colores
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)

# font
Title = pygame.font.Font('freesansbold.ttf', 32)
MenuItem = pygame.font.Font("freesansbold.ttf", 25)

# objetos
marks = [-170, -40, 90]
boxes = []
for i in range(3):
    box = []
    for j in range(3):
        box.append(pygame.Rect(
            Width/2+marks[j], Height/2+marks[i], 80, 80))
    boxes.append(box)

# menu 1
menuItems = []
menuItemsRects = []
menuTexts = [["Menu", "1 Jugador", "2 Jugadores", "Salir"],
             ["Un Jugador", "Primer Turno Usuario",
                 "Primer Turno Computadora", "Atras"],
             ["Dos Jugadores", "Empieza X", "Empieza O", "Atras"],
             ["Rematch", "Atras", "Salir"]]
menuPositionsX = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [-150, 0, 150]]
menuPositionY = [[-100, -30, 10, 50],
                 [-100, -30, 10, 50],
                 [-100, -30, 10, 50],
                 [200, 200, 200]]
menuFonts = [[Title, MenuItem, MenuItem, MenuItem],
             [Title, MenuItem, MenuItem, MenuItem],
             [Title, MenuItem, MenuItem, MenuItem],
             [MenuItem, MenuItem, MenuItem]]

for i in range(4):
    menuItem = []
    menuItemRect = []
    for j in range(len(menuTexts[i])):
        menuItem.append(menuFonts[i][j].render(
            menuTexts[i][j], True, light_grey, bg_color))
        menuItemRect.append(menuItem[j].get_rect())
        menuItemRect[j].center = (
            Width / 2 + menuPositionsX[i][j], Height / 2 + menuPositionY[i][j])
    menuItems.append(menuItem)
    menuItemsRects.append(menuItemRect)
#menuItem = Title.render("Menu", True, light_grey, bg_color)

# variables
status = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]
lineMarks = [-65, 65, -180, -180]
lineMarks2 = [-65, 65, 180, 180]
ComputerStarts = True
Turn = 0
Starts = 0
Play = False
Menu = 1

# loop

while True:
    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if Play and Menu != 4:
                for i in range(3):
                    for j in range(3):
                        if boxes[i][j].collidepoint(pos) and status[i][j] == 0:
                            if Starts == 0:
                                status[i][j] = 4
                                DoMovement()
                            elif Turn == 1:
                                status[i][j] = 3
                                Turn += 1
                            elif Turn == 2:
                                status[i][j] = 4
                                Turn -= 1
            elif Menu == 1:
                if menuItemsRects[0][1].collidepoint(pos):
                    Menu = 2
                if menuItemsRects[0][2].collidepoint(pos):
                    Menu = 3
                if menuItemsRects[0][3].collidepoint(pos):
                    pygame.quit()
                    sys.exit()
            elif Menu == 2:
                if menuItemsRects[1][1].collidepoint(pos):
                    Menu = 0
                    Play = True
                    ComputerStarts = False
                if menuItemsRects[1][2].collidepoint(pos):
                    Menu = 0
                    Play = True
                    ComputerStarts = True
                    status[random.choice((0, 2))][random.choice((0, 2))] = 3
                if menuItemsRects[1][3].collidepoint(pos):
                    Menu = 1
            elif Menu == 3:
                if menuItemsRects[2][1].collidepoint(pos):
                    Menu = 0
                    Play = True
                    Turn = 2
                    Starts = 2
                    ComputerStarts = False
                if menuItemsRects[2][2].collidepoint(pos):
                    Menu = 0
                    Play = True
                    Turn = 1
                    Starts = 1
                    ComputerStarts = False
                if menuItemsRects[2][3].collidepoint(pos):
                    Menu = 1
            elif Menu == 4:
                if menuItemsRects[3][0].collidepoint(pos):
                    Reset()
                    Menu = 0
                    Turn = Starts
                    if ComputerStarts == True:
                        status[random.choice(
                            (0, 2))][random.choice((0, 2))] = 3
                if menuItemsRects[3][1].collidepoint(pos):
                    Reset()
                    Menu = 1
                    Play = False
                    Starts = 0
                if menuItemsRects[3][2].collidepoint(pos):
                    pygame.quit()
                    sys.exit()

    # victory
    victoria = CheckVictory(status)
    if victoria != 0:
        Menu = 4

    # visuals
    screen.fill(bg_color)
    if Play:
        for i in range(3):
            for j in range(3):
                if status[i][j] == 3:
                    pygame.draw.ellipse(screen, light_grey, boxes[i][j], 8)
                elif status[i][j] == 4:
                    pygame.draw.line(screen, light_grey,
                                     boxes[i][j].topleft, boxes[i][j].bottomright, 8)
                    pygame.draw.line(screen, light_grey,
                                     boxes[i][j].bottomleft, boxes[i][j].topright, 8)
        for i in range(4):
            pygame.draw.line(screen, light_grey, (Width/2+lineMarks[i], Height/2+lineMarks[3-i]),
                             (Width/2+lineMarks2[i], Height/2+lineMarks2[3-i]), 10)
    if Menu != 0:
        for i in range(len(menuItemsRects[Menu-1])):
            screen.blit(menuItems[Menu-1][i], menuItemsRects[Menu-1][i])

    #creen.blit(menuItem, menuItemRect)

    pygame.display.flip()
    clock.tick(60)
