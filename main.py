import pygame
import random

def draw_rect(color, rect):
	pygame.draw.rect(pygame.display.get_surface(), color, rect)

def draw_rect_w(rect):
	draw_rect((255, 255, 255), rect)

def draw():
	# draw jancsi A
	draw_rect_w(pygame.Rect(jancsi_off, jancsiAy, jancsi_width, jancsi_height))
	# draw jancsi B
	draw_rect_w(pygame.Rect(width - jancsi_width - jancsi_off, jancsiBy, jancsi_width, jancsi_height))
	# draw ball
	draw_rect_w(pygame.Rect(ballx, bally, ball_size, ball_size))

def resetball():
	global ballx
	global bally
	global ballvx
	global ballvy
	global ball_scale
	ballx = width / 2 - ball_size / 2
	bally = height / 2 - ball_size / 2
	#ballvx = -0.02
	#ballvy = 0.05
	ballvx = 0.04 * ((scoreA + scoreB) % 2 * 2 - 1)
	ballvy = random.random() * 0.08
	ball_scale = 1

pygame.init()
width = 400
height = 300
screen = pygame.display.set_mode((width, height))
done = False

jancsi_v = 0.08
jancsi_off = 10
jancsi_height = 70
jancsi_width = 10
jancsiAy = height / 2 - jancsi_height / 2
jancsiBy = height / 2 - jancsi_height / 2

scoreA = 0
scoreB = 0

ball_size = 15
ball_scale = 1
ball_scale_scale = 0.1
resetball()

deflect_scale = 0.05

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	
	# handle input A
	if pygame.key.get_pressed()[pygame.K_s]:
		jancsiAy += jancsi_v
	elif pygame.key.get_pressed()[pygame.K_w]:
		jancsiAy -= jancsi_v
	jancsiAy = max(0, jancsiAy)
	jancsiAy = min(height - jancsi_height, jancsiAy)

	# handle input B
	if pygame.key.get_pressed()[pygame.K_DOWN]:
		jancsiBy += jancsi_v
	elif pygame.key.get_pressed()[pygame.K_UP]:
		jancsiBy -= jancsi_v
	jancsiBy = max(0, jancsiBy)
	jancsiBy = min(height - jancsi_height, jancsiBy)

	# update ball pos
	ballx += ballvx * ball_scale
	bally += ballvy * ball_scale

	# check wall collision
	if bally < 0:
		bally = 0
		ballvy *= -1
	elif bally > height - ball_size:
		bally = height - ball_size
		ballvy *= -1

	# check goal
	if ballx <= 0:
		scoreB += 1
		print(scoreA, ":", scoreB)
		resetball()
	elif ballx + ball_size >= width:
		scoreA += 1
		print(scoreA, ":", scoreB)
		resetball()

	# check jancsi collision
	off = (bally + ball_size / 2 - jancsiAy - jancsi_height/2) / (jancsi_height / 2 + ball_size)
	if ballx < jancsi_off + jancsi_width and abs(off) < 1:
		ballx = jancsi_off + jancsi_width
		ballvx *= -1
		ball_scale += ball_scale_scale
		ballvy += off * deflect_scale
	
	off = (bally + ball_size / 2 - jancsiBy - jancsi_height/2) / (jancsi_height / 2 + ball_size)
	if ballx > width - jancsi_off - jancsi_width - ball_size and abs(off) < 1:
		ballx = width - jancsi_off - jancsi_width - ball_size
		ballvx *= -1
		ball_scale += ball_scale_scale
		ballvy += off * deflect_scale


	pygame.display.get_surface().fill((0,0,0))
	draw()
	pygame.display.flip()
