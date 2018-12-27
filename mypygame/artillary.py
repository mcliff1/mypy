"""
Classic Artillary GetParameter


Shoot cannons over a mountain at each other
given bags of powder and angle
"""
import pygame

DISPLAY = (800, 600)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def main(caption):
    """
    main game loop
    """
    frames_per_second = 30
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY[0], DISPLAY[1]))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    # def draw(blob):
    #     #game.draw.line(screen, GREEN, [0,0], [50, 30], 5)
    #     print(blob)
    #     print(blob.position)
    #     position = (int(blob.position[0]), int(blob.position[1]))
    #     pygame.draw.circle(screen, blob.color, position, int(blob.size), 0) # 0 width is filled
    #
    # blobs = init_blobs(5, color=BLUE)
    #blobs.append(init_blobs(5, color=BLUE))
    #print(blobs)
    #print(blobs[0].distance(blobs[1].position))

    exit_loop = False
    p_x = 200
    p_y = 100
    step = 2
    while not exit_loop:
        print('.')
        # check for exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                exit_loop = True

            # if event.key == pygame.K_UP:
            #     # make a new red blob
            #     print('move the gun up')
            #     p_y -= step

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # make a new red blob
                    print('move the gun up')
                    p_y -= step
                if event.key == pygame.K_DOWN:
                    # make a new red blob
                    print('move the gun down')
                    p_y += step
                    #blobs.append(Blob(_random_position(), color=BLUE))

                # L/R - more or less powder
                #  space - fire


        # paint the frame
        screen.fill(WHITE)

        pygame.draw.lines(screen, RED, False, [(100, 100), (p_x, p_y)], 2)


        pygame.display.update()   # or .flip()
        clock.tick(frames_per_second)   # frames per second (this is 60 in the web version)


    # run game
    pygame.quit()


if __name__ == '__main__':
    main('Artillary')
