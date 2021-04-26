import pygame
import sys
import random


def movement():
    global speed_x, ship_x
    ship_x += speed_x
    if ship_x <= 0:
        ship_x += 5
    if ship_x >= screen_width-50:
        ship_x -= 5


def shoot():
    global bullets, ship_x, ship_y
    bullet1 = pygame.Rect(ship_x+5, ship_y, 1, 10)
    bullet2 = pygame.Rect(ship_x+45, ship_y, 1, 10)
    bullets.append([bullet1, bullet2])


def bulletMovement():
    global bullets, vida, menu
    erase = []
    if len(bullets) > 0:
        for i in range(len(bullets)):
            bullets[i][0].y -= 5
            bullets[i][1].y -= 5
            if bullets[i][0].colliderect(menuBackground):
                erase.append(i)
                vida -= 10
            if bullets[i][0].y < 0:
                erase.append(i)
        try:
            for j in erase:
                bullets.pop(j)
        except:
            pass


def logica():
    global turno, vida, menu, menuBackground, light_grey, deathStar_y, explotion, explotionImage
    if vida == 0:
        menu += 1
        vida = 100
        turno = 0
    turno += 1
    if turno == 1:
        for i in range(len(menuItemsRects[menu])):
            menuItemsRects[menu][i].y -= 624
        menuBackground = pygame.Rect(320, -464, 360, 210)
        deathStar_y = -574
        explotion = True
        explotionImage.set_alpha(100)
    elif turno < 30:
        explotionImage.set_alpha(100-(turno))
    elif turno == 30:
        explotion = False
    elif turno < 157:
        for i in range(len(menuItemsRects[menu])):
            menuItemsRects[menu][i].y += 5
        menuBackground = pygame.Rect(320, (turno-29)*5 - 464, 360, 210)
        deathStar_y += 5
    elif turno > 157:
        menuBackground = pygame.Rect(320, 171, 360, 210)


# general setup
pygame.init()
clock = pygame.time.Clock()
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Expo Innovation and Product Development")
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)
red = (255, 40, 0)
speed_x = 0
Title = pygame.font.Font('freesansbold.ttf', 32)
MenuItem = pygame.font.Font("freesansbold.ttf", 25)

# objects
bullets = []

text = Title.render("Top Innovation Companies 2020",
                    True, light_grey, bg_color)
textRect = pygame.Rect(text.get_rect())
textRect.center = (screen_width/2, screen_height/2-60)

menu = 0
turno = 500
vida = 100
explotion = False

menuItems = []
menuItemsRects = []
menuTexts = [["Top 10 Most Innovative Compaines 2020", "by Carlos Feijoo", "source: Boston Consulting Group", "Start"],
             ["10 - Facebook", "Industry: Techology",
                 "Head Quarters: US", "Change from 2019: -2"],
             ["9 - Sony", "Industry: Consumer Goods",
                 "Head Quarters: Japan", "Change from 2019: return"],
             ["8 - IBM", "Industry: Techology",
                 "Head Quarters: US", "Change from 2019: -1"],
             ["7 - Alibaba", "Industry: Consumer Goods",
                 "Head Quarters: China", "Change from 2019: 16"],
             ["6 - Huawei", "Industry: Technology",
                 "Head Quarters: China", "Change from 2019: 42"],
             ["5 - Samsung", "Industry: Technology",
                 "Head Quarters: South Korea", "Change from 2019: 0"],
             ["4 - Microsoft", "Industry: Technology",
                 "Head Quarters: US", "Change from 2019: 0"],
             ["3 - Amazon", "Industry: Consumer Goods",
                 "Head Quarters: US", "Change from 2019: -1"],
             ["2 - Alphabet", "Industry: Technology",
                 "Head Quarters: US", "Change from 2019: -1"],
             ["1 - Apple", "Industry: Techology",
                 "Head Quarters: US", "Change from 2019: +2"],
             ["YOU WIN", "you finished the presentation", "Thanks for watching!", "Exit"]]

menuPositionsX = [[0, 0, 0, 0] for i in range(12)]
menuPositionY = [[-100, -50, 0, 50] for i in range(12)]
menuFonts = [[Title, MenuItem, MenuItem, MenuItem] for i in range(12)]

for i in range(len(menuTexts)):
    menuItem = []
    menuItemRect = []
    for j in range(len(menuTexts[i])):
        menuItem.append(menuFonts[i][j].render(
            menuTexts[i][j], True, bg_color, light_grey))
        menuItemRect.append(menuItem[j].get_rect())
        #pygame.transform.scale2x(menuItem[j].get_rect(), menuItemRect[j])
        #menuItemRect[j].length += 20
        menuItemRect[j].center = (
            screen_width / 2 + menuPositionsX[i][j], screen_height / 2 + menuPositionY[i][j])
    menuItems.append(menuItem)
    menuItemsRects.append(menuItemRect)

menu1Background = pygame.Rect(100, 170, 800, 210)
menuBackground = pygame.Rect(320, 170, 360, 210)

spaceship = pygame.transform.scale(
    pygame.image.load("./images/battleship.png"), (50, 50))
ship_x = screen_width/2 - 25
ship_y = screen_height - 100

background = pygame.transform.scale(pygame.image.load(
    "./images/Background.png"), (screen_width, screen_height))
background_x = 0
background_y = 0

explotionImage = pygame.transform.scale(
    pygame.image.load("./images/explotion.png"), (400, 400))
explotion_x = 300
explotion_y = 50

deathStars = [
    pygame.transform.scale(pygame.image.load(
        "./images/DeathStar1.png"), (400, 400)),
    pygame.transform.scale(pygame.image.load(
        "./images/DeathStar2.png"), (400, 400)),
    pygame.transform.scale(pygame.image.load(
        "./images/DeathStar3.png"), (400, 400))
]

deathStar_x = 300
deathStar_y = 0

# loop principal
while True:
    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                speed_x += 5
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                speed_x -= 5
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                speed_x -= 5
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                speed_x += 5

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if menuItemsRects[0][3].collidepoint(pos):
                vida = 0
            elif menuItemsRects[11][3].collidepoint(pos):
                pygame.quit()
                sys.exit()

    # movement
    movement()
    bulletMovement()
    logica()
    # visuals
    screen.fill(bg_color)
    screen.blit(background, (background_x, background_y))

    for bullet in bullets:
        pygame.draw.rect(screen, red, bullet[0])
        pygame.draw.rect(screen, red, bullet[1])

    screen.blit(spaceship, (ship_x, ship_y))

    if menu > 0 and menu < 6:
        screen.blit(deathStars[0], (deathStar_x, deathStar_y))
    elif menu > 5 and menu < 10:
        screen.blit(deathStars[1], (deathStar_x, deathStar_y))
    elif menu == 10:
        screen.blit(deathStars[2], (deathStar_x, deathStar_y))

    if menu == 0:
        pygame.draw.rect(screen, light_grey, menu1Background)
    else:
        pygame.draw.rect(screen, light_grey, menuBackground)

    if explotion:
        screen.blit(explotionImage, (explotion_x, explotion_y))

    for i in range(len(menuItemsRects[menu])):
        screen.blit(menuItems[menu][i], menuItemsRects[menu][i])
    # update window
    pygame.display.flip()
    clock.tick(60)
