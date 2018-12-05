import pygame

pygame.init()
game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption('my racer')
clock = pygame.time.Clock()

crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # are you sure?
            crashed = True   #breaks us out of the loop
        print(event)

    pygame.display.update()
    clock.tick(30)   # frames per second


# unload
pygame.quit()
quit()
