import pygame
import math
from pygame import mixer

pygame.init()

#ScreenSize
screenW = 1280
screenH = 720

#Background Sound
mixer.music.load("Assets/sounds/backgroundsound2.mp3")
mixer.music.play(-1)

#Create Screen
screen = pygame.display.set_mode((screenW,screenH))
background = pygame.image.load("Assets/background/background.png")

#Game Title and Icon
pygame.display.set_caption("PythonCourseWithHuseyinHoca")
icon = pygame.image.load("Assets/huseyinhoca/hocaleft.png")
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)


#Player
#Player Image
playerImg = pygame.image.load("Assets/player/playerright.png")
#Player's starting X and Y coordinate
playerX = 370
playerY = 570
#Player Speed
playerX_change = 1
#Player Direction
playerdirect = "right"

#This function turns player image according to direction
def player(direct, x,y):
    if direct == "right":
        screen.blit(playerImg, (x, y))
    elif direct == "left":
        screen.blit(pygame.transform.flip(playerImg, True, False), (x, y))

# Score
playerSkor = 0
playerHealth = 3
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

#This function prints score on screen
def show_score(x, y):
    score = font.render("Score : " + str(playerSkor), True, (255, 255, 255))
    screen.blit(score, (x, y))
#This function prints healt on screen
def show_playerLive(x,y):
    live = font.render("Health : " + str(playerHealth), True, (255, 255, 255))
    screen.blit(live, (x, y))

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 150)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))

    screen.blit(over_text, (200, 300))

#Hoca
#Hoca's Image
HocaImg = pygame.image.load("Assets/huseyinhoca/hocaright.png")
#Hoca's starting X and Y coordinate
HocaX = -50
HocaY = -20
#Hoca's direction
Hocadirect = "right"
#Hoca's speed
Hocaspeed = 0.3

#This function turns hoca's image according to direction
def Hoca(direct,x,y):
    if direct == "right":
        screen.blit(HocaImg,(x,y))
    elif direct == "left":
        screen.blit(pygame.transform.flip(HocaImg, True, False),(x,y))


# "ready" means hw does not exits right now
# "drop" means hw is falling from plane
#HW
HWImg = pygame.image.load("Assets/scores/hw.png")
HWX = -200
HWY = 20
HWychange = 0.25
HW_state = "ready"
def dropHw(x,y):
    global HW_state
    HW_state = "drop"
    screen.blit(HWImg, (x+ 100, y+ 20))

# "ready" means exam does not exits right now
# "drop" means exam is falling from plane
#Exam
ExImg = pygame.image.load("Assets/scores/exam.png")
ExX = -200
ExY = 20
Exychange = 0.25
Ex_state = "ready"
def dropEx(x,y):
    global Ex_state
    Ex_state = "drop"
    screen.blit(ExImg, (x+ 100, y+ 20))


#Collision Function
def isCollision(playerX, playerY, HWX, HWY):
    distance = math.sqrt(math.pow(playerX - HWX, 2) + (math.pow(playerY - HWY, 2)))
    if distance < 80:
        return True
    else:
        return False

#Game Loop
running = True
while running:

    #Background
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        running = False

    if key[pygame.K_d]:
        playerX += playerX_change
        playerdirect = "right"
    if key[pygame.K_a]:
        playerX -= playerX_change
        playerdirect = "left"

    if Ex_state == "ready" and playerSkor % 200 == 0:
        if playerSkor != 0:
            ExX = HocaX
            ExY = HocaY
            dropEx(ExX,ExY)

    if HW_state == "ready" and Ex_state != "drop":
        HWX = HocaX
        dropHw(HWX, HWY)
        HWychange += 0.03
        if Hocaspeed < 5:
            Hocaspeed += 0.1




    #Boundaries
    if playerX < -50:
        playerX = -50
    elif playerX > 1150:
        playerX = 1150

    #Hoca Movement
    if Hocadirect == "right":
        HocaX += Hocaspeed
        if HocaX >= 1150:
            Hocadirect = "left"
    if Hocadirect == "left":
        HocaX -= Hocaspeed
        if HocaX <= -100:
            Hocadirect = "right"

    #HW Movement
    if HWY >= 700:
        HWY = 20
        HW_state = "ready"
        if playerHealth >= 0:
            failsound = mixer.Sound("Assets/sounds/failsound.mp3")
            failsound.play()
            playerHealth -= 1

    if HW_state == "drop":
        dropHw(HWX,HWY)
        HWY += HWychange

    #Exam Movement
    if ExY >= 700:
        ExY = 10000
        Ex_state = "ready"

    if Ex_state == "drop":
        dropEx(ExX,ExY)
        ExY += 0.75

    # Collision HW
    collision = isCollision(playerX, playerY, HWX, HWY)
    if collision:
        HWY = 20
        HW_state = "ready"
        playerSkor += 20
        SkorSound = mixer.Sound("Assets/sounds/scoresound.mp3")
        SkorSound.play()

    collisionEX = isCollision(playerX, playerY, ExX, ExY)
    if collisionEX:
        ExY = 350
        Ex_state = "ready"
        playerX_change += 0.5
        playerHealth += 1
        playerSkor += 20
        SkorSound = mixer.Sound("Assets/sounds/scoresound.mp3")
        SkorSound.play()


    #GameOver
    if playerHealth == -1:
        game_over_text()
        HocaY = 1000000
        HWY = 1000000
        playerY = 10000000


    Hoca(Hocadirect,HocaX,HocaY)
    player(playerdirect,playerX,playerY)
    show_score(textX, testY)
    show_playerLive(textX,testY+30)
    pygame.display.update()