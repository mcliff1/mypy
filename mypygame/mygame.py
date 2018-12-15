"""
My first PyGame project; a simple race car - thanks sentdex
"""
import pygame
import time
import random

# https://pythonprogramming.net/pygame-python-3-part-1-intro
# image from - https://pythonprogramming.net/static/images/pygame/racecar.png
pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

car_width = 73


game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('my racer')
clock = pygame.time.Clock()

car_image = pygame.image.load('racecar.png')

def things(thing_x, thing_y, thing_w, thing_h, color):
    """
    draws things on the board
    """
    pygame.draw.rect(game_display, color, [thing_x, thing_y, thing_w, thing_h])


def car(position_x, position_y):
    """
    puts the car image on rthe display
    """
    game_display.blit(car_image, (position_x, position_y))    # draw background

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
    """displays the you crashed message"""
    message_display('You Crashed!!!')

    # game_loop()  # not sure this needs to be here

def new_thing_position():
    """
    creates a new thing's x,y tuple
    """
    new_x = random.randrange(0, display_width - 100)
    new_y = 0
    return (new_x, new_y)


def game_loop():
    car_x = (display_width) * .45
    car_y = (display_height) * .8
    x_change = 0
    car_speed = 5
    #crashed = False

    thing_w = 100
    thing_h = 100
    thing_x, thing_y = new_thing_position()
    thing_speed = 7


    game_exit = False


    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # are you sure?
                game_exit = True   #breaks us out of the loop
            #print(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -1 * car_speed
                elif event.key == pygame.K_RIGHT:
                    x_change = car_speed
                elif event.key == pygame.K_DOWN:
                    thing_speed += -1
                elif event.key == pygame.K_UP:
                    thing_speed += 1
                elif event.key == pygame.K_q:
                    game_exit = True
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    x_change = 0

        car_x += x_change

        game_display.fill(white)
        things(thing_x, thing_y, thing_w, thing_h, black)
        thing_y += thing_speed
        car(car_x, car_y)

        if car_x < 0 or car_x > display_width - car_width:
            crash()

        if thing_y > display_height:
            thing_x, thing_y = new_thing_position()
            # thing_y = thing_h
            # thing_x = random.randrange(0, display_width - thing_w)

        if car_y < thing_y + thing_h:
            if car_x > thing_x and car_x < thing_x + thing_w or \
               car_x + car_width > thing_x and car_x + car_width < thing_x + thing_w:
                # make a new thing
                thing_x, thing_y = new_thing_position()
                crash()

        pygame.display.update()   # or .flip()
        clock.tick(30)   # frames per second (this is 60 in the web version)

    pygame.quit()
    quit()


if __name__ == '__main__':
    game_loop()
