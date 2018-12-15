import pygame
import time

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

def things(thing_x, thing_y, thing_w, thing_h, color):
    pygame.draw.rect(game_display, color, [thing_x, thing_y, thing_w, thing_h])

def car(x, y):
    game_display.blit(car_image, (x, y))    # draw background

def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def message_display(text):
    large_text_font = pygame.font.Font('freesansbold.ttf', 115)
    text_surf, text_rect = text_objects(text, large_text_font)
    text_rect.center = ((display_width/2), (display_height/2))
    game_display.blit(text_surf, text_rect)

    pygame.display.update()
    time.sleep(2)

def crash():
    message_display('You Crashed!!!')

    # game_loop()  # not sure this needs to be here


def game_loop():
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
            crash()

        pygame.display.update()   # or .flip()
        clock.tick(30)   # frames per second (this is 60 in the web version)

if __name__ == '__main__':
    game_loop()
    pygame.quit()
    quit()
