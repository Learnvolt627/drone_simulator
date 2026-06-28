import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT =800, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('2D Drone Flight Simulator- Physics Engine')



WHITE =(255,255,255)
DARK_GREY=(30,30,30)
RED=(255,50,50)
BLUE=(50,50,255)

#Clock to control frame rate (60 Fps)
clock=pygame.time.Clock()

# Physics constrains & variables
GRAVITY= 0.15
DRONE_MASS=1
MOMENT_OF_INERTIA=0.5
vx=0
vy=0
angular_velocity=0
DRONE_WIDTH=60
HALF_W= DRONE_WIDTH/2

# Drone state variables (initial positions)

drone_x = WIDTH //2
drone_y= HEIGHT // 2
drone_angle= 0.0
drone_width = 60

def draw_drone(surface,x,y, angle, width):
    half_w= width/2

    

    x_left= x- half_w* math.cos(angle)
    y_left= y- half_w*math.sin(angle) 

    x_right=x+ half_w* math.cos(angle)
    y_right=y+ half_w* math.sin(angle)


    pygame.draw.line(surface, WHITE, (x_left, y_left), (x_right, y_right), 4)


    pygame.draw.circle(surface, RED, (int(x_left), int(y_left)), 8)
    pygame.draw. circle(surface, BLUE, (int(x_right), int(y_right)), 8)

def reset_drone():
    global drone_x, drone_y , drone_angle , vx, vy , angular_velocity
    drone_x = WIDTH //2
    drone_y = HEIGHT //3
    drone_angle= 0.0
    vx=0.0
    vy=0.0
    angular_velocity=0.0


# simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    left_thrust=0.075
    right_thrust=0.075

    keys= pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        left_thrust+=0.1
        right_thrust+=0.1
    if keys[pygame.K_LEFT]:
        right_thrust+=0.05
        
        
    if keys[pygame.K_RIGHT]:
        
        left_thrust+=0.05
        
    total_thrust= right_thrust+left_thrust

    thrust_x=total_thrust*math.sin(drone_angle)
    thrust_y=-total_thrust*math.cos(drone_angle)

    ax=thrust_x/DRONE_MASS
    ay=(thrust_y+GRAVITY)/ DRONE_MASS
    torque= (right_thrust-left_thrust)*HALF_W
    angular_accleration= torque/MOMENT_OF_INERTIA


    vx+=ax
    vy+=ay
    drone_x+=vx
    drone_y+=vy
    angular_velocity+= angular_accleration
    drone_angle+=angular_velocity
   


    if drone_y>HEIGHT:
        print("Drone hit the ground")
        reset_drone()

    elif drone_y<=0:
        print("Drone hit the ceiling")
        reset_drone()

    elif drone_x< 0 or drone_x> WIDTH:
        print("Drone flew of the sides")
        reset_drone()    

    screen.fill(DARK_GREY)
    
    draw_drone(screen, drone_x, drone_y, drone_angle, drone_width)

    pygame.display.flip()
    clock.tick(60)

pygame.quit ()
sys.exit()