# -*- coding: utf-8 -*-
from json.encoder import INFINITY
import pygame
from pygame import mixer
from pygame.locals import *
import sys
import random

def main():
    pygame.init()
    mixer.init()
    screen = pygame.display.set_mode((600, 400))
    bg = pygame.transform.scale(pygame.image.load("images/bg.jpg"), (600, 400))
    bikkuri = pygame.image.load("images/bikkuri.png").convert_alpha()
    gorilla1 = pygame.image.load("images/gorilla1.png").convert_alpha()
    gorilla2 = pygame.image.load("images/gorilla2.png").convert_alpha()
    miss = pygame.image.load("images/miss.png").convert_alpha()
    win = pygame.image.load("images/win.png").convert_alpha()
    lose = pygame.image.load("images/lose.png").convert_alpha()
    cutin = pygame.image.load("images/cutin.png").convert_alpha()
    font = pygame.font.Font(None, 30)
    menufont = pygame.font.Font(None, 60)
    lefttime = 0
    enemytime = 0

    status = -1 # -1:menu 0:fight 1:win 2:miss 3:lose
    flying = 0
    timer = 0
    timer_end = False
    return_wait = 0

    menu = 0

    while(True):
        timer -= 1
        if return_wait > 0:
            return_wait -= 1
        if status == -1:
            screen.fill((0,0,0))
            text = menufont.render("EASY", True, (255,255,255))
            screen.blit(text, [250, 100])
            text = menufont.render("HARD", True, (255,255,255))
            screen.blit(text, [250, 200])
            text = menufont.render("HELL", True, (255,255,255))
            screen.blit(text, [250, 300])
            text = menufont.render(">", True, (255,255,255))
            screen.blit(text, [200, 100*(menu+1)])
        else:
            screen.blit(bg, (0, 0))
        if status == 0:
            screen.blit(gorilla1, (50, 250))
            screen.blit(gorilla2, (550-gorilla2.get_rect()[2], 250))
            lefttime -= 1
            if lefttime <= 0:
                screen.blit(bikkuri, (300-bikkuri.get_rect()[2]/2, 200-bikkuri.get_rect()[3]/2))
        if status == 1:
            if timer == 0:
                if timer_end == False:
                    gorilla1 = pygame.image.load("images/gorilla_win.png").convert_alpha()
                    timer_end = True
                else:
                    gorilla1 = pygame.transform.flip(gorilla1, True, False)
                timer = 20
            if timer < 0 and timer_end == False:
                timer = 75
            screen.blit(win, (300-win.get_rect()[2]/2, 200-win.get_rect()[3]/2))
            screen.blit(gorilla1, (200, 250))
            screen.blit(pygame.transform.rotate(gorilla2, 270), (400-gorilla2.get_rect()[2]+flying, 200-flying))
            flying += 15
        if status == 2:
            if timer == 0:
                lefttime = random.randint(100, 200)
                mixer.music.load("sounds/wind.mp3")
                mixer.music.play(1)
                status = 0
            if timer < 0:
                timer = 200
            screen.blit(miss, (300-miss.get_rect()[2]/2, 200-miss.get_rect()[3]/2))
        if status == 3:
            screen.blit(lose, (300-lose.get_rect()[2]/2, 200-lose.get_rect()[3]/2))
            screen.blit(pygame.transform.rotate(gorilla1, 90), (200-flying, 200-flying))
            screen.blit(gorilla2, (400-gorilla2.get_rect()[2], 250))
            flying += 15
        if lefttime == 0 and status == 0:
            mixer.music.stop()
            mixer.music.load("sounds/go.mp3")
            mixer.music.play(1)
        if lefttime < 0:
            text = font.render(str(-lefttime), True, (0,0,0))
            screen.blit(text, [373, 335])
            if -lefttime > enemytime and status == 0:
                mixer.music.load("sounds/lose.mp3")
                mixer.music.play(1)
                status = 3
                return_wait = 50
        pygame.display.update()
        pygame.time.wait(15)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE and status == 0:
                    if lefttime <= 0:
                        mixer.music.load("sounds/win.mp3")
                        mixer.music.play(1)
                        status = 1
                    else:
                        mixer.music.load("sounds/miss.mp3")
                        mixer.music.play(1)
                        status = 2
                elif event.key == K_SPACE and status == -1:
                    if menu == 0:
                        enemytime = random.randint(24, 28)
                    if menu == 1:
                        enemytime = random.randint(16, 20)
                    if menu == 2:
                        enemytime = random.randint(11, 13)
                    status = 0
                    flying = 0
                    mixer.music.load("sounds/ready.mp3")
                    mixer.music.play(1)
                    screen.blit(bg, (0, 0))
                    screen.blit(gorilla1, (50, 250))
                    screen.blit(gorilla2, (550-gorilla2.get_rect()[2], 250))
                    screen.blit(cutin, (0, 0))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    mixer.music.load("sounds/wind.mp3")
                    mixer.music.play(1)
                    lefttime = random.randint(150, 250)
                elif event.key == K_SPACE and (status == 1 or status == 3) and return_wait <= 0:
                    lefttime = 0
                    timer_end = False
                    status = -1
                if event.key == K_DOWN:
                    menu = (menu+1)%3
                if event.key == K_UP:
                    menu = (menu+2)%3
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()