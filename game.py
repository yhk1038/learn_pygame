# -*- coding: utf-8 -*-

# 1 - Import library
import random
import math
import pygame
from pygame.locals import *

# 2 - Initialize the game
class myGame:
    def __init__(self, args={}):
    
        size = [640, 480]
        volum = 0.5
        runTime = 90000
        valocity = 50
        bgm = 'IU-maum.wav'
        
        pygame.init()
        self.width, self.height = size
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.FPS = valocity
        self.fpsClock = pygame.time.Clock()
        self.runTime = runTime
        
        pygame.mixer.init()
        
        # 키 입력 체크
        self.keys = [False, False, False, False]
        # 플레이어 위치(버니)
        self.playerpos = [100, 100]

        self.acc = [0, 0]
        self.arrows = []

        self.badtimer = 100
        self.badtimer1 = 0
        self.badguys = [[640, 100]]
        self.healthvalue = 194
        
        # 3 - Load images
        self.player = pygame.image.load("resources/images/dude.png")
        self.grass = pygame.image.load("resources/images/grass.png")
        self.castle = pygame.image.load("resources/images/castle.png")
        self.arrow = pygame.image.load("resources/images/bullet.png")

        self.badguyimg1 = pygame.image.load("resources/images/badguy.png")
        self.badguyimg = self.badguyimg1

        self.healthbar = pygame.image.load("resources/images/healthbar.png")
        self.health = pygame.image.load("resources/images/health.png")

        self.gameover = pygame.image.load("resources/images/gameover.png")
        self.youwin = pygame.image.load("resources/images/youwin.png")
        
        # 3.1 - Load audio
        self.hit = pygame.mixer.Sound("resources/audio/explode.wav")
        self.enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
        self.shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
        
        self.volum = volum
        self.hit.set_volume(self.volum)
        self.enemy.set_volume(self.volum)
        self.shoot.set_volume(self.volum)
        
        # pygame.mixer.music.load('resources/audio/moonlight.wav')
        self.bgvolum = volum
        pygame.mixer.music.load(bgm)
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(self.bgvolum)


# 4 - keep looping through
    def start(self):
        running = 1
        exitcode = 0
        while running:
            self.badtimer -= 1
            # 5 - clear the screen before drawing it again
            self.screen.fill(0)
            
            # 6 - draw the screen elements
            # 잔디를 그린다.
            for x in range(self.width / self.grass.get_width() + 1):
                for y in range(self.height / self.grass.get_height() + 1):
                    self.screen.blit(self.grass, (x * 100, y * 100))
            
            # 성을 그린다.
            self.screen.blit(self.castle, (0, 30))
            self.screen.blit(self.castle, (0, 135))
            self.screen.blit(self.castle, (0, 240))
            self.screen.blit(self.castle, (0, 345))
            
            # 6.1 - Set player position and rotation
            position = pygame.mouse.get_pos()
            angle = math.atan2(position[1] - (self.playerpos[1] + 32), position[0] - (self.playerpos[0] + 26))
            playerrot = pygame.transform.rotate(self.player, 360 - angle * 57.29)
            playerpos1 = (self.playerpos[0] - playerrot.get_rect().width / 2, self.playerpos[1] - playerrot.get_rect().height / 2)
            self.screen.blit(playerrot, playerpos1)
            
            # 6.2 - Draw arrows
            for bullet in self.arrows:
                index = 0
                velx = math.cos(bullet[0]) * 10
                vely = math.sin(bullet[0]) * 10
                bullet[1] += velx
                bullet[2] += vely
                if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
                    self.arrows.pop(index)
                index += 1
                for projectile in self.arrows:
                    arrow1 = pygame.transform.rotate(self.arrow, 360 - projectile[0] * 57.29)
                    self.screen.blit(arrow1, (projectile[1], projectile[2]))
            
            # 6.3 - Draw badgers
            if self.badtimer == 0:
                self.badguys.append([640, random.randint(50, 430)])
                self.badtimer = 100 - (self.badtimer1 * 2)
                if self.badtimer1 >= 35:
                    self.badtimer1 = 35
                else:
                    self.badtimer1 += 5
            index = 0
            for badguy in self.badguys:
                if badguy[0] < -64:
                    self.badguys.pop(index)
                badguy[0] -= 7
                
                # 6.3.1 - Attack castle
                badrect = pygame.Rect(self.badguyimg.get_rect())
                badrect.top = badguy[1]
                badrect.left = badguy[0]
                
                if badrect.left < 64:
                    self.hit.play()
                    self.healthvalue -= random.randint(5, 20)
                    self.badguys.pop(index)
                
                # 6.3.2 - Check for collisions
                index1 = 0
                for bullet in self.arrows:
                    bullrect = pygame.Rect(self.arrow.get_rect())
                    bullrect.left = bullet[1]
                    bullrect.top = bullet[2]
                    if badrect.colliderect(bullrect):
                        self.enemy.play()
                        self.acc[0] += 1
                        self.badguys.pop(index)
                        self.arrows.pop(index1)
                    index1 += 1
                
                # 6.3.3 - Next bad guy
                index += 1
            
            for badguy in self.badguys:
                self.screen.blit(self.badguyimg, badguy)
            
            # 6.4 - Draw clock
            font = pygame.font.Font(None, 24)
            survivedtext = font.render(str((self.runTime - pygame.time.get_ticks()) / 60000) + ":" + str(
                (self.runTime - pygame.time.get_ticks()) / 1000 % 60).zfill(2), True, (0, 0, 0))
            textRect = survivedtext.get_rect()
            textRect.topright = [635, 5]
            self.screen.blit(survivedtext, textRect)
            
            # 6.5 - Draw health bar
            self.screen.blit(self.healthbar, (5, 5))
            for health1 in range(self.healthvalue):
                self.screen.blit(self.health, (health1 + 8, 8))
            
            # 7 - update the screen
            pygame.display.flip()
            self.fpsClock.tick(self.FPS)
            
            # 8 - loop through the events
            for event in pygame.event.get():
                # check if the event is the X button
                if event.type == pygame.QUIT:
                    # if it is quit the game
                    pygame.quit()
                    exit(0)
                
                # 키를 누를 때: 키가 눌렸음을 True 로 변환.
                if event.type == pygame.KEYDOWN:
                    # 위로 이동 키
                    if event.key == K_w:
                        self.keys[0] = True
                    # 왼쪽으로 이동 키
                    elif event.key == K_a:
                        self.keys[1] = True
                    # 아래로 이동 키
                    elif event.key == K_s:
                        self.keys[2] = True
                    # 오른쪽으로 이동 키
                    elif event.key == K_d:
                        self.keys[3] = True
                    # 볼륨 업 키
                    elif event.key == K_UP:
                        self.bgvolum += 0.1
                    # 볼륨 다운 키
                    elif event.key == K_DOWN:
                        self.bgvolum -= 0.1
                    # 게임 종료 키
                    elif event.key == K_q:
                        print self.keys
                        pygame.quit()
                        exit(0)
                    pygame.mixer.music.set_volume(self.bgvolum)
                
                # 키를 뗄 때: 눌린 키의 상태를 뗀 상태로 전환.
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.keys[0] = False
                    elif event.key == pygame.K_a:
                        self.keys[1] = False
                    elif event.key == pygame.K_s:
                        self.keys[2] = False
                    elif event.key == pygame.K_d:
                        self.keys[3] = False
                
                # 마우스를 클릭했을 때: 화살을 쏜다.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.shoot.play()
                    position = pygame.mouse.get_pos()
                    self.acc[1] += 1
                    self.arrows.append(
                        [math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)),
                         playerpos1[0] + 32,
                         playerpos1[1] + 32])
            
            # 9 - Move player 플레이어 움직이게 하기.
            # 조건문의 순서는 상, 하, 좌, 우
            if self.keys[0]:
                self.playerpos[1] -= 5
            elif self.keys[2]:
                self.playerpos[1] += 5
            if self.keys[1]:
                self.playerpos[0] -= 5
            elif self.keys[3]:
                self.playerpos[0] += 5
            
            # 10 - Win/Lose check
            if pygame.time.get_ticks() >= self.runTime:
                running = 0
                exitcode = 1
            if self.healthvalue <= 0:
                running = 0
                exitcode = 0
            if self.acc[1] != 0:
                accuracy = self.acc[0] * 1.0 / self.acc[1] * 100
            else:
                accuracy = 0
        
        # 11 - Win/lose display
        if exitcode == 0:
            pygame.font.init()
            font = pygame.font.Font(None, 24)
            text = font.render("Accuracy: "+str(accuracy)+"%", True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = self.screen.get_rect().centery+24
            self.screen.blit(self.gameover, (0, 0))
            self.screen.blit(text, textRect)
        else:
            pygame.font.init()
            font = pygame.font.Font(None, 24)
            text = font.render("Accuracy: "+str(accuracy)+"%", True, (0, 255, 0))
            textRect = text.get_rect()
            textRect.centerx = self.screen.get_rect().centerx
            textRect.centery = self.screen.get_rect().centery+24
            self.screen.blit(self.youwin, (0, 0))
            self.screen.blit(text, textRect)
    
mygame = myGame({})
mygame.start()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                exit(0)
            elif event.key == K_SPACE:
                pygame.quit()
                mygame = myGame({})
                mygame.start()
                break
    pygame.display.flip()
