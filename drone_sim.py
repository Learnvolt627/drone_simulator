import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT =800, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('2d Drone Flight Simulator')



WHITE =(255,255,255)
DARK_GREY=(30,30,30)
RED=(255,50,50)
BLUE=(50,50,255)

#Clock to control frame rate (60 Fps)
clock=pygame.time.Clock()

# Drone state variables (initial positions)

drone_x = WIDTH //2
drone_y= HEIGHT // 2
drone_angle= 0.0
drone_width = 60

def draw_drone(surface, x, y, angle, width):
    half_w= width/2

    x_left= x- half_w* math.cos(angle)
    y_left= y- half_w*math.sin(angle) 

    x_right=x+ half_w* math.cos(angle)
    y_right=y+ half_w* math.sin(angle)


    pygame.draw.line(surface, WHITE, (x_left, y_left), (x_right, y_right), 4)


    pygame.draw.circle(surface, RED, (int(x_left), int(y_left)), 8)
    pygame.draw. circle(surface, BLUE, (int(x_right), int(y_right)), 8)


# simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    # Temporary manual controls to test visual rotation

    keys= pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        drone_angle-= 0.05
    if keys[pygame.K_RIGHT]:
        drone_angle+=0.05

    if keys[pygame.K_w]:
        drone_y-=3

    if keys[pygame.K_s]:
        drone_y+=3

    screen.fill(DARK_GREY)
    
    draw_drone(screen, drone_x, drone_y, drone_angle, drone_width)

    pygame.display.flip()
    clock.tick(60)

pygame.quit ()
sys.exit()