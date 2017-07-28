# -*- coding: utf-8 -*-

import pygame
pygame.init()
pygame.display.set_caption('이미지 삽입 테스트')

# pygame.mixer.music.load('IU-maum.mp3')
# pygame.mixer.music.play(-1)

# Size
display_width = 800
display_height = 600

img_width = 100
img_height = 100

start_x_position = 0
start_y_position = display_height - img_height

end_left    = 0
end_right   = display_width - img_width
end_top     = 0
end_bottom  = display_height - img_height

# Setup MetaData
ourScreen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

myImg = pygame.image.load('gorae.png')
myImg = pygame.transform.scale(myImg, (img_width, img_height))

# Image Rendering
def myimg(x, y):
	ourScreen.blit(myImg, (x, y))
	
def move(pressed, x, y):
	if pressed[pygame.K_UP]:
		y -= 10
		if y < end_top:
			y = end_top
	if pressed[pygame.K_DOWN]:
		y += 10
		if y > end_bottom:
			y = end_bottom
	if pressed[pygame.K_LEFT]:
		x -= 10
		if x < end_left:
			x = end_left
	if pressed[pygame.K_RIGHT]:
		x += 10
		if x > end_right:
			x = end_right
	return x, y
	

x = start_x_position
y = start_y_position

# Main Loop
finished = False
while not finished:
	# Event Loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
	ourScreen.fill((255, 255, 200))
	
	pressed = pygame.key.get_pressed()
	x, y = move(pressed, x, y)
	myimg(x, y)
	
	pygame.display.flip()
	clock.tick(60)
	
pygame.quit()
quit()
