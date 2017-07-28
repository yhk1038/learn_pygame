import pygame
pygame.init()
pygame.display.set_caption('이미지 삽입 테스트')

display_width = 800
display_height = 600
ourScreen = pygame.display.set_mode((display_width, display_height))

myImg = pygame.image.load('gorae.png')

def myimg(x, y):
	ourScreen.blit(myImg, (x, y))
	
x = display_width * 0.5
y = display_height * 0.5

finished = False
while not finished:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
	ourScreen.fill((255, 255, 200))
	myimg(x, y)
	
	pygame.display.flip()
	
pygame.quit()
quit()
