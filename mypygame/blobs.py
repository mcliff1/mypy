"""
My version of the game of life
"""

import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Blob():
    def __init__(self, position=(0, 0), size=10, color=RED):
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.size = size




def main(caption):
    """
    main game loop
    """
    display_width = 800
    display_height = 600
    frames_per_second = 10
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    def draw(blob):
        #game.draw.line(screen, GREEN, [0,0], [50, 30], 5)
        _center = [blob.x, blob.y]
        pygame.draw.circle(screen, blob.color, _center, blob.size, 0) # 0 width is filled

    blob = Blob([50, 50])

    exit_loop = False
    while not exit_loop:
        # check for exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                exit_loop = True


        screen.fill(WHITE)

        #pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)
        draw(blob)

        pygame.display.update()   # or .flip()
        clock.tick(frames_per_second)   # frames per second (this is 60 in the web version)


    # run game
    pygame.quit()


if __name__ == '__main__':
    main('Blobs')
