# -*- coding: utf-8 -*-

# 1 - Import library
import random
import math
import pygame
from pygame.locals import *

import numpy as np
import scipy

# 2 - Define Class
# class BreakBrick:
#     def __init__(self):
#
#         pygame.init()
#         width
#
#         pass
#
#     def move(self):
#         pass
#     pass
#
# bb = BreakBrick()
# bb.move()

# 패들, 볼, 블럭, 스크린, 스코어

# Size init
screenSize_width = 600
screenSize_height = 700

paddleSize_width = 200
paddleSize_height = 20

bollSize_radius = 7

brickSize_width = 30
brickSize_height = 15
brickSize_margin = 1

# Color Labelling
c_black = (50, 50, 50)
c_white = (255, 255, 255)
c_blue = (0, 128, 255)
def c_rainbow(): return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

# Position init
paddlePosition_X = 0.5 * (screenSize_width - paddleSize_width)
paddlePosition_Y = screenSize_height - paddleSize_height - 50

bollPosition_X = int(paddlePosition_X + paddleSize_width * 0.5)
bollPosition_Y = int(paddlePosition_Y - bollSize_radius)

# Paddle
paddle_X_increase = 5.0
paddleMoves_right = True

paddleLimit_left = 0.0
paddleLimit_right = screenSize_width - paddleSize_width

# Boll
bollMove_valocity = 6
boll_X_increase = 1 * bollMove_valocity
boll_Y_increase = -1 * bollMove_valocity

bollLimit_bottom = screenSize_height + bollSize_radius

# Brick
bricks = []

bricks_horizontal_length = (screenSize_width / brickSize_width)
bricks_vertical_length = 20

for bx in range(bricks_horizontal_length):
    for by in range(bricks_vertical_length):
        brick_x_pos = bx * brickSize_width
        brick_y_pos = by * brickSize_height
        brick = pygame.Rect(brick_x_pos, brick_y_pos, brickSize_width - brickSize_margin, brickSize_height - brickSize_margin)
        bricks.append([brick, brick_x_pos, brick_y_pos])

# Launch Game
pygame.init()
screen = pygame.display.set_mode((screenSize_width, screenSize_height))
pygame.display.set_caption('Break Bricks')
clock = pygame.time.Clock()

def changePaddleDirection(x_increase, direct):
    if direct == 'right': x_increase = abs(x_increase) * 1.0
    elif direct == 'left': x_increase = abs(x_increase) * -1.0
    
    if direct == 'stop': x_increase = x_increase * 0.0
    elif direct == 'restart': x_increase = 5.0
    
    return x_increase

def collision(rleft, rtop, width, height,   # rectangle definition
              center_x, center_y, radius,   # circle definition
              dx, dy):
    
    # complete boundbox of the rectangle
    # rright, rbottom = rleft + width/2, rtop + height/2
    rright, rbottom = rleft + width, rtop + height

    # bounding box of the circle
    cleft,  ctop    = center_x - radius, center_y - radius
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
    if math.hypot(rleft - center_x, rtop - center_y) <= radius:
        return True, True, True
    # x_rL, y_rB 좌하점
    if math.hypot(rleft - center_x, (rtop + height) - center_y) <= radius:
        return True, True, True
    # x_rR, y_rT 우상점
    if math.hypot((rleft + width) - center_x, rtop - center_y) <= radius:
        return True, True, True
    # x_rR, y_rB 우하점
    if math.hypot((rleft + width) - center_x, (rtop + height) - center_y) <= radius:
        return True, True, True

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True, center_x, center_y  # overlaid

    return False, False, False  # no collision detected

def changeBollDirection(x_pos, y_pos, x_increase, y_increase):
    if x_pos <= 0:                                          # 왼쪽 벽에 닿는 경우
        x_increase = abs(x_increase)
    elif (x_pos + bollSize_radius) >= screenSize_width:     # 오른쪽 벽에 닿는 경우
        x_increase = abs(x_increase) * -1
    
    if (y_pos - bollSize_radius) <= 0:                      # 위쪽 벽에 닿는 경우
        y_increase = abs(y_increase)
    elif (y_pos + bollSize_radius) >= bollLimit_bottom:     # 아래쪽 한계에 닿는 경우
        # y_increase = abs(y_increase) * -1
        x_increase = 0
        y_increase = 0
    
    return [x_increase, y_increase]

def touchPaddle(rleft, rtop, width, height,   # rectangle definition
                center_x, center_y, radius,   # circle definition
                dx, dy):
    if rtop <= (center_y + radius) <= (rtop + height):
        if rleft <= center_x <= (rleft + width):  # 패들 구역 왼쪽 끝 부터, 패들 구역 오른쪽 끝 안에
            dy *= -1
    
    return dx, dy

# Main Loop
finish = False
while not finish:
    
    screen.fill(c_black)

    # Paddle 그리기
    paddlePosition_X += paddle_X_increase
    paddle = pygame.Rect(paddlePosition_X, paddlePosition_Y, paddleSize_width, paddleSize_height)
    pygame.draw.rect(screen, c_blue, paddle)

    # Boll 그리기
    bollPosition_X += boll_X_increase
    bollPosition_Y += boll_Y_increase
    pygame.draw.circle(screen, c_white, (bollPosition_X, bollPosition_Y), bollSize_radius)
    
    # Brick 그리기
    bricks_i = 0
    for brickSet in bricks:
        brick = brickSet[0]
        colsn = collision(brickSet[1], brickSet[2], brickSize_width, brickSize_height, bollPosition_X, bollPosition_Y, bollSize_radius, boll_X_increase, boll_Y_increase)
        if colsn[0]:
            boll_X_increase = colsn[1]
            boll_Y_increase = colsn[2]
            bricks.pop(bricks_i)
        pygame.draw.rect(screen, c_rainbow(), brick)
        bricks_i += 1
    
    # 그린것들 띄우기
    pygame.display.flip()
    
    for event in pygame.event.get():
        # 닫기 버튼으로 게임종료
        if event.type == pygame.QUIT:
            finish = True
            
        if event.type == pygame.KEYDOWN:
            # 일시정지 및 해제 / 게임종료
            if event.key == K_SPACE:
                if not paddle_X_increase == 0.0:
                    paddle_X_increase = changePaddleDirection(paddle_X_increase, 'stop')
                else:
                    paddle_X_increase = changePaddleDirection(paddle_X_increase, 'restart')
            elif event.key == K_ESCAPE:
                pygame.quit()
                exit(0)

            # 패들 방향 (수동) 지정
            if event.key == K_LEFT:
                paddleMoves_right = False
            elif event.key == K_RIGHT:
                paddleMoves_right = True
                
        clock.tick(60)
        
    # 패들 방향 (자동) 지정
    if (paddlePosition_X + paddle_X_increase) < paddleLimit_left:
        paddleMoves_right = True
    elif (paddlePosition_X + paddle_X_increase) > paddleLimit_right:
        paddleMoves_right = False
    
    # 패들 지정된 방향 반영
    if not paddleMoves_right:
        paddle_X_increase = changePaddleDirection(paddle_X_increase, 'left')
    else:
        paddle_X_increase = changePaddleDirection(paddle_X_increase, 'right')
    
    boll_X_increase, boll_Y_increase = changeBollDirection(bollPosition_X, bollPosition_Y, boll_X_increase, boll_Y_increase)
    boll_X_increase, boll_Y_increase = touchPaddle(paddlePosition_X, paddlePosition_Y, paddleSize_width, paddleSize_height,
                                                   bollPosition_X, bollPosition_Y, bollSize_radius,
                                                   boll_X_increase, boll_Y_increase)
    
    # 게임 종료
    if (boll_X_increase, boll_X_increase) == (0, 0):
        # 게임 패배
        if bollPosition_Y >= paddlePosition_Y:
            finish = True
            print bollPosition_Y, paddlePosition_Y
    
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
            elif event.key == K_SPACE:
                pygame.quit()
                break
    pygame.display.flip()
