"""
Classic Artillary GetParameter


Shoot cannons over a mountain at each other
given bags of powder and angle
"""
import math
import pygame
from pygame.color import THECOLORS

DISPLAY = (800, 600)
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
GROUND_COLOR = (128, 128, 60)

GROUND_LEVEL = 500
GRAVITY = 0.1


class Shell():
    """ represents an artillary round """
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.color = THECOLORS['black']
        self.size = 3

    def draw(self, draw_circle):
        """ displays a shell using the provided routine """
        draw_circle(self.color, (int(self.position[0]), int(self.position[1])), self.size)


    def move(self):
        """
        applies the velocity change to position, and the gravity impact to the init_velocity
        """
        # tuple_add in one line
        self.position = tuple(sum(x) for x in zip(self.position, self.velocity))
        # apply the pull of GRAVITY
        self.velocity = tuple(sum(x) for x in zip(self.velocity, (0, GRAVITY)))
        #print('shell.move:postion:{}'.format(self.position))

    def __repr__(self):
        """ representation method """
        return 'Shell(position={}, velocity={}, color={})'.format(self.position, self.velocity, self.color)

class Gun():
    """
    implements an artillary piece
    uses Shell
    """
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
        line_start = (int(self.position[0]), int(self.position[1] - self.size/2))
        line_end = (int(line_start[0] + self.size), line_start[1])
        draw_line(self.color, line_start, line_end, self.size)

        gun_start = (int(self.position[0] + self.size/2), line_start[1])
        gun_end = (int(gun_start[0] + math.cos(self.angle) * self.barrel), int(gun_start[1] - math.sin(self.angle) * self.barrel))
        draw_line(self.color, gun_start, gun_end, 2)

    # def set_angle(self, angle):
    #     """ stores the angle provided in degrees as radians """
    #     self.angle = angle * math.pi / 180

    def change_angle(self, up_or_down):
        """ adjusts the angle of the gun up or down """
        self.angle += up_or_down * math.pi / 180

    def fire(self):
        """
        returns a Shell object in the direction the gun is fired and loaded
        """
        speed = 6
        velocity = (speed * math.cos(self.angle), -1 * speed * math.sin(self.angle))
        return Shell(self.position, velocity)




#def _add_vectors((length1, angle1), (length2, angle2)):
def _add_vectors(v1, v2):
    """
    v1 = (r, theta)
    adds to vectors in polar co-ordinates together
    converts to X, y; adds; and convers back
    """
    x = math.cos(v1[1]) * v1[0] + math.cos(v2[1]) * v2[0]
    y = math.sin(v1[1]) * v1[0] + math.sin(v2[1]) * v2[0]

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)
    return (length, angle)


def main(caption):
    """
    main game loop
    """
    frames_per_second = 20
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY[0], DISPLAY[1]))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    # def draw_rect(color, rect):
    #     """ hides the pygame and screen object """
    #     pygame.draw.rect(screen, color, rect)

    def draw_line(color, start_pos, end_pos, width=1):
        """ hides the pygame and screen object """
        pygame.draw.line(screen, color, start_pos, end_pos, width)


    def draw_circle(color, position, radius, width=0):
        """ hides the pygame and screen object """
        #print('(color={}, position={}, radius={}, width={})')
        pygame.draw.circle(screen, color, position, radius, width)


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
    # p_x = 200
    # p_y = 100
    step = 2

    gun = Gun((200, GROUND_LEVEL))
    shells = []
    while not exit_loop:
        #print('.{}'.format(shells))
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
                    # p_y -= step
                    gun.change_angle(1)
                if event.key == pygame.K_DOWN:
                    # make a new red blob
                    print('move the gun down')
                    # p_y += step
                    gun.change_angle(-1)
                if event.key == pygame.K_SPACE:
                    # make a new red blob
                    print('fire!')
                    shells.append(gun.fire())
                    #blobs.append(Blob(_random_position(), color=BLUE))
                    #shell = Shell(gun.position, (1, 1))
                # L/R - more or less powder
                #  space - fire


        # paint the frame
        screen.fill(THECOLORS['white'])
        pygame.draw.rect(screen, GROUND_COLOR,
                         (0, GROUND_LEVEL, DISPLAY[0], DISPLAY[1] - GROUND_LEVEL))


        gun.draw(draw_line)


        # check for impact !
        # if shell.position < ground level

        #map(lambda x: x.draw(draw_circle), shells)
        #map(lambda x: x.move(), shells)
        for shell in shells:
            shell.draw(draw_circle)
            shell.move()




        # pygame.draw.lines(screen, THECOLORS['red'], False, [(100, 100), (p_x, p_y)], 2)


        pygame.display.update()   # or .flip()
        clock.tick(frames_per_second)   # frames per second (this is 60 in the web version)


    # run game
    pygame.quit()


if __name__ == '__main__':
    main('Artillary')
