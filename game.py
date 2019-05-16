import pygame
import time
from random import *
import sqlite3


blue = (113,177,227)
white = (225,225,225) #max values = 225

pygame.init()

Data = "/Users/Kante/Desktop/Data.sq3"
conn = sqlite3.connect(Data)
cur = conn.cursor()
cur.execute("create table players(score integer)")
cur.execute("insert into players(score) values(0)")
conn.commit()


surfaceW = 800
surfaceH = 500
balloonW = 50
ballonH = 66
cloudW = 300
cloudH = 300

surface = pygame.display.set_mode((surfaceW,surfaceH))
pygame.display.set_caption("Flying Balloon")
Clock = pygame.time.clock()

img = pygame.image.load('balon.png')
img_cloud_1 =pygame.image.load('cloud_1.png')
img_cloud_2 =pygame.image.load('cloud_2.png')

def  scores(account):
     police = pygame.font.Font('BradBunR.ttf',16)
     text = police.render("scores: " + str(account),True,white)
     surface.blit(text,[10,0])

def Hscores(account):
    police = pygame.font.Font('BradBunR.ttf', 16)
    text = police.render("Hscores: " + str(account), True, white)
    surface.blit(text, [700, 0])


def clouds(x_cloud,y_cloud,space):
    surface.blit(img_cloud_1,(x_cloud,y_cloud))
    surface.blit(img_cloud_2,(x_cloud,y_cloud + cloudW + space))


def replayOrQuit():
    for event in pygame.event.get([pygame.KEYDOWN ,pygame.KEYUP,pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYUP:
            continue
        return event.key
    return None

def creaTextObj(text,Police):
    textArea = Police.render(text,True,white)
    return textArea,textureArea.get_rect()


def message(text):
    GOText = pygame.font.Font('BradBunR.ttf', 150)
    smallText = pygame.font.Font('BradBunR.ttf', 20)

    GOTextSurf ,GOTextRect = creaTextObj(text,GOText)
    GOTextRect.center = surfaceW/2,((surfaceH/2)-50)
    surface.blit(GOTextSurf,GOTextRect)

    smallTextSurf, smallTextRect = creaTextObj("Press any Button to continue", smallText)

    smallTextRect.center = surfaceW / 2, ((surfaceH / 2) + 50)
    surface.blit(smallTextSurf, smallTextRect)

    pygame.display.update()
    Clock.sleep(2)


    while replayOrQuit() == None:
        Clock.tick()
    Main()

def gameOver(acutal_score):
    a = list(str(acutal_score))
    Datas="/Users/Kante/Desktop/Data.sq3"
    connex = sqlite3.connect(Datas)
    cur = connex.cursor()
    cur.execute("select * from players")
    Plist = list(cur)
    hscore=[]

    for i in range ( 0 ,len(Plist)):
        hscore +=Plist[i]

    if (int (hscore[-1]< acutal_score)):
        cur.execute("insert into players(score) values(?)",a)
        connex.commit()
        cur.close()
        connex.close()

    message("BooM!")

def balloon (x,y,image):
    surface.blit(image,(x,y))


def Main():
    x = 150
    y = 200
    y_move = 0

    x_cloud = surfaceW
    y_cloud = randint(-300,20)
    space = ballonH*3
    cloud_speed = 6
    actual_score = 0

    game_over = False

    while not game_over :
        for event in pygame.event.get():
            if event.key == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move= -5
            if event.type == pygame.KEYUP:
                y_move =5

        y += y_move

        surface.fill(blue)
        balloon(x,y,img)

        clouds(x_cloud, y_cloud, space)

        scores(actual_score)

        cur.execute("select * from players ")
        PList = list(cur)
        print(cur)
        print(PList)

        hscores =[]
        for i in range (0 , len(PList)):
            hscores += PList[i]
            print(hscores)

            hscores(hscores[-1])


        x_cloud -= cloud_speed


        if y > surfaceH -40 or y < -10 :
            gameOver(actual_score)

    if x_cloud<(-1*cloudW):
        x_cloud = surfaceW
        y_cloud = randint(-300,10)

        if 3 <= actual_score <5 :
            cloud_speed =7
            space = ballonH*2.8

        if 5 <= actual_score< 7 :
            cloud_speed =8
            space = ballonH*2.7

        if 7 <= actual_score <10:
             cloud_speed = 9
             space = ballonH*2.5

        if 10 <= actual_score <22:
            cloud_speed =11
            space =ballonH*2.2

        if 22 <= actual_score:
            cloud_speed =13
            space = ballonH*2


        if x + balloonW > x_cloud + 40 :
            if y < y_cloud + cloudH - 50 :
                if x - balloonW < x_cloud + cloudW - 20 :
                    gameOver(actual_score)

        if x + balloonW > x_cloud + 40 :
            if y + ballonH > y_cloud + cloudH + space + 50 :
                if x-balloonW < x_cloud + cloudW -20 :
                    gameOver(actual_score)



        if x_cloud < (-1*cloudW):
            x_cloud = surfaceW
            y_cloud = randint(-300,20)

            if x_cloud < (x-cloudW) < x_cloud + cloud_speed :
                actual_score += 1

        pygame.display.update()

Main()
pygame.quit()
quit()



