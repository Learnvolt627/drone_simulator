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
linear_drag=0.01
angular_drag=0.02
kp=1.2 #proportional gain
ki=0.0 #integral gain
kd=1.0  #prevents overshoots

error_integral=0.0
previous_angle=0.0
target_angle=0.0




# Drone state variables (initial positions)

drone_x = WIDTH //2
drone_y= HEIGHT // 2
drone_angle= 0.0
drone_width = 60

ground_y= HEIGHT-40
hover_thrust=GRAVITY

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
    global error_integral,previous_angle, target_angle
    drone_x = WIDTH //2
    drone_y =ground_y
    drone_angle= 0.0
    vx=0.0
    vy=0.0
    angular_velocity=0.0

    error_integral=0.0
    previous_angle=0.0
    target_angle=0.0

grid_spacing=80
def scrolling_background(surface, cam_x, cam_y):
    surface.fill(DARK_GREY)
    #vertical grid lines
    start_x= -(cam_x % grid_spacing)
    x=start_x
    while x< WIDTH:
        pygame.draw.line(surface, (50,50,50), (x,0),(x,HEIGHT),1)
        x += grid_spacing

    #horizontal grid lines
    start_y=-(cam_y % grid_spacing)
    y= start_y
    while y< HEIGHT:
        pygame.draw.line(surface, (50,50,50), (0,y),(WIDTH,y),1)
        y += grid_spacing

    #Ground line
    ground_screen= ground_y- cam_y
    pygame.draw.line(surface, (100,70,40),(0,ground_screen), (WIDTH,ground_screen),3)


# simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    base_thrust=0.0

    keys= pygame.key.get_pressed()
    if keys[pygame.K_UP]:
       base_thrust+=0.15

    if keys[pygame.K_DOWN]:
        base_thrust-=0.15

    desired_angle=-0.3 if keys[pygame.K_LEFT] else (0.3 if keys[pygame.K_RIGHT] else 0.0)
    target_angle+= (desired_angle-target_angle)*0.1

 

    current_error= target_angle-drone_angle
    error_integral+=current_error
    error_derivative=-(drone_angle-previous_angle)
    pid_output=(kp*current_error)+(ki*error_integral)+(kd*error_derivative)
    previous_angle= drone_angle

    left_thrust=base_thrust + pid_output
    right_thrust= base_thrust - pid_output


    total_thrust= right_thrust+left_thrust
   

    thrust_x=total_thrust*math.sin(drone_angle)
    thrust_y=-total_thrust*math.cos(drone_angle)

    ax=thrust_x/DRONE_MASS
    ay=(thrust_y+GRAVITY)/ DRONE_MASS

    arm_lenght=HALF_W*0.01
    torque= (left_thrust-right_thrust)*arm_lenght
    angular_accleration= torque/MOMENT_OF_INERTIA


    vx+=ax
    vy+=ay
    drone_x+=vx
    drone_y+=vy
    angular_velocity+= angular_accleration
    drone_angle+=angular_velocity
    vx=vx*(1-linear_drag)
    vy=vy*(1-linear_drag)
    angular_velocity= angular_velocity*(1-angular_drag)

    #clamping of output for safety
    pid_output=max(-0.5, min(0.5, pid_output))
    angular_velocity=max(-2.0, min(2.0,angular_velocity))

    if drone_y>=ground_y:
        drone_y=ground_y
        if vy>0:
            vy=0

    elif drone_y<=-2000:
        print("Drone hit max altitude")
        reset_drone()

    camera_x = drone_x - WIDTH /2
    camera_y = drone_y - HEIGHT /2

    scrolling_background(screen, camera_x, camera_y)
    draw_drone(screen, drone_x-camera_x, drone_y-camera_y,drone_angle, drone_width )

    pygame.display.flip()
    clock.tick(60)

pygame.quit ()
sys.exit()