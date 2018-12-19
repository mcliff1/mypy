"""
My version of the game of life
"""
import random
import itertools
import uuid

import pygame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Blob():
    """
    Unit in the Game of Life
    """
    def __init__(self, position=(0, 0), size=10, color=RED):
        self.name = uuid.uuid4()
        self.x_position = position[0]
        self.y_position = position[1]

        self.x_velocity = 0
        self.y_velocity = 0

        self.color = color
        self.size = size

    def move(self):
        """
        moves the blob a step according to its velocity
        """
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity

        self.x_velocity += random.randint(0, 1) * (-1, 1)[self.x_velocity < 0]
        self.y_velocity += random.randint(0, 1) * (-1, 1)[self.y_velocity < 0]

        self.x_position = max(self.x_position, 0)
        self.y_position = max(self.y_position, 0)
        self.x_position = min(self.x_position, DISPLAY_WIDTH)
        self.y_position = min(self.y_position, DISPLAY_HEIGHT)


    def collides(self, blob):
        """
        returns true if this overlaps with the specified blob
        """
        # ideally use np norm but spell it out for now
        # delta_x^2 + delta_y^2 < (r_1+r_2)^2
        delta_center_sq = (self.x_position - blob.x_position)**2 + \
                          (self.y_position - blob.y_position)**2
        return delta_center_sq < (self.size + blob.size)**2


    def hit(self):
        """
        toggles the color and changes size accordingly
        """
        #print('Yeah: color {}'.format(self.color))

        self.x_velocity = -1 * self.x_velocity
        self.y_velocity = -1 * self.y_velocity

        self.color = RED if self.color == BLUE else BLUE

        if self.color == RED:
            self.size += 1

        if self.color == BLUE:
            self.size += -1

        if self.size < 1:
            self.size = 1

    def __repr__(self):
        return 'Blob[(' + ','.join([str(self.x_position), str(self.y_position)]) + ')' + \
               ', velocity=(' + ','.join([str(self.x_velocity), str(self.y_velocity)]) + ')' + \
               ', size=' + str(self.size) + \
               ', color=' + str(self.color) + \
               ']'

def _random_position():
    """ returns random tuple in display range """
    return (random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT))


def init_blobs(count=10, color=RED):
    """
    creates a count of new Blobs
    """
    return [Blob(_random_position(), color=color) for x in range(1, count)]



def main(caption):
    """
    main game loop
    """
    frames_per_second = 5
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    def draw(blob):
        #game.draw.line(screen, GREEN, [0,0], [50, 30], 5)
        _center = [blob.x_position, blob.y_position]
        pygame.draw.circle(screen, blob.color, _center, blob.size, 0) # 0 width is filled

    blobs = init_blobs(10)

    exit_loop = False
    while not exit_loop:
        # check for exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                exit_loop = True


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # make a new red blob
                    print('making a new red blob')
                    blobs.append(Blob(_random_position(), color=RED))
                if event.key == pygame.K_RIGHT:
                    # make a new red blob
                    print('making a new blue blob')
                    blobs.append(Blob(_random_position(), color=BLUE))



        screen.fill(WHITE)

        #pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)
        for blob in blobs:
            draw(blob)
            blob.move()
        #map(draw, blobs)

        for pair in [x for x in itertools.product(blobs, repeat=2) if x[0] != x[1]]:
            if pair[0].collides(pair[1]):
                print('hit on {}'.format(pair))
                pair[0].hit()
                pair[1].hit()




        pygame.display.update()   # or .flip()
        clock.tick(frames_per_second)   # frames per second (this is 60 in the web version)


    # run game
    pygame.quit()


if __name__ == '__main__':
    main('Blobs')
