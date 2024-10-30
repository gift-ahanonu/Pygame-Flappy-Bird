import pygame
import random

# Initialize pygame
pygame.init()

# Set the window title
pygame.display.set_caption("Flappy Bird")

# Load the game assets (images)
background = pygame.image.load('bg.png')
bird = pygame.image.load('bird_sing.png')
ground = pygame.image.load('ground.png')
gameover = pygame.image.load('Game_Over.1.png')
tube1 = pygame.image.load('tube2.png')
tube2 = pygame.transform.flip(tube1, False, True)

# Set global constants
SCREEN = pygame.display.set_mode((288, 496))
FPS = 50
SPEED_FOW = 3
FONT = pygame.font.SysFont('calibri', 50, bold=True)

# Define the tube class
class tubes_class:
    # __init__ function initializes the tube's position
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75,150)
    # foward_draw function moves the tube forward and draw it in the screen
    def foward_draw(self):
        self.x -= SPEED_FOW
        SCREEN.blit(tube1, (self.x, self.y + 210))
        SCREEN.blit(tube2, (self.x, self.y - 210))
    # collision function checks if the bird collides with the tubes
    def collision(self, bird, birdx, birdy):
        tolerance = 5
        bird_Rside = birdx + bird.get_width() - tolerance
        bird_Lside = birdx + tolerance
        tubes_Rside = self.x + tube1.get_width()
        tubes_Lside = self.x
        bird_Uside= birdy + tolerance
        bird_Dside= birdy + bird.get_height() - tolerance
        tubes_Uside= self.y + 110
        tubes_Dside = self.y + 210
        if bird_Rside > tubes_Lside and bird_Lside < tubes_Rside:
            if bird_Uside < tubes_Uside or bird_Dside > tubes_Dside:
                you_lost()

    # between_tubes function checks if the bird is between the tubes
    def between_tubes(self, bird, birdx):
        tolerance = 5
        bird_Rside = birdx + bird.get_width() - tolerance
        bird_Lside = birdx + tolerance
        tubes_Rside = self.x + tube1.get_width()
        tubes_Lside = self.x
        if bird_Rside > tubes_Lside and bird_Lside < tubes_Rside:
            return True


#  drawobjects functiona draws the elements on the screen and renders the score
def drawobjects():
    SCREEN.blit(background, (0,0))
    for t in tubes:
        t.foward_draw()
    SCREEN.blit(bird, (birdx, birdy))
    SCREEN.blit(ground, (groundx,400))
    score_render = FONT.render(str(score), 1, (255,255,255))
    SCREEN.blit(score_render, (144,0))

# The update function updates the display and sets the FPS
def update():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

# The initialize function sets initial values for game variables
def initialize():
    global birdx, birdy, birdspeed_y
    global groundx
    global tubes
    global score
    global between_tubes
    birdx, birdy = 60, 150
    birdspeed_y = 0
    groundx = 0
    score = 0
    tubes = []
    tubes.append(tubes_class())
    between_tubes = False

# Function to display game over screen and start over the game
def you_lost():
    SCREEN.blit(gameover, (50, 180))
    update()
    startover = False
    while not startover:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                initialize()
                startover = True
            if event.type == pygame.QUIT:
                pygame.quit()

# Initialize the game
initialize()


# Main Loop
while True:
    # Move the ground image to the left
    groundx -= SPEED_FOW
    if groundx < -45: groundx = 0
    #Gravity
    birdspeed_y += 1
    birdy += birdspeed_y

    # Handle user input events
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
            # Move the bird up by decreasing its speed
            birdspeed_y = -10
        if event.type == pygame.QUIT:
            # Quit the game if user closes the game window
            pygame.quit()

    # Manage the tubes
    max_tubesx = 0
    for t in tubes:
       if t.x > max_tubesx: max_tubesx = t.x
    if max_tubesx < 150: tubes.append(tubes_class())
    if tubes[-1].x < 150: tubes.append(tubes_class())

    # Check collision between bird and tubes
    for t in tubes:
        t.collision(bird, birdx,birdy)
    # Check if bird is between the tubes to count score
    if not between_tubes:
        for t in tubes:
            if t.between_tubes(bird, birdx):
                between_tubes = True
                break
    if between_tubes:
        between_tubes = False
        for t in tubes:
            if t.between_tubes(bird, birdx):
                between_tubes = True
                break
        if not between_tubes:
            score +=1

    # Check collision between bird and ground
    if birdy > 381:
        you_lost()

    #Screen update
    drawobjects()
    update()

main()



