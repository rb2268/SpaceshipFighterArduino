'''
Name: Riley Becker
Date: 5/19/25
Project: Spaceship Fighter with Arduino Hardware/Joystick compatibility
Purpose: Add further compatibility my Python videogame to work with electrical
hardware (Joystick, LEDs, push buttons)
'''

import pygame, sys, random, math
from pygame.locals import *

import serial.tools.list_ports 

pygame.init()
serialInst = serial.Serial()
# ____________________INITIALIZE PYGAME_________________
SCREENHEIGHT = 300
SCREENWIDTH = 500
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
SKY = (144,194,202)

print("Damage:")

def runGame():
  global screen, level

  clock = pygame.time.Clock()
  fps = 60
  level = 0
  def startLevel():
    global enemyDamage, spaceShipDamage, fontTextOne, textRectOne, textSurfaceOne, enemyRespawns, countRespawns, spaceShipLives, missionFailed, enemyHealth, enemyLives, rocketBlast, rocketSpeed, enemyTwoDamage, enemyTwoHealth, enemyShipDamaged, enemyShipTwoDamaged, completionPoints, progress, fontTextTwo, textSurfaceTwo, textRectTwo, restartLevel, fontTextThree, textSurfaceThree, textRectThree, fontTextFour, textSurfaceFour, textRectFour, nextLevel, level, textRectFive, fontTextFive, textSurfaceFive, textRectSix, fontTextSix, textSurfaceSix, textRectSeven, fontTextSeven, textSurfaceSeven, textRectEight, fontTextEight, textSurfaceEight

    nextLevel = False
    restartLevel = False
    spaceShipLives = 4


    enemyDamage = 0
    spaceShipDamage = 0 #Starts on one
    enemyRespawns = 0
    countRespawns = 0

    missionFailed = 0

    enemyHealth = 5
    enemyLives = 10
    enemyTwoHealth = 2
    enemyTwoDamage = 0

    completionPoints = 20
    progress = 0

    rocketSpeed = 0
    #Rocket blast not available yet
    rocketBlast = 0
    enemyShipDamaged = False #When spaceship is hit by this enemy ship
    enemyShipTwoDamaged = False



    fontTextOne = pygame.font.SysFont('Arial', 40)
    textSurfaceOne = fontTextOne.render('Mission Unsuccessful', True, GREEN, WHITE)
    textRectOne = textSurfaceOne.get_rect()
    textRectOne.center = (SCREENWIDTH/2, SCREENHEIGHT/2)

    fontTextTwo = pygame.font.SysFont('Arial', 40)
    textSurfaceTwo = fontTextTwo.render('Restart: R', True, BLACK, WHITE)
    textRectTwo = textSurfaceTwo.get_rect()
    textRectTwo.center = (SCREENWIDTH/2 - 50, SCREENHEIGHT/2 + 50)

    fontTextThree = pygame.font.SysFont('Arial', 40)
    textSurfaceThree = fontTextThree.render('Next level: F', True, BLACK, WHITE)
    textRectThree = textSurfaceThree.get_rect()
    textRectThree.center = (SCREENWIDTH/2 - 50, SCREENHEIGHT/2 + 50)

    fontTextFour = pygame.font.SysFont('Arial', 40)
    textSurfaceFour = fontTextFour.render("Level " + str(int(level) + 1) + " Complete", True, GREEN, WHITE)
    textRectFour = textSurfaceOne.get_rect()
    textRectFour.center = (SCREENWIDTH/2, SCREENHEIGHT/2)

    fontTextFive = pygame.font.SysFont('Arial', 30)
    textSurfaceFive = fontTextFive.render("New Weapon Unlocked: ", True, BLACK, SKY)
    textRectFive = textSurfaceFive.get_rect()
    textRectFive.center = (SCREENWIDTH/2 - 90, SCREENHEIGHT/2 + 100)

    fontTextSix = pygame.font.SysFont('Arial', 40)
    textSurfaceSix = fontTextSix.render("New Enemy: ", True, BLACK, YELLOW)
    textRectSix = textSurfaceSix.get_rect()
    textRectSix.center = (SCREENWIDTH/2 - 70, SCREENHEIGHT/2 + 100)

    fontTextSeven = pygame.font.SysFont('Arial', 25)
    textSurfaceSeven = fontTextSeven.render("(Press 'X'): ", True, BLACK, SKY)
    textRectSeven = textSurfaceSeven.get_rect()
    textRectSeven.center = (SCREENWIDTH/2 - 70, SCREENHEIGHT/2 + 140)

    fontTextEight = pygame.font.SysFont('Arial', 8)
    textSurfaceEight = fontTextEight.render("(The red bar is your progress towards completing the level) ", True, WHITE)
    textRectEight = textSurfaceEight.get_rect()
    textRectEight.center = (100, 80)
  startLevel()
  screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
  #def startCoords():
  global spaceShipX, spaceShipY, spaceShipHitBox, spaceShipImage, laserBulletX, laserBulletY, laserBulletHitBox, healthBarImage, rocketBlastImage, rocketBlastX, rocketBlastY, rocketBlastHitBox, damagedImage

  spaceShipImage = pygame.image.load("spaceShip.png")
  spaceShipImage = pygame.transform.scale(spaceShipImage, (60,60))
  spaceShipX = SCREENWIDTH/4
  spaceShipY = SCREENHEIGHT*0.4
  spaceShipHitBox = pygame.Rect(spaceShipX-30, spaceShipY-20, 40, 20)
  damagedImage = pygame.image.load("spaceShipDamaged.png")
  damagedImage = pygame.transform.scale(damagedImage, (60, 60))
  laserBulletX = spaceShipX + 30
  laserBulletY = spaceShipY + 60


  rocketBlastImage = pygame.image.load("spaceShipDamaged.png")
  rocketBlastImage = pygame.transform.scale(rocketBlastImage, (40,10))
  rocketBlastX = 0
  rocketBlastY = -10
  rocketBlastHitBox = pygame.Rect(rocketBlastX, rocketBlastY, 40, 10)
  global explosionImage, explosionX, explosionY, explosionValueX, explosionValueY, explosionValueTwoX, explosionValueTwoY #Add the explosion image and coords
  explosionImage = pygame.image.load("explosion.png")
  explosionImage = pygame.transform.scale(explosionImage, (50, 50))
  explosionX = - 40
  explosionY = - 40
  explosionValueX = 1000 #Number in comparison to enemyX or enemyY ( This value starts off the screen until it is called)
  explosionValueY = 1000
  explosionValueTwoX = 1000 #Starts off the screen
  explosionValueTwoY = 1000

  global enemyX, enemyY, enemyHitBox, enemyImage, enemyImageTwo, enemyTwoX, enemyTwoY, enemyTwoHitBox

  enemyImage = pygame.image.load("enemy.png")
  enemyImage = pygame.transform.scale(enemyImage, (200,100))
  enemyX = SCREENWIDTH
  enemyY = random.randint(1,200)
  enemyHitBox = pygame.Rect(enemyX, enemyY, 200, 100)

  enemyImageTwo = pygame.image.load("anotherEnemyShip.png")
  enemyImageTwo = pygame.transform.scale(enemyImageTwo, (50, 50))
  enemyTwoX = SCREENWIDTH
  enemyTwoY = random.randint(1, SCREENHEIGHT - 50)
  enemyTwoHitBox = pygame.Rect(enemyTwoX, enemyTwoY, 50, 50)

  global backgroundImage
  backgroundImage = pygame.image.load("spaceBackground.png")
  backgroundImage = pygame.transform.scale(backgroundImage, (SCREENWIDTH,SCREENHEIGHT))
  global restartImage, forwardImage
  restartImage = pygame.image.load("restart.png")
  restartImage = pygame.transform.scale(restartImage, (80, 80))
  forwardImage = pygame.image.load("forward.png")
  forwardImage = pygame.transform.scale(forwardImage, (80, 80))
  global startImage
  startImage = pygame.image.load("start.png")
  startImage = pygame.transform.scale(startImage, (SCREENWIDTH,SCREENHEIGHT))
  global endImage
  endImage = pygame.image.load("finish.png")
  endImage = pygame.transform.scale(endImage, (300, 200))
  global newEnemyImage
  newEnemyImage = pygame.image.load("anotherEnemyShip.png")
  newEnemyImage = pygame.transform.scale(newEnemyImage, (50, 50))
  global newWeaponImage
  newWeaponImage = pygame.image.load("explosion.png")
  newWeaponImage = pygame.transform.scale(newWeaponImage, (50, 50))
  global restartLevel, nextLevel, completionPoints

  global serialInst
  
  
  while True:
    #Before the level query, determine input values from hardware
    #Joystick input
    LR = UD = 500
    serialValues = readSerial()
    # print("SerialValues: " + serialValues + "\n")
    if serialValues:
      tempTuple = separateAndConvert(serialValues)
      if LR and UD:
        LR, UD = tempTuple
      else:
        LR = UD = 500

    #This is where the different levels are
    if level == 0:
      #Controls
      handleKeyboardEvents(LR, UD)
      #Show the scene
      start()
      #UPDATE GAME
      pygame.display.update()
      clock.tick(fps)

    if level == 1:
      if restartLevel == True: #Level restarts
        startLevel()
        spaceShipX = SCREENWIDTH/4
        spaceShipY = SCREENHEIGHT*0.4
        enemyX = SCREENWIDTH
        enemyY = random.randint(1, 200)
        enemyTwoX = SCREENWIDTH
        enemyTwoY = random.randint(1, 200)
        restartLevel = False
      if nextLevel == True:
        level += 1
        command = "newLevel"
        serialInst.write(command.encode('utf-8'))
        nextLevel = False
        restartLevel = True
      #Draw screen
      drawScene()
      drawSpaceShip()
      drawEnemy()
      drawSpaceShipHealthBar()
      drawEnemyHealthBar()
      showProgressBar()
      

      #HANDLE ALL EVENTS
      handleKeyboardEvents(LR, UD)
      collisions()
      fails()    
      endLevel()

      #UPDATE THE GAME

      moveEnemy()
      pygame.display.update()

      clock.tick(fps)
    if level == 2:
      if restartLevel == True: #Level restarts
        startLevel()
        spaceShipX = SCREENWIDTH/4
        spaceShipY = SCREENHEIGHT*0.4
        enemyX = SCREENWIDTH
        enemyY = random.randint(1, 200)
        enemyTwoX = SCREENWIDTH
        enemyTwoY = random.randint(1, 200)
        completionPoints = 75
        restartLevel = False
      if nextLevel == True:
        level += 1
        nextLevel = False
        restartLevel = True
      #Draw screen
      drawScene()
      drawSpaceShip()
      drawEnemy()
      drawSpaceShipHealthBar()
      drawEnemyHealthBar()
      rocketBlastSpeed()
      drawRocketBlast()
      #drawAnotherEnemy()
      showProgressBar()
      

      #HANDLE ALL EVENTS
      handleKeyboardEvents(LR, UD)
      collisions()
      fails()    
      endLevel()

      #UPDATE THE GAME

      moveEnemy()
      pygame.display.update()

      clock.tick(fps)

    if level == 3:
      if restartLevel == True: #Level restarts
        startLevel()
        spaceShipX = SCREENWIDTH/4
        spaceShipY = SCREENHEIGHT*0.4
        enemyX = SCREENWIDTH
        enemyY = random.randint(1, 200)
        enemyTwoX = SCREENWIDTH
        enemyTwoY = random.randint(1, 200)
        completionPoints = 110
        restartLevel = False
      if nextLevel == True:
        level += 1
        nextLevel = False
      #Draw screen
      drawScene()
      drawSpaceShip()
      drawEnemy()
      drawSpaceShipHealthBar()
      drawEnemyHealthBar()
      drawRocketBlast()
      rocketBlastSpeed()
      drawAnotherEnemy()
      showProgressBar()

      #HANDLE ALL EVENTS
      handleKeyboardEvents(LR, UD)
      collisions()
      fails()    
      endLevel()

      #UPDATE THE GAME

      moveEnemy()
      pygame.display.update()

      clock.tick(fps)
    if level == 4:
      drawScene()
      finishGame()
      pygame.display.update()

      clock.tick(fps)

#Notifies the player they have completed the game
def finishGame():
  global endImage
  screen.blit(endImage, (66, 50))

#Shows the directions on how to play the game
def start():
  global startImage, textRectEight, textSurfaceEight, serialInst
  #Signal the game is on by lighting the green LED
  # command = "Blink"
  # serialInst.write(command.encode('utf-8'))
  command = "ON"
  serialInst.write(command.encode('utf-8'))
  screen.fill(WHITE)
  screen.blit(startImage, (0, 0))
  screen.blit(textSurfaceEight, textRectEight)
  pygame.draw.rect(screen, RED, (5, 90, 100, 3), 0)

#The player completes a level
def endLevel():
  global missionFailed, restartImage, restartHitBox, textSurfaceTwo, textRectTwo, progress, completionPoints, textSurfaceThree, textRectThree, textSurfaceFour, textRectFour, nextLevel
  if missionFailed >= 1: #When the spaceship loses all of its lives
    #screen.blit(restartImage, (70, 150))
    #restartHitBox = pygame.Rect(70, 150, 70, 70)
    screen.blit(textSurfaceTwo, textRectTwo)
    nextLevel = False
    progress = 0
  if progress >= completionPoints:
    screen.blit(textSurfaceThree, textRectThree)
    screen.blit(textSurfaceFour, textRectFour)

#The amount of progress a player has in a level
def showProgressBar():
  global progress, completionPoints
  pygame.draw.rect(screen, SKY, (50, 10, 300, 5), 0)
  #Increment of the health bar
  pygame.draw.rect(screen, RED, (50, 10, 300 - (300 * (progress / completionPoints)), 5), 0) #Progress bar at the top of screen

#Draws the rocket blast
def drawRocketBlast():
  global rocketBlastX, rocketBlastY, spaceShipX, spaceShipY, rocketBlastImage, rocketBlastHitBox, rocketBlast

  screen.blit(rocketBlastImage, (rocketBlastX, rocketBlastY))
  if rocketBlast == 1:
    rocketBlastHitBox = pygame.Rect(rocketBlastX, rocketBlastY, 40, 10)

#Slowly drops the rocket blast
def rocketBlastSpeed():
  global rocketBlastX, rocketBlastY, rocketSpeed, spaceShipX
  if rocketBlast == 1:
    rocketBlastX += 3
    rocketBlastY += 1

#Draws the enemy health bar
def drawEnemyHealthBar():
  global healthBarImage, enemyX, enemyY, enemyDamage, enemyLives, enemyHealth
  #screen.blit(healthBarImage, (spaceShipX+20,spaceShipY-20))
  pygame.draw.rect(screen, WHITE, (enemyX + (200/2), enemyY - 20, 30, 10), 0)
  #Increment of the health bar
  pygame.draw.rect(screen, RED, (enemyX + (200/2), enemyY - 20, 30 - 30 * (enemyDamage / enemyHealth), 10), 0)

#The result of failing to complete a level
def fails():
  global missionFailed, textSurfaceOne, textRectOne 
  if missionFailed >= 1: #When the spaceship loses all of its lives
    screen.blit(textSurfaceOne, textRectOne)

#When the spaceship or weapon collides with the enemy
def collisions():
  global enemyHitBox, spaceShipX, spaceShipY, spaceShipHitBox, laserBulletX, laserBulletY, spaceShipDamage, fontTextOne, textSurfaceOne, textRectOne, enemyRespawns, spaceShipLives, missionFailed, spaceShipLives, enemyDamage, enemyX, enemyY, enemyHealth, level, enemyTwoHitBox, enemyTwoDamage, enemyShipDamaged, enemyShipTwoDamaged


  if spaceShipDamage == spaceShipLives:
    missionFailed += 1
    screen.blit(damagedImage, (spaceShipX,spaceShipY))

  
  if spaceShipDamage <= enemyRespawns and (spaceShipHitBox.colliderect(enemyHitBox) or spaceShipHitBox.colliderect(enemyTwoHitBox)):
    spaceShipDamage += 1
    #if spaceShipDamage <= spaceShipLives:
      #print(spaceShipDamage)
    if spaceShipHitBox.colliderect(enemyHitBox): #If spaceship collides with enemyOne, the spaceship counts its damage for that specific enemy
      enemyShipDamaged = True
    if spaceShipHitBox.colliderect(enemyTwoHitBox): #If spaceship collides with enemytwo, the spaceship counts its damage for that specific enemy
      enemyShipTwoDamaged = True
    if spaceShipDamage == spaceShipLives:
      print("Game Over")
   

    
  if laserBulletHitBox.colliderect(enemyHitBox):   #Enemy is damaged
    enemyHitBox = pygame.Rect(enemyX, enemyY, 200, 100)
    enemyDamage += 1
    spaceShipHitBox = pygame.Rect(spaceShipX, spaceShipY, 60, 60)
  if laserBulletHitBox.colliderect(enemyTwoHitBox):
    enemyTwoDamage += 1
    enemyTwoHitBox = pygame.Rect(enemyTwoX, enemyTwoY, 50, 50)
  
  global explosionValueX, explosionValueY, progress
  if enemyDamage >= enemyHealth: #If the enemy is destroyed
    screen.blit(explosionImage, (explosionValueX + enemyX, explosionValueY + enemyY))
    explosionValueX = 1000
    enemyX = SCREENWIDTH + 200
    enemyY = random.randint(0,SCREENHEIGHT-100)
    enemyDamage = 0
    enemyHitBox = pygame.Rect(enemyX, enemyY, 200, 100)
    enemyHealth = 5
    progress += 2
    if spaceShipDamage > enemyRespawns and enemyShipDamaged == True:
      enemyRespawns += 1
      enemyShipDamaged = False
      

  global rocketBlastHitBox, rocketBlastX, rocketBlastY, drawRocketBlast, rocketBlast, explosionX, explosionY, explosionHitBox, explosionValueTwoX, explosionValueTwoY

  if rocketBlastHitBox.colliderect(enemyHitBox):
    explosionX = rocketBlastX
    explosionY = rocketBlastY
    rocketBlastX = SCREENWIDTH + 500
    rocketBlastY = SCREENHEIGHT + 500 #Sends the rocket blast out of screen
    enemyDamage += 2
    explosionValueX = explosionX - enemyX #Makes the coordinate compare to enemyX
    explosionValueY = explosionY - enemyY
  if rocketBlastHitBox.colliderect(enemyTwoHitBox):
    explosionX = rocketBlastX
    explosionY = rocketBlastY
    rocketBlastX = SCREENWIDTH + 500
    rocketBlastY = SCREENHEIGHT + 500
    enemyTwoDamage += 2
    explosionValueTwoX = explosionX - enemyTwoX #Makes the coordinate compare to enemyX
    explosionValueTwoY = explosionY - enemyTwoY

#Moves the enemy to the left
def moveEnemy():
  global enemyImage, enemyX, enemyY, spaceShipDamage, enemyRespawns, explosionValueX, explosionValueY, enemyTwoX, enemyTwoY, explosionValueTwoX, explosionValueTwoY, enemyShipDamaged, enemyShipTwoDamaged, level
  if level == 2:
    enemyX -= 6
  else:
    enemyX -= 5
  if enemyX < -200: #Enemy goes off the screen
    enemyX = SCREENWIDTH
    if spaceShipDamage > enemyRespawns and enemyShipDamaged == True:
      enemyRespawns += 1
      enemyShipDamaged = False
    enemyY = random.randint(0,SCREENHEIGHT-100)
    explosionValueX = -1000
  if enemyTwoX < -50: #The second enemy goes off the screen
    explosionValueTwoX = -1000
    enemyTwoX = SCREENWIDTH
    enemyTwoY = random.randint(0, SCREENHEIGHT - 50)
    if spaceShipDamage > enemyRespawns and enemyShipTwoDamaged == True:
      enemyRespawns += 1
      enemyShipTwoDamaged = False
    
#Draws the second enemy
def drawAnotherEnemy():
  global enemyImageTwo, enemyTwoX, enemyTwoY, enemyTwoHitBox, explosionValueTwoX, enemyRespawns, explosionValueTwoY, progress, enemyShipTwoDamaged
  screen.blit(enemyImageTwo, (enemyTwoX, enemyTwoY))
  #Moves the enemy 
  enemyTwoX -= 7
  #Draws the health bar 
  global enemyLives, enemyHealth, enemyTwoDamage, enemyTwoHealth
  pygame.draw.rect(screen, WHITE, (enemyTwoX + (50/2), enemyTwoY - 20, 30, 10), 0)
  #Increment of the health bar
  pygame.draw.rect(screen, RED, (enemyTwoX + (50/2), enemyTwoY - 20, 30 - 30 * (enemyTwoDamage / enemyTwoHealth), 10), 0)
  #If the enemy is destroyed
  if enemyTwoDamage >= enemyTwoHealth:
    screen.blit(explosionImage, (explosionValueX + enemyX, explosionValueY + enemyY))
    enemyTwoX = SCREENWIDTH + 50
    enemyTwoY = random.randint(0,SCREENHEIGHT-50)
    enemyTwoDamage = 0
    enemyTwoHitBox = pygame.Rect(enemyTwoX, enemyTwoY, 50, 50)
    enemyTwoHealth = 2
    explosionValueTwoX = 1000 #Explosion image disseapears
    progress += 2
    if spaceShipDamage > enemyRespawns and enemyShipTwoDamaged == True:
      enemyRespawns += 1
      enemyShipTwoDamaged = False
  #Draw the hitbox
  enemyTwoHitBox = pygame.Rect(enemyTwoX, enemyTwoY, 50, 50)
  #Draw the explosion
  screen.blit(explosionImage, (explosionValueTwoX + enemyTwoX, explosionValueTwoY + enemyTwoY))
  
#Draws the first enemy ship
def drawEnemy():
  global enemyImage, enemyX, enemyY, enemyHitBox, explosionX, explosionY, explosionImage, explosionValueX, explosionValueY
  screen.blit(enemyImage, (enemyX, enemyY))
  enemyHitBox = pygame.Rect(enemyX, enemyY, 200, 100)
  screen.blit(explosionImage, (explosionValueX + enemyX, explosionValueY + enemyY))
  
#Events on the keyboard; makes the spaceship move, fires the lasers and handles keys to restart and progress through levels
def handleKeyboardEvents(LR, UD):
  global spaceShipX, spaceShipY, laserBulletX, laserBulletY, missionFailed, restartLevel, progress, completionPoints, level, nextLevel, spaceShipDamage, textSurfaceFive, textRectFive, textSurfaceSix, textRectSix, newWeaponImage, newEnemyImage, textRectSeven, textSurfaceSeven

  drawLaserBullet()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  key = pygame.key.get_pressed()
  if UD < 100 and spaceShipY > 0:
    spaceShipY -= 5
  
  if UD > 900 and spaceShipY < 240:
    spaceShipY += 5
  
  if LR < 100 and spaceShipX > 0:
    spaceShipX -= 5
  
  if LR > 900 and spaceShipX < 440:
    spaceShipX += 5
  
  if missionFailed >= 1: #When the spaceship loses all of its lives
    if key[pygame.K_r]:
      restartLevel = True
  if progress >= completionPoints: #When the spaceship completes the level
    spaceShipDamage = 0
    if level == 1:
      screen.blit(textSurfaceFive, textRectFive)
      screen.blit(newWeaponImage, (320, 220))
      screen.blit(textSurfaceSeven, textRectSeven)
    if level == 2:
      screen.blit(textSurfaceSix, textRectSix)
      screen.blit(newEnemyImage, (320, 220))
    if key[pygame.K_f]:
      nextLevel = True
    
  if level == 0 and key[pygame.K_f]:
    level = 1
  global laserBulletHitBox, enemyHitBox, enemyX, enemyY, enemyDamage, enemyHealth, spaceShipHitBox

  if laserBulletHitBox.colliderect(enemyHitBox) or laserBulletHitBox.colliderect(enemyTwoHitBox):
    if key[pygame.K_SPACE]: #Laser bullet respawns
      laserBulletX = spaceShipX + 45
      laserBulletY = spaceShipY + 30
      enemyHitBox = pygame.Rect(enemyX, enemyY, 200, 100)
    else:
      #Laser dissapears when it reaches the enemy but space bar isn't pressed
      laserBulletY = - 10

  if not laserBulletHitBox.colliderect(spaceShipHitBox) and not key[pygame.K_SPACE]: #When space bar is not pressed, the laser continues its path
    moveLaser()
  if key[pygame.K_SPACE]: #Shoots lasers
    if laserBulletX > SCREENWIDTH:
      laserBulletX = spaceShipX + 45
      laserBulletY = spaceShipY + 30
    moveLaser()
    

  global rocketBlast, rocketBlastX, rocketBlastY
  if key[pygame.K_x]:
    if rocketBlast != 1:
      rocketBlastX = spaceShipX + 45
      rocketBlastY = spaceShipY + 30
    rocketBlast = 1
  rocketBlastSpeed()
  if rocketBlastX > SCREENWIDTH or rocketBlastY > SCREENHEIGHT:
    rocketBlast = 0

  pygame.draw.rect(screen, BLUE, spaceShipHitBox, 1)
  pygame.draw.rect(screen, RED, enemyHitBox, 1)
  pygame.draw.rect(screen, RED, enemyTwoHitBox, 1)

#Draws the laser bullet
def drawLaserBullet():
  global laserBulletX, laserBulletY, spaceShipX, spaceShipY, laserBulletHitBox
  #Draw lasers with coordinates
  pygame.draw.circle(screen, WHITE, (laserBulletX,laserBulletY), 4, 0)
  laserBulletHitBox = pygame.Rect(laserBulletX, laserBulletY, 4, 4)

#Makes the lasers move
def moveLaser():
  global laserBulletX, laserBulletY
  
  laserBulletX = laserBulletX + 10

#Draws the spaceship health bar
def drawSpaceShipHealthBar():
  global healthBarImage, spaceShipX, spaceShipY, spaceShipDamage, spaceShipLives
  #screen.blit(healthBarImage, (spaceShipX+20,spaceShipY-20))
  pygame.draw.rect(screen, WHITE, (spaceShipX + 20, spaceShipY - 20, 30, 10), 0)
  #Increment of the health bar
  pygame.draw.rect(screen, BLUE, (spaceShipX + 20, spaceShipY - 20, 30 - 30 * (spaceShipDamage / spaceShipLives), 10), 0)

#Makes the scene
def drawScene():
  global backgroundImage
  screen.fill(WHITE)
  screen.blit(backgroundImage, (0,0))

#Draws the spaceship
def drawSpaceShip():
  global spaceShipImage, spaceShipX, spaceShipY, spaceShipHitBox, damagedImage
  screen.blit(spaceShipImage, (spaceShipX,spaceShipY))
  spaceShipHitBox = pygame.Rect(spaceShipX, spaceShipY, 60, 60)
  if enemyShipDamaged == True or enemyShipTwoDamaged == True:
    screen.blit(damagedImage, (spaceShipX,spaceShipY))

#Initializes PySerial
def initPySerial():
  ports = serial.tools.list_ports.comports()
  portsList = []

  for one in ports:
    portsList.append(str(one))
    print(str(one))

  #Import the port attatched to either IOUSBHOSTDEVICE (not wifi or bluetooth 
  # or n/a)
  #Example—type: "usbmodem142301" for "/dev/cu.usbmodem142301 - IOUSBHostDevice"
  portName = input("Select ports for Arduino # ")
  use = ""
  for i in range(len(portsList)):
    if portsList[i].startswith("/dev/cu." + str(portName)):
      use = "/dev/cu." + str(portName)
      print(use)
  try:
    serialInst.baudRate = 9600
    serialInst.port = use
    serialInst.open()
  except serial.SerialException as e:
    print(f"Failed to open board at serial port {e}")
    exit()
  return

def readSerial():
    lineString = ""
    if serialInst.in_waiting:
        packet = serialInst.readline()
        lineString = packet.decode('utf')
    return lineString

#Separates two integers from a string (input) and outputs them as a tuple
def separateAndConvert(input_string):
  try:
      str1, str2 = input_string.split(',')
      int1 = int(str1)
      int2 = int(str2)
      return int1, int2
  except ValueError:
      return None
    
#Initializes Serial Monitor and runs the game
initPySerial()
runGame()
serialInst.close()