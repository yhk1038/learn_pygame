# -*- coding: utf-8 -*-

import pygame
pygame.init()

# 게임 윈도우 사이즈 설정
ourScreen = pygame.display.set_mode((400, 300))
# 게임 윈도우 제목 설정
pygame.display.set_caption('독기의 첫 번째 게임')

# 메인루프
finish = False

# moving
x = 30
y = 30
clock = pygame.time.Clock()

# color
colorBlue = True

while not finish:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finish = True
		
		if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_c):
			colorBlue = not colorBlue
		
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_UP]: y -= 10
		if pressed[pygame.K_DOWN]: y += 10
		if pressed[pygame.K_LEFT]: x -= 10
		if pressed[pygame.K_RIGHT]: x += 10
		ourScreen.fill((0, 0, 0))
		
		if colorBlue:
			color = (0, 128, 255)
		else:
			color = (255, 255, 255)
		
		pygame.draw.rect(ourScreen, color, pygame.Rect(x, y, 60, 60))
		pygame.display.flip()
		
		clock.tick(60)
