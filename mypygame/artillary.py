"""
Classic Artillary GetParameter


Shoot cannons over a mountain at each other
given bags of powder and angle
"""
import pygame
import math

DISPLAY = (800, 600)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GROUND_COLOR = (128, 128, 60)

GROUND_LEVEL = 500


class Gun():
    """ implements an artillary piece """
    def __init__(self, position):
        self.angle = 40 * math.pi / 180
        self.position = position
        self.size = 20
        self.color = (250, 90, 90)
        self.barrel = 50

    def draw(self, draw_line):
        """
        draws itself using the given rectangle function
        """
        #draw_rect(self.color, (self.position, (self.size, self.size)))
        line_start = (self.position[0], self.position[1] - int(self.size/2))
        line_end = (line_start[0] + self.size, line_start[1])
        draw_line(self.color, line_start, line_end, self.size)

        gun_start = (self.position[0] + int(self.size/2), line_start[1])
        gun_end = (gun_start[0] + math.cos(self.angle) * self.barrel, gun_start[1] - math.sin(self.angle) * self.barrel)
        draw_line(self.color, gun_start, gun_end, 2)

    # def set_angle(self, angle):
    #     """ stores the angle provided in degrees as radians """
    #     self.angle = angle * math.pi / 180

    def change_angle(self, up_or_down):
        """ adjusts the angle of the gun up or down """
        self.angle += up_or_down * math.pi / 180


def main(caption):
    """
    main game loop
    """
    frames_per_second = 30
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY[0], DISPLAY[1]))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    def draw_rect(color, rect):
        """ hides the pygame and screen object """
        pygame.draw.rect(screen, color, rect)

    def draw_line(color, start_pos, end_pos, width=1):
        """ hides the pygame and screen object """
        pygame.draw.line(screen, color, start_pos, end_pos, width)



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

    gun = Gun((200, GROUND_LEVEL))

    while not exit_loop:
        # print('.')
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
                    gun.change_angle(1)
                if event.key == pygame.K_DOWN:
                    # make a new red blob
                    print('move the gun down')
                    p_y += step
                    gun.change_angle(-1)
                if event.key == pygame.K_SPACE:
                    # make a new red blob
                    print('fire!')
                    #blobs.append(Blob(_random_position(), color=BLUE))

                # L/R - more or less powder
                #  space - fire


        # paint the frame
        screen.fill(WHITE)
        pygame.draw.rect(screen, GROUND_COLOR,
                         (0, GROUND_LEVEL, DISPLAY[0], DISPLAY[1] - GROUND_LEVEL))


        gun.draw(draw_line)

        pygame.draw.lines(screen, RED, False, [(100, 100), (p_x, p_y)], 2)


        pygame.display.update()   # or .flip()
        clock.tick(frames_per_second)   # frames per second (this is 60 in the web version)


    # run game
    pygame.quit()


if __name__ == '__main__':
    main('Artillary')
