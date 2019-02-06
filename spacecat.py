import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
magenta = (255, 0, 255)
blue = (5, 46, 76)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Space Cat')
icon = pygame.image.load('cat_icon.png')
pygame.display.set_icon(icon)

img = pygame.image.load("cat1_resized.png")
doughnut = pygame.image.load("Space_Doughnut_Animated50x50.gif")
background = pygame.image.load("background.jpg")
menu_background = pygame.image.load("menu_background.jpg")

clock = pygame.time.Clock()

AppleThickness = 50

block_size = 40

FPS = 10

direction = "right"

smallfont = pygame.font.SysFont("consolas", 20)
medfont = pygame.font.SysFont("consolas", 50)
largefont = pygame.font.SysFont("impact", 80)


def pause():
    paused = True
    message_to_screen("Paused", white, -100, size="medium")
    message_to_screen("Press C to continue or Q to quit", white, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == K_q:
                    pygame.quit()
                    quit()

        # gameDisplay.fill(white)
        clock.tick(5)


def score(score):
    text = smallfont.render("Score: " + str(score), True, white)
    gameDisplay.blit(text, [0, 0])


def randDoughnutGen():
    randDoughnutX = round(random.randrange(
        0, display_width - AppleThickness))
    randDoughnutY = round(random.randrange(
        0, display_height - AppleThickness))

    return randDoughnutX, randDoughnutY


def game_intro():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(blue)
        gameDisplay.blit(menu_background, (0, 0))
        message_to_screen("Welcome to Space Cat", green, -100, size="medium")
        message_to_screen(
            "The objective is to eat as many space doughnuts as you can", black, -30)
        message_to_screen(
            "The more you eat, the longer your space trail would be", black, 10)
        message_to_screen(
            "If you run into your trail or into the edges - the game will end", black, 50)
        message_to_screen(
            "Press C to play P to pause or Q to quit", black, 180)

        pygame.display.update()
        clock.tick(15)


def snake(block_size, snakeList):
    if direction == "right":
        head = img
    if direction == "left":
        head = pygame.transform.flip(img, True, False)
    if direction == "up":
        head = pygame.transform.rotate(img, 90)
    if direction == "down":
        head = pygame.transform.rotate(img, 270)
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, magenta, [
                         XnY[0], XnY[1], block_size, block_size])


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg: object, color: object, y_displace: object = 0, size: object = "small") -> object:
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    global direction

    direction = 'right'
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randDoughnutX, randDoughnutY = randDoughnutGen()

    while not gameExit:
        if gameOver == True:
            message_to_screen("GAME OVER!", red, -50, size="large")
            message_to_screen("Your score is " +
                              str(snakeLength - 1), white, 100, size="small")
            message_to_screen(
                "Press C to play again or press Q to quit", white, 150, size="small")
            pygame.display.update()

        while gameOver == True:
            # gameDisplay.fill(white)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.blit(background, (0, 0))
        gameDisplay.blit(doughnut, (randDoughnutX, randDoughnutY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)

        score(snakeLength - 1)

        pygame.display.update()

        if lead_x > randDoughnutX and lead_x < randDoughnutX + AppleThickness or lead_x + block_size > randDoughnutX and lead_x + block_size < randDoughnutX + AppleThickness:
            if lead_y > randDoughnutY and lead_y < randDoughnutY + AppleThickness:
                randDoughnutX, randDoughnutY = randDoughnutGen()
                snakeLength += 1

            elif lead_y + block_size > randDoughnutY and lead_y + block_size < randDoughnutY + AppleThickness:
                randDoughnutX, randDoughnutY = randDoughnutGen()
                snakeLength += 1

        clock.tick(FPS)

    pygame.quit()
    quit()


game_intro()
gameLoop()
