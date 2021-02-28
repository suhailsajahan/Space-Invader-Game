import pygame
import math
import random
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")
# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# caption and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("logo32.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_Change = 0
playerY_Change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
numberOfEnemies = 2

for i in range(numberOfEnemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(20, 150))
    enemyX_Change.append(4)
    enemyY_Change.append(40)

# bomb
# ready - you can't see the bomb on screen
# fire - bomb is currently moving
bombImg = pygame.image.load("bomb16.png")
bombX = playerX
bombY = playerY
bombX_Change = 0
bombY_Change = 5
bomb_state = "ready"

# score
score_value = 0
font = pygame.font.Font('aAlloyInk.ttf', 32)
textX = 10
textY = 10

# Game over text
gameOver_font = pygame.font.Font('aAlloyInk.ttf', 64)
isGameOver = False

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def gameOverText():
    gameOver_text = gameOver_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(gameOver_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bomb(x, y):
    global bomb_state
    bomb_state = "fire"
    screen.blit(bombImg, (x + 24, y + 10))


def isCollision(enemyX, enemyY, bombX, bombY):
    distance = math.sqrt((math.pow(enemyX - bombX, 2)) + (math.pow(enemyY - bombY, 2)))
    if distance < 27:
        return True
    else:
        return False


def isDamaged(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2)))
    if distance < 75:
        return True
    else:
        return False


# Game loop
running = True

while running:

    # RGB
    screen.fill((150, 185, 255))
    # background image
    screen.blit(background, (0, 0))

    player(playerX, playerY)
    show_score(textX, textY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -2
            if event.key == pygame.K_RIGHT:
                playerX_Change = 2
            if event.key == pygame.K_UP:
                playerY_Change = -2
            if event.key == pygame.K_DOWN:
                playerY_Change = 2
            if event.key == pygame.K_SPACE:
                if bomb_state == "ready":
                    bomb_Sound = mixer.Sound('laser.wav')
                    bomb_Sound.play()
                    bombX = playerX
                    bombY = playerY
                    fire_bomb(bombX, bombY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_Change = 0

    # checking the boundary of spaceship
    playerX += playerX_Change
    playerY += playerY_Change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    if playerY >= 536:
        playerY = 536

    # enemy movement
    for i in range(numberOfEnemies):
        # Game over
        if isDamaged(enemyX[i], enemyY[i], playerX, playerY):
            for j in range(numberOfEnemies):
                enemyY[j] = 2000
            isGameOver = True
            break

        if isGameOver:
            gameOverText()

        enemyX[i] += enemyX_Change[i]
        # enemyY[i] += enemyY_Change[i]

        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_Change[i] = (-1) * enemyX_Change[i]
            enemyY[i] += enemyY_Change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bombX, bombY)
        if collision:
            collision_Sound = mixer.Sound('explosion.wav')
            collision_Sound.play()
            bombY = playerY
            bomb_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(20, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bomb movement
    if bombY <= 0:
        bombY = playerY
        bomb_state = "ready"
    if bomb_state == "fire":
        fire_bomb(bombX, bombY)
        bombY -= bombY_Change


    pygame.display.update()
