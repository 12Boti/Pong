import pygame
import random

def draw_rect(color, rect):
    pygame.draw.rect(pygame.display.get_surface(), color, rect)
# váltotott
def draw_rect_w(color,rect):
    draw_rect(color, rect)

def draw():
    # draw jancsi A
    	draw_rect_w((255,255,255),pygame.Rect(jancsi_off, jancsiAy, jancsi_width, jancsi_height_A))
    # draw jancsi B
    	draw_rect_w((255,255,255),pygame.Rect(width - jancsi_width - jancsi_off, jancsiBy, jancsi_width, jancsi_height_B))
    # draw ball
    	draw_rect_w((255,255,255),pygame.Rect(ballx, bally, ball_size, ball_size))
# váltotott
    # töltés A
    	if szamlA<90000 and not lejar[0]:
        	draw_rect_w((255,0,0),pygame.Rect(jancsi_off, jancsiAy + jancsi_height_A - (jancsi_height_A*szamlA/90000), jancsi_width, (jancsi_height_A/90000)*szamlA))
    	if szamlA>=90000 and not lejar[0]:
        	draw_rect_w((255,0,0),pygame.Rect(jancsi_off, jancsiAy, jancsi_width, jancsi_height_A))
    	if lejar[0]:
        	draw_rect_w((255,0,0),pygame.Rect(jancsi_off, jancsiAy + (jancsi_height_A*szamlA/18000), jancsi_width, (jancsi_height_A/18000)*(18000-szamlA)))
    # töltés B
  	if szamlB<90000 and not lejar[1]:
        	draw_rect_w((0,0,255),pygame.Rect(width - jancsi_width - jancsi_off, jancsiBy + jancsi_height_B - (jancsi_height_B*szamlB/90000), jancsi_width, (jancsi_height_B/90000)*szamlB))
	if szamlB>=90000 and not lejar[1]:
        	draw_rect_w((0,0,255),pygame.Rect(width - jancsi_width - jancsi_off, jancsiBy, jancsi_width, jancsi_height_B))
	if lejar[1]:
        	draw_rect_w((0,0,255),pygame.Rect(width - jancsi_width - jancsi_off, jancsiBy + (jancsi_height_B*szamlB/18000), jancsi_width, (jancsi_height_B/18000)*(18000-szamlB)))        
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
#jancsi_height = 70
# váltotott
jancsi_height_A = 70
jancsi_height_B = 70
jancsi_width = 10
jancsiAy = height / 2 - jancsi_height_A / 2
jancsiBy = height / 2 - jancsi_height_B / 2

scoreA = 0
scoreB = 0
szamlA = 0
szamlB = 0
lejar=[False,False]

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
# váltotott
    if pygame.key.get_pressed()[pygame.K_SPACE] and szamlA>=4500*20:
        jancsi_height_A *= 2
        szamlA = 0
        lejar[0] = True
                
    if lejar[0] and szamlA == 18000:
        jancsi_height_A = jancsi_height_A/2
        szamlA = 0
        lejar[0] = False
            
    jancsiAy = max(0, jancsiAy)
    jancsiAy = min(height - jancsi_height_A, jancsiAy)

	# handle input B
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        jancsiBy += jancsi_v
    elif pygame.key.get_pressed()[pygame.K_UP]:
        jancsiBy -= jancsi_v
# váltotott
    if pygame.key.get_pressed()[pygame.K_TAB] and szamlB>=4500*20:
        jancsi_height_B *= 2
        szamlB = 0
        lejar[1] = True
    if lejar[1] and szamlB == 18000:
        jancsi_height_B = jancsi_height_B/2
        szamlB = 0
        lejar[1] = False

            
    jancsiBy = max(0, jancsiBy)
    jancsiBy = min(height - jancsi_height_B, jancsiBy)

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
    off = (bally + ball_size / 2 - jancsiAy - jancsi_height_A/2) / (jancsi_height_A / 2 + ball_size)
    if ballx < jancsi_off + jancsi_width and abs(off) < 1:
        ballx = jancsi_off + jancsi_width
        ballvx *= -1
        ball_scale += ball_scale_scale
        ballvy += off * deflect_scale
	
    off = (bally + ball_size / 2 - jancsiBy - jancsi_height_B/2) / (jancsi_height_B / 2 + ball_size)
    if ballx > width - jancsi_off - jancsi_width - ball_size and abs(off) < 1:
        ballx = width - jancsi_off - jancsi_width - ball_size
        ballvx *= -1
        ball_scale += ball_scale_scale
        ballvy += off * deflect_scale


    pygame.display.get_surface().fill((0,0,0))
    draw()
# váltotott
    szamlA += 1
    szamlB += 1
    pygame.display.flip()
