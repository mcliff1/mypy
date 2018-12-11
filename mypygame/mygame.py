import pygame

# https://pythonprogramming.net/pygame-python-3-part-1-intro
# image from - https://pythonprogramming.net/static/images/pygame/racecar.png
pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)


game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('my racer')
clock = pygame.time.Clock()

car_image = pygame.image.load('racecar.png')

def car(x, y):
    game_display.blit(car_image, (x, y))    # draw background

x = (display_width) * .45
y = (display_height) * .8
x_change = 0
car_speed = 0
#crashed = False
game_exit = False
car_width = 73


while not game_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # are you sure?
            game_exit = True   #breaks us out of the loop
        #print(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            elif event.key == pygame.K_RIGHT:
                x_change = 5
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                x_change = 0

    x += x_change

    game_display.fill(white)
    car(x, y)

    if x < 0 or x > display_width - car_width:
        game_exit = True

    pygame.display.update()   # or .flip()
    clock.tick(30)   # frames per second


# unload
pygame.quit()
quit()
