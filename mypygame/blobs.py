"""
My version of the game of life
"""
import random
import itertools
import uuid
import math

import pygame

DISPLAY = (800, 600)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Blob():
    """
    Unit in the Game of Life
    """
    def __init__(self, position=(0, 0), velocity=(0, 0), size=10, color=RED):
        self.name = uuid.uuid4()

        self.position = position
        self.velocity = velocity
        #self.velocity = [random.randint(-1, 1), random.randint(-1, 1)]

        self.color = color
        self.size = size

    def move(self):
        """
        moves the blob a step according to its velocity
        """
        self.position = tuple(sum(x) for x in zip(self.position, self.velocity))

        #self.x_velocity += random.randint(0, 1) * (-1, 1)[self.x_velocity < 0]
        #self.y_velocity += random.randint(0, 1) * (-1, 1)[self.y_velocity < 0]

        if self.position[0] < self.size:
            self.position = (self.size, self.position[1])
            self.velocity = (-1 * self.velocity[0], self.velocity[1])
        if self.position[0] > DISPLAY[0] - self.size:
            self.position = (DISPLAY[0] - self.size, self.position[1])
            self.velocity = (-1 * self.velocity[0], self.velocity[1])
        if self.position[1] < self.size:
            self.position = (self.position[0], self.size)
            self.velocity = (self.velocity[0], -1 * self.velocity[1])
        if self.position[1] > DISPLAY[1] - self.size:
            self.position = (self.position[0], DISPLAY[1] - self.size)
            self.velocity = (self.velocity[0], -1 * self.velocity[1])

        # self.x_position = max(self.x_position, self.size)
        # self.y_position = max(self.y_position, self.size)
        # self.x_position = min(self.x_position, DISPLAY_WIDTH - self.size)
        # self.y_position = min(self.y_position, DISPLAY_HEIGHT - self.size)


    def collides(self, blob):
        """
        returns true if this overlaps with the specified blob
        """
        # ideally use np norm but spell it out for now
        # delta_x^2 + delta_y^2 < (r_1+r_2)^2
        delta_center_sq = (self.position[0] - blob.position[0])**2 + \
                          (self.position[1] - blob.position[1])**2
        return delta_center_sq < (self.size + blob.size)**2


    def hit(self, target):
        """
        toggles the color and changes size accordingly
        """
        #print('Yeah: color {}'.format(self.color))

        self.velocity += -1 * target.velocity
        # self.velocity[1] += -1 * target.velocity[1]

        #self.velocity, target.velocity = -1 * target.velocity, -1 * self.velocity

        # if they match, the target gets destroyed
        if self.color == target.color:
            # self.color = random.choice([RED, BLUE])
            # self.color = random.choice([RED, BLUE])
            self.size += target.size
            target.size = 0

        # if self.color == RED:
        #     self.size += 1
        #
        # if self.color == BLUE:
        #     self.size += -1
        #
        # if self.size < 1:
        #     self.size = 1

    def distance(self, position):
        """ distance between center of this blob and the given position """
        return math.sqrt((self.position[0] - position[0])**2 + (self.position[1] - position[1])**2)

    def direction(self, position, norm=1.0):
        """ returns the direction vector from the center of this blob to the position """
        factor = norm / self.distance(position)
        # TODO - how do I make this pythonic?
        return ( factor * (position[0] - self.position[0]), factor * (position[1] - self.position[1]) )

    def calc_forces(self, blobs, const=1.0):
        """
        forces is equal to sum of size^2/distance^2
        """
        force = (0.0, 0.0)
        for blob in blobs:
            if blob.name != self.name:
                distance = self.distance(blob.position)
                magnitude = const * blob.size**2 / distance**2
                if self.color == blob.color:
                    magnitude *= -1.0
                direction = self.direction(blob.position, norm=magnitude)
                force = tuple(sum(x) for x in zip(force, direction))
                #force.append(direction)
        return force

    def __repr__(self):
        return 'Blob[name=' + str(self.name)[:6] + \
               ', ' + str(self.position) + \
               ', velocity=' + str(self.velocity) + \
               ', size=' + str(self.size) + \
               ', color=' + str(self.color) + \
               ']'

def _random_position():
    """ returns random tuple in display range """
    return (random.randint(0, DISPLAY[0]), random.randint(0, DISPLAY[1]))

def _random_velocity(max_value=2):
    """ returns random tuple """
    return (random.randint(-1 * max_value, max_value), random.randint(-1 * max_value, max_value))


def init_blobs(count=10, color=RED):
    """
    creates a count of new Blobs
    """
    return [Blob(position=_random_position(),
                 velocity=_random_velocity(),
                 color=color, size=10) for x in range(0, count)]
    #self.velocity = [random.randint(-1, 1), random.randint(-1, 1)]


def add_tuple(v1, v2):
    """ elementwise addition of tuples """
    return tuple(sum(x) for x in zip(v1, v2))

def main(caption):
    """
    main game loop
    """
    frames_per_second = 30
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY[0], DISPLAY[1]))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    def draw(blob):
        #game.draw.line(screen, GREEN, [0,0], [50, 30], 5)
        print(blob)
        print(blob.position)
        position = (int(blob.position[0]), int(blob.position[1]))
        pygame.draw.circle(screen, blob.color, position, int(blob.size), 0) # 0 width is filled

    blobs = init_blobs(5, color=BLUE)
    #blobs.append(init_blobs(5, color=BLUE))
    #print(blobs)
    #print(blobs[0].distance(blobs[1].position))

    exit_loop = False
    while not exit_loop:
        print('.')
        # check for exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                exit_loop = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # print('mousedown {}'.format(pygame.mouse.get_pressed()))
                # pressed1, pressed2, _ = pygame.mouse.get_pressed()
                # if pressed1:
                #     blobs.append(Blob(pos, color=RED))
                # if pressed2:
                #     blobs.append(Blob(pos, color=BLUE))
                blobs.append(Blob(pos))

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
            blob.velocity = add_tuple(blob.velocity, blob.calc_forces(blobs))
            #print(blob.velocity)

        for blob in blobs:
            blob.move()

        #print(blobs[0].calc_forces([blobs[1]]))

        # check each pair to see on any interactions
        for pair in itertools.combinations(blobs.copy(), r=2):
            #print('checking {}'.format(pair))
            if pair[0].collides(pair[1]):
                if pair[0].color == pair[1].color:
                    # aborb and remove one
                    pair[0].size += pair[1].size
                    blobs.remove(pair[1])
                else:
                    # split both of them
                    pair[0].size -= 1
                    pair[1].size -= 1
                    pair[0].size = min(pair[0].size, 0)
                    pair[1].size = min(pair[1].size, 0)


        for blob in blobs:
            draw(blob)

        pygame.display.update()   # or .flip()
        clock.tick(frames_per_second)   # frames per second (this is 60 in the web version)


    # run game
    pygame.quit()


if __name__ == '__main__':
    main('Blobs')
