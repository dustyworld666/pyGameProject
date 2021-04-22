import pygame
import random
import math
from pygame import mixer


#initialize the game
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#TITLE AND ICON
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space-ship.png')
pygame.display.set_icon(icon)

#Background
background = pygame.image.load('space2.png')

#background music
mixer.music.load('alien_dream.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('spaceship1.png')
playerX = 370
playerY = 480
playerX_change = 0


# enemy 
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.1)
    enemyY_change.append(40)


#Ready - You cant see the bullet on the screeen
#fire - The bullet is currently moving
# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

#score card
score_value = 0
font = pygame.font.Font('ZenDots-Regular.ttf', 32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('ZenDots-Regular.ttf', 64)


#show score
def show_score(x, y):
    score = font.render("Score :" + str(score_value),True, (255, 255, 255))
    screen.blit(score, (x, y))

#over function
def game_over_text():
    over_text = over_font.render("GAME OVER",True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#Bullet state
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


#collision funcion
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


#Player Function
def player(x, y):
    screen.blit(playerImg, (playerX, playerY))


#Enemy Function
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))


# GAME LOOP
running = True
while running:
    #rgb red, green, blue
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.9
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.9
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser_shot.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                playerX_change = 0
    
    #player movement
    playerX += playerX_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #enemy movement
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('bomb_explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)
    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

