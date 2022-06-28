# -*- coding: utf-8 -*-
from json.encoder import INFINITY
import pygame
from pygame import mixer
from pygame.locals import *
import sys
import math
import random

DEBUG = False # FalseからTrueにするとTimerとかを見れます
FRAME_MIN = 200 # !マークが出るまでの時間の下限
FRAME_MAX = 350 # !マークが出るまでの時間の上限
ENEMY_FRAME = [40, 25, 18, 13, 10] # 敵が反応するまでの時間，左からEASY，NORMAL，HARD，HELL，IMPOSSIBLE

def main():
    pygame.init()
    mixer.init()
    screen = pygame.display.set_mode((600, 400))
    img_title = pygame.transform.scale(pygame.image.load("images/title.jpg"), (600, 400))
    img_bg = pygame.transform.scale(pygame.image.load("images/bg.jpg"), (600, 400))
    img_audience = pygame.transform.scale(pygame.image.load("images/audience.png"), (600, 400))
    img_bikkuri = pygame.image.load("images/bikkuri.png").convert_alpha()
    img_gorilla = pygame.image.load("images/gorilla1.png").convert_alpha()
    img_enemy = pygame.image.load("images/enemy1.png").convert_alpha()
    img_badgorilla = pygame.image.load("images/gorilla2.png").convert_alpha()
    img_miss = pygame.image.load("images/miss.png").convert_alpha()
    img_win = pygame.image.load("images/win.png").convert_alpha()
    img_lose = pygame.image.load("images/lose.png").convert_alpha()
    img_cutin = pygame.image.load("images/cutin.png").convert_alpha()
    img_tip = pygame.image.load("images/tip.png").convert_alpha()
    font = pygame.font.Font(None, 30)
    font_menu = pygame.font.Font(None, 60)
    left_frame = 0 # !マークが出るまでの時間
    finish_frame = 0
    enemy_frame = 0 # 敵が反応するまでの時間
    game_status = "menu" # menuの時はメニュー画面，fightの時はゲーム中，winの時は勝った時，loseの時は負けた時，missの時はおてつきした時
    flying_dist = 0
    timer = 0
    timer_return = 0
    select_menu = 0
    cleared = [0, 0, 0, 0, 0]
    menu_num = 3 # 難易度の数，初めは3，HELL開放で4，IMPOSSIBLE開放で5

    while(True):
        timer -= 1 # 各種タイマーを1減らす
        timer_return -= 1
        left_frame -= 1

        if game_status == "menu": # メニュー画面
            screen.blit(img_title, [0, 0])
            text = font_menu.render("EASY", True, (255,255,255))
            screen.blit(text, [250, 100])
            text = font_menu.render("NORMAL", True, (255,255,255))
            screen.blit(text, [250, 150])
            text = font_menu.render("HARD", True, (255,255,255))
            screen.blit(text, [250, 200])
            if menu_num >= 4: # 解禁済みなら色を変える，(100,100,100)はグレー(未解禁)，(255,255,255)は白(解禁済み)
                text = font_menu.render("HELL", True, (255,255,255))
            else:
                text = font_menu.render("HELL", True, (100,100,100))
            screen.blit(text, [250, 250])
            if menu_num >= 5: # 解禁済みなら表示
                text = font_menu.render("IMPOSSIBLE", True, (255,100,100))
                screen.blit(text, [250, 300])
            text = font_menu.render(">", True, (255,255,255)) # カーソル
            screen.blit(text, [150, 50*(select_menu+2)-5])
            for stage in range(5):
                if cleared[stage] == 1:
                    text = font_menu.render("X", True, (255,50,50))
                    screen.blit(text, [200, 50*(stage+2)])
                if cleared[stage] == 2:
                    text = font_menu.render("O", True, (50,255,50))
                    screen.blit(text, [200, 50*(stage+2)])

        elif game_status == "fight": # ゲーム中
            screen.blit(img_bg, [0, 0])
            screen.blit(img_audience, (0, -70))
            if DEBUG:
                text = font.render(str(left_frame), True, (100,100,100))
                screen.blit(text, [373, 335])
            screen.blit(img_gorilla, (50, 250))
            screen.blit(img_enemy, (550-img_enemy.get_rect()[2], 250))
            screen.blit(img_badgorilla, (600-img_enemy.get_rect()[2], 300))
            if timer > 0: # カットイン中なら
                screen.blit(img_cutin, [0, 0])
            if timer == 0: # カットインが終わった瞬間に1回だけ
                mixer.music.load("sounds/wind.mp3")
                mixer.music.play(1)
                left_frame = random.randint(FRAME_MIN, FRAME_MAX) # !マークが出るまでの時間をランダムに決める
            if left_frame == 0: # !マークが出た瞬間に1回だけ
                mixer.music.load("sounds/go.mp3")
                mixer.music.play(1)
            if left_frame <= 0 and timer < 0: # !マークが出ているなら
                finish_frame = -left_frame
                screen.blit(img_bikkuri, (300-img_bikkuri.get_rect()[2]/2, 200-img_bikkuri.get_rect()[3]/2))
                text = font.render(str(finish_frame), True, (0,0,0)) # 看板に時間を表示
                screen.blit(text, [373, 335])
                if -left_frame >= enemy_frame and game_status == "fight": # !マークが出てから敵が反応したら
                    mixer.music.load("sounds/lose.mp3")
                    mixer.music.play(1)
                    game_status = "lose" # 負けにする
                    timer_return = 100 # Spaceキーで戻れるようになるまでの時間

        elif game_status == "win": # 勝った時
            screen.blit(img_bg, (0, 0))
            screen.blit(img_audience, (0, -70-abs(math.sin(flying_dist/500*math.pi)*100)))
            text = font.render(str(finish_frame), True, (0,0,0))
            screen.blit(text, [373, 335])
            if timer == 0:
                img_gorilla = pygame.image.load("images/gorilla_win.png").convert_alpha() # timerが0で画像をドラミングゴリラに変更
            if timer < 0 and -timer % 20 == 0:
                img_gorilla = pygame.transform.flip(img_gorilla, True, False) # 20フレーム毎に左右反転
            screen.blit(img_win, (300-img_win.get_rect()[2]/2, 100-img_win.get_rect()[3]/2))
            screen.blit(img_gorilla, (200, 250))
            screen.blit(pygame.transform.rotate(img_enemy, 270), (400-img_enemy.get_rect()[2]+flying_dist, 200-flying_dist))
            screen.blit(img_badgorilla, (600-img_enemy.get_rect()[2]+random.randint(-10, 10), 300+random.randint(-10, 10)))
            flying_dist += 15
            if timer_return <= 0:
                screen.blit(img_tip, (300, 350))

        elif game_status == "lose": # 負けた時
            if cleared[select_menu] == 0:
                cleared[select_menu] = 1
            screen.blit(img_bg, (0, 0))
            screen.blit(img_audience, (0, -70+flying_dist/10))
            text = font.render(str(finish_frame), True, (0,0,0))
            screen.blit(text, [373, 335])
            screen.blit(img_lose, (300-img_lose.get_rect()[2]/2, 100-img_lose.get_rect()[3]/2))
            screen.blit(pygame.transform.rotate(img_gorilla, 90), (200-flying_dist, 200-flying_dist))
            screen.blit(img_enemy, (350-img_enemy.get_rect()[2], 250))
            screen.blit(img_badgorilla, (600-img_enemy.get_rect()[2], 300-abs(math.sin(flying_dist/500*math.pi)*100)))
            flying_dist += 15
            if timer_return <= 0:
                screen.blit(img_tip, (300, 350))

        elif game_status == "miss": # おてつきした時
            screen.blit(img_bg, (0, 0))
            screen.blit(img_audience, (0, -70))
            if timer == 0: # ゲームに戻る時に
                left_frame = random.randint(FRAME_MIN, FRAME_MAX) # !マークが出るまでの時間を再びランダムに決める
                mixer.music.load("sounds/wind.mp3")
                mixer.music.play(1)
                game_status = "fight"
            if timer < 0: # おてつきの画面の間
                timer = 200 # fightに戻るまでの時間
            screen.blit(img_miss, (300-img_miss.get_rect()[2]/2, 100-img_miss.get_rect()[3]/2))

        if DEBUG:
            text = font.render("DEBUG MODE", True, (0,0,0))
            screen.blit(text, [0, 0])
            text = font.render("timer:" + str(timer), True, (0,0,0))
            screen.blit(text, [0, 20])
            text = font.render("timer_return:" + str(timer_return), True, (0,0,0))
            screen.blit(text, [0, 40])
            text = font.render("flying_dist:" + str(flying_dist), True, (0,0,0))
            screen.blit(text, [0, 60])

        pygame.display.update()
        pygame.time.wait(15) # 0.015秒待つ

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE and game_status == "fight": # ゲーム中にスペースキーが押されたら
                    if left_frame <= 0 and timer <= 0: # ちゃんと!が出てから押した
                        mixer.music.load("sounds/win.mp3")
                        mixer.music.play(1)
                        game_status = "win"
                        timer = 150 # ゴリラが踊りだすまでの時間
                        timer_return = 100 # スペースキーで戻れるようになるまでの時間
                        cleared[select_menu] = 2
                        if select_menu == 2 and menu_num == 3: # HARDクリアでHELL解禁
                            menu_num = 4
                        if select_menu == 3 and menu_num == 4: # HELLクリアでIMPOSSIBLE解禁
                            menu_num = 5
                    elif timer <= 0: # おてつき
                        mixer.music.load("sounds/miss.mp3")
                        mixer.music.play(1)
                        game_status = "miss"

                elif event.key == K_SPACE and game_status == "menu": # メニュー画面でスペースキーが押されたら
                    enemy_frame = ENEMY_FRAME[select_menu]
                    game_status = "fight"
                    flying_dist = 0
                    if select_menu == 0:
                        img_enemy = pygame.image.load("images/enemy1.png").convert_alpha()
                    if select_menu == 1:
                        img_enemy = pygame.image.load("images/enemy2.png").convert_alpha()
                    if select_menu == 2:
                        img_enemy = pygame.image.load("images/enemy3.png").convert_alpha()
                    if select_menu == 3:
                        img_enemy = pygame.image.load("images/enemy4.png").convert_alpha()
                    if select_menu == 4:
                        img_enemy = pygame.image.load("images/enemy5.png").convert_alpha()
                    mixer.music.load("sounds/ready.mp3")
                    mixer.music.play(1)
                    timer = 200 # ゲームが始まる時のカットインの表示時間
                elif event.key == K_SPACE and (game_status == "win" or game_status == "lose") and timer_return <= 0: # ゲームが終わってからスペースキーが押されたら
                    img_gorilla = pygame.image.load("images/gorilla1.png").convert_alpha()
                    left_frame = 0
                    game_status = "menu"
                if event.key == K_DOWN and game_status == "menu": # カーソルを下に移動
                    select_menu = (select_menu+1)%menu_num
                if event.key == K_UP and game_status == "menu": # カーソルを上に移動
                    select_menu = (select_menu+(menu_num-1))%menu_num
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()