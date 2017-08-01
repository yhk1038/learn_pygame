# -*- coding: utf-8 -*-

# 1 - Import library
import random
import math
import pygame
from pygame.locals import *

import numpy as np
import scipy

class Screen(object):
    def __init__(self, objects, options={}):
        size = objects[0]
        
        self.width = size[0]
        self.height = size[1]
        
        self.win_game = pygame.image.load("resources/images/youwin.png")
        self.lose_game = pygame.image.load("resources/images/gameover.png")
        
        self.win_game = pygame.transform.scale(self.win_game, (self.width, self.height))
        self.lose_game = pygame.transform.scale(self.lose_game, (self.width, self.height))
        pass
    pass

class Color(object):
    def __init__(self):
        self.black = (50, 50, 50)
        self.white = (255, 255, 255)
        self.blue = (0, 128, 255)
        pass
    
    def rainbow(self):
        return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    pass

class Paddle(object):
    
    def __init__(self, objects, options={}):
        screen = objects[0]
        self.color = objects[1]
        
        size = options['size']
        speed = options['speed']
        
        self.width = size[0]
        self.height = size[1]
        
        self.pos_x = 0.5 * (screen.width - self.width)
        self.pos_y = screen.height - self.height - 50
        
        self.x_increase = speed
        
        self.left_end = 0.0
        self.right_end = screen.width - self.width
        
        # self.obj = lambda x: pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        pass
    
    def obj(self):
        return pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
    
    def draw(self, screen):
        self.pos_x += self.x_increase
        return pygame.draw.rect(screen, self.color.blue, self.obj())
    
    def changeDirection(self, direct):
        if   direct == 'right':   self.x_increase = abs(self.x_increase) * 1.0
        elif direct == 'left':    self.x_increase = abs(self.x_increase) * -1.0
        elif direct == 'stop':    self.x_increase = self.x_increase * 0.0
        elif direct == 'restart': self.x_increase = 5.0
        pass
    
    def screen_touch_listener(self):
        if (self.pos_x + self.x_increase) <= self.left_end: self.changeDirection('right')
        elif (self.pos_x + self.x_increase) >= self.right_end: self.changeDirection('left')
        pass
    
    pass

class Boll(object):
    
    def __init__(self, objects, options={}):
        self.screen = objects[0]
        self.color = objects[1]
        paddle = objects[2]
        
        self.radius = options['radius']
        speed = options['speed']
        
        self.pos_x = int(paddle.pos_x + paddle.width * 0.5)
        self.pos_y = int(paddle.pos_y - self.radius)
        
        self.x_increase = 1 * speed
        self.y_increase = -1 * speed
        
        self.bottom_end = self.screen.height + self.radius
        
        self.touch_brick = pygame.mixer.Sound("resources/audio/explode.wav")
        self.touch_paddle = pygame.mixer.Sound("resources/audio/shoot.wav")
        self.touch_screen = pygame.mixer.Sound("resources/audio/enemy.wav")
        
        self.touch_brick.set_volume(0.2)
        self.touch_paddle.set_volume(0.2)
        self.touch_screen.set_volume(0.2)
        pass
    
    def draw(self, screen):
        self.pos_x += self.x_increase
        self.pos_y += self.y_increase
        return pygame.draw.circle(screen, self.color.white, (self.pos_x, self.pos_y), self.radius)
    
    pass

    # 공이 벽돌에 맞는 경우
    def bricks_touch_listener(self, rleft, rtop, width, height,  # rectangle definition
                           center_x, center_y, radius,  # circle definition
                           dx, dy):
    
        # complete boundbox of the rectangle
        # rright, rbottom = rleft + width/2, rtop + height/2
        rright, rbottom = rleft + width, rtop + height
    
        # bounding box of the circle
        cleft, ctop = center_x - radius, center_y - radius
        cright, cbottom = center_x + radius, center_y + radius
    
        # trivial reject if bounding boxes do not intersect
        if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
            return False, False, False  # no collision possible
    
        # check whether any point of rectangle is inside circle's radius
        # 좌변 or 우변에 충돌
        if 0 < (rleft - center_x) <= radius or 0 < (center_x - (rleft + width)) <= radius:
            dx *= -1
            return True, dx, dy
        # 하단 or 상단에 충돌
        if 0 < (center_y - (rtop + height)) <= radius or 0 < (rtop - center_y) <= radius:
            dy *= -1
            return True, dx, dy
    
        # x_rL, y_rT 좌상점
        if math.hypot(rleft - center_x, rtop - center_y) <= radius: return True, True, True
        # x_rL, y_rB 좌하점
        if math.hypot(rleft - center_x, (rtop + height) - center_y) <= radius: return True, True, True
        # x_rR, y_rT 우상점
        if math.hypot((rleft + width) - center_x, rtop - center_y) <= radius: return True, True, True
        # x_rR, y_rB 우하점
        if math.hypot((rleft + width) - center_x, (rtop + height) - center_y) <= radius: return True, True, True
    
        # check if center of circle is inside rectangle
        if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
            return True, center_x, center_y  # overlaid
    
        return False, False, False  # no collision detected

    # 공이 패들에 맞는 경우
    def paddle_touch_listener(self, paddle):
        rtop,    rleft  = paddle.pos_y,         paddle.pos_x
        rbottom, rright = rtop + paddle.height, rleft + paddle.width

        # 원의 높이가 패들의 세로 범위 안으로 들어왔을 때
        if rtop <= (self.pos_y + self.radius) <= rbottom:
            # 원의 중심이 패들의 가로 범위 안으로 들어왔을 때
            if rleft <= self.pos_x <= rright:
                self.y_increase *= -1
                self.touch_paddle.play()
                return
    
            # 원의 중심이 패들의 가로 범위 바깥에 있으면서,
            else:
                # (측면 충돌) [원의 중심의 y값]이 [패들의 위쪽]과 [패들의 아랫쪽] 사이에 있으면서,
                if rtop < self.pos_y < rbottom:
            
                    # (좌변에 충돌) [패들의 왼쪽]이 [원의 왼쪽 점]과 [원의 오른쪽 점] 사이에 있을 때
                    if (self.pos_x - self.radius) < rleft <= (self.pos_x + self.radius):
                        self.x_increase *= -1
                        return
            
                    # (우변에 충돌) [패들의 오른쪽]이 [원의 왼쪽 점]과 [원의 오른쪽 점] 사이에 있을 때
                    if (self.pos_x - self.radius) < rright <= (self.pos_x + self.radius):
                        self.x_increase *= -1
                        return
        pass

    # 공이 벽에 닿는 경우
    def screen_touch_listener(self):
        if self.pos_x <= 0:                                      # 왼쪽 벽에 닿는 경우
            self.x_increase = abs(self.x_increase)
            self.touch_screen.play()
        elif (self.pos_x + self.radius) >= self.screen.width:    # 오른쪽 벽에 닿는 경우
            self.x_increase = abs(self.x_increase) * -1
            self.touch_screen.play()

        if (self.pos_y - self.radius) <= 0:                      # 위쪽 벽에 닿는 경우
            self.y_increase = abs(self.y_increase)
            self.touch_screen.play()
        elif (self.pos_y + self.radius) >= self.bottom_end:      # 아래쪽 한계에 닿는 경우
            self.x_increase, self.y_increase = 0, 0
        pass

class Brick(object):
    
    def __init__(self, objects, options={}):
        screen = objects[0]
        self.color = objects[1]
        
        self.width = 40
        self.height = 30
        self.margin = 1
        
        self.horizontal_length = screen.width / self.width
        self.vertical_length = options['vertical_length']
        pass
    
    def obj(self, x_pos, y_pos):
        return pygame.Rect(x_pos, y_pos, self.width - self.margin, self.height - self.margin)
    
    def bricks_array(self):
        bricks = []
        
        for bx in range(self.horizontal_length):
            for by in range(self.vertical_length):
                x_pos = bx * self.width
                y_pos = by * self.height
                brick = self.obj(x_pos, y_pos)
                bricks.append([brick, x_pos, y_pos])
        
        return bricks
    
    def draw(self, screen, bricks, myBoll):
        i = 0
        for brickSet in bricks:
            brick = brickSet[0]
            collision = myBoll.bricks_touch_listener(
                brickSet[1], brickSet[2],
                self.width, self.height,
                myBoll.pos_x, myBoll.pos_y, myBoll.radius,
                myBoll.x_increase, myBoll.y_increase
            )
            
            if collision[0]:
                myBoll.touch_brick.play()
                myBoll.x_increase = collision[1]
                myBoll.y_increase = collision[2]
                bricks.pop(i)

            pygame.draw.rect(screen, self.color.rainbow(), brick)
            i += 1
        pass
    
    pass

class Score(object):
    def __init__(self, objects, options={}):
        self.screen = objects[0]
        self.color = objects[1]
        
        bricks = options['bricks']
        self.full_score = len(bricks)
        self.breaked = 0
        self.score = 0.0
        pass
    
    def current_score(self, bricks):
        self.breaked = self.full_score - len(bricks)
        
        total = self.full_score * 1.0
        breaked = self.breaked * 1.0
        self.score = int((breaked / total) * 100.0)
        pass
    
    def draw(self, screen, color):
        score_message = '{} of {} Breaked! / Remain: {} / Now Points: {}'.format(self.breaked, self.full_score, (self.full_score - self.breaked), self.score)
        
        font = pygame.font.Font(None, 24)
        text = font.render(score_message, True, color)
        textRect = text.get_rect()
        textRect.center = [self.screen.width/2, self.screen.height/2]
        screen.blit(text, textRect)
        pass
    
    pass

class BreakBrick:
    def __init__(self, options={'size': [600, 800], 'paddle': [200, 20, 5.0], 'boll': [7, 6], 'brick': [10]}):
        
        self.init_size = options['size']
        self.init_paddle = options['paddle']
        self.init_boll = options['boll']
        self.init_brick = options['brick']
        
        # # Launch Game
        # pygame.init()
        # self.load_music()
        #
        # # Objects init
        # self.myScreen = Screen([self.init_size])
        # self.myColor = Color()
        # self.myPaddle = Paddle([self.myScreen, self.myColor], {'size': [self.init_paddle[0], self.init_paddle[1]], 'speed': self.init_paddle[2]})
        # self.myBoll = Boll([self.myScreen, self.myColor, self.myPaddle], {'radius': self.init_boll[0], 'speed': self.init_boll[1]})
        # self.myBricks = Brick([self.myScreen, self.myColor, self.myBoll], {'vertical_length': self.init_brick[0]})
        #
        # self.bricks = self.myBricks.bricks_array()
        # self.myScore = Score([self.myScreen, self.myColor], {'bricks': self.bricks})
        #
        # # Set Game
        # self.screen = pygame.display.set_mode((self.myScreen.width, self.myScreen.height))
        # pygame.display.set_caption('Break Bricks')
        # self.clock = pygame.time.Clock()
        self.load_data()
        pass
    
    def load_data(self):
        # Launch Game
        pygame.init()
        self.load_music()
    
        # Objects init
        self.myScreen = Screen([self.init_size])
        self.myColor = Color()
        self.myPaddle = Paddle([self.myScreen, self.myColor],
                               {'size': [self.init_paddle[0], self.init_paddle[1]], 'speed': self.init_paddle[2]})
        self.myBoll = Boll([self.myScreen, self.myColor, self.myPaddle],
                           {'radius': self.init_boll[0], 'speed': self.init_boll[1]})
        self.myBricks = Brick([self.myScreen, self.myColor, self.myBoll], {'vertical_length': self.init_brick[0]})
    
        self.bricks = self.myBricks.bricks_array()
        self.myScore = Score([self.myScreen, self.myColor], {'bricks': self.bricks})
    
        # Set Game
        self.screen = pygame.display.set_mode((self.myScreen.width, self.myScreen.height))
        pygame.display.set_caption('Break Bricks')
        self.clock = pygame.time.Clock()
        pass
    
    def load_music(self):
        bgm = 'IU-maum.wav'
        pygame.mixer.init()
        pygame.mixer.music.load(bgm)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        pass
    
    def draw_objects(self):
        self.screen.fill(self.myColor.black)  # 스크린 채우기
        self.myPaddle.draw(self.screen)  # 패들 그리기
        self.myBoll.draw(self.screen)  # 볼 그리기
        self.myBricks.draw(self.screen, self.bricks, self.myBoll)  # 벽돌 그리기
        self.myScore.draw(self.screen, self.myColor.blue)
        pygame.display.flip()  # 그린 것 띄우기
        pass

    def start(self):
        
        status = 1
        is_win = False
        while status:
            self.draw_objects()
        
            for event in pygame.event.get():
                # 닫기 버튼으로 게임종료
                if event.type == pygame.QUIT:
                    self.exit()
            
                if event.type == pygame.KEYDOWN:
                    # 일시정지 및 해제 / 게임종료
                    if event.key == K_SPACE:
                        if not self.myPaddle.x_increase == 0.0:
                            self.myPaddle.changeDirection('stop')
                        else:
                            self.myPaddle.changeDirection('restart')
                    elif event.key == K_ESCAPE:
                        self.exit()
                
                    # 패들 방향 조작
                    if event.key == K_LEFT:
                        self.myPaddle.changeDirection('left')
                    elif event.key == K_RIGHT:
                        self.myPaddle.changeDirection('right')

            self.clock.tick(60)
        
            # 패들이 벽에 닿으면 방향을 바꾼다
            self.myPaddle.screen_touch_listener()
            
            # 공이 벽에 닿으면 튕겨낸다
            self.myBoll.screen_touch_listener()
            
            # 공이 패들에 닿으면 튕겨낸다
            self.myBoll.paddle_touch_listener(self.myPaddle)
            
            # 이번 루프의 점수를 계산한다
            self.myScore.current_score(self.bricks)
        
            # 게임 종료
            # # 승리
            if self.myScore.score == 100.0:
                status = 0
                is_win = True
            # # 패배
            elif (self.myBoll.x_increase, self.myBoll.x_increase) == (0, 0):
                if self.myBoll.pos_y > self.myPaddle.pos_y:
                    status = 0
                    is_win = False
                    
        # self.stop(is_win)
        self.restart()
        pass  # exit Start function
    
    def pause(self):
        pass
    
    def stop(self, win_game):
        print "최종 스코어 : 총 {}개의 벽돌 중, {}개 파괴. [{} 점]".format(self.myScore.full_score, self.myScore.breaked, self.myScore.score)
        
        pygame.font.init()
        font = pygame.font.Font(None, 24)
        text = font.render("Points: " + str(self.myScore.score) + "%", True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = self.screen.get_rect().centerx
        textRect.centery = self.screen.get_rect().centery + 24
        
        if win_game:
            self.screen.blit(self.myScreen.win_game, (0, 0))
        else:
            self.screen.blit(self.myScreen.lose_game, (0, 0))
            
        self.screen.blit(text, textRect)
        
        self.myScore.draw(self.screen, self.myColor.white)
        pygame.display.update()
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()
                    elif event.key == K_SPACE:
                        self.restart()
                        pass
                pass
        pass
    
    def restart(self):
        pygame.quit()
        self.load_data()
        self.start()
        pass
    
    def exit(self):
        pygame.quit()
        exit(0)
        pass
    
    pass  # exit class

config = {
    'size': [600, 400],         # screen size   [ width, height ]
    'paddle': [200, 20, 5.0],   # paddle config [ width, height, speed]
    'boll': [7, 6],             # boll config   [ radius, speed ]
    'brick': [1],  # brick config [ line count ]
}

bb = BreakBrick()
# bb = BreakBrick(config)
bb.start()
