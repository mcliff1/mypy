"""
My version of the game of life
"""

import pygame

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Blob():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = GREEN




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
        _to = [blob.x, blob.y]
        _from = [blob.x + 50, blob.y + 50]
        pygame.draw.line(screen, GREEN, _to, _from, 5)

    blob = Blob()

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
