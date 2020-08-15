""" Surface object """


class Surface():
    """ represents a 2D surface by the data points connecting it, expected data points are in x ascending order """
    def __init__(self, data):
        self.surface_data = data

        self.pairs = [
            (self.surface_data[k], self.surface_data[k+1])
            for k in range(len(self.surface_data)-1)
        ]
        self.slopes = [
            (pair[1][1] - pair[0][1])/(pair[1][0] - pair[0][0])
            for pair in self.pairs
        ]

    def __repr__(self):
        return (
            '{self.__class__.__name__}('
            'data={self.surface_data}'
            ',slopes={self.slopes}'
            ')'
        ).format(self=self)



    def find_lz(self):
        """ returns the mid-point and altitude of the landing surface """
        def find_lz_ndx(surface):
            """ input is array of numbers, we find two adjacent number in the 2nd position """
            x = surface[0][1]
            for i, y in enumerate(surface[1:]):
                if y[1] == x:
                    return i
                x = y[1]
            return None

        right_ndx = find_lz_ndx(self.surface_data)
        mid_point = int((self.surface_data[right_ndx][0] + self.surface_data[right_ndx + 1][0])/2)
        altitude = self.surface_data[right_ndx][1]
        return mid_point, altitude


    def detect_collision(self, position, target):
        """ returns None if there is no impact; or the appropriate left/right end point of the nearest impact """

        # list of x,y pairs representing the surface points
        #self.surface_data

        # for each surface segment
        # y = m1*(x-x0) + y0  (m from surface_slopes,  (x0,y0) from surface_pairs[0])

        # for the track to target (target)
        # y = m2*(x-p.x)+p.y
        # y = (target.y - position.y)/(target.x - position.x)*(x - position.x) + position.y

        # these cross at x wehn
        # (m1x0 - y0 - m2p.x + p.y)/(m1 - m2)
        # if this is between x0, x1 we have a collisiion

        m2 = (target[1] - position[1])/(target[0] - position[0])
        print(f'slope to target: {m2}')
        collision_points = []

        # for each pair of points calculate the slope
        for s in zip(self.pairs, self.slopes):
            # s[0][0][0] is the x co-ord of the the first elem in nth pair
            # s[0][1] is the 2nd elem in the nth pair
            # s[1] is the slope connecting the nth pair
            x = (s[1]*s[0][0][0] - s[0][0][1] - m2*position[0] + position[1]) / (s[1] - m2)
            print(f'x: {x} for pair: {s} and position: {position}')




            if s[0][0][0] < x < s[0][1][0]:
                if s[1] > 0:
                    collision_points.append(s[0][1])
                else:
                    collision_points.append(s[0][0])

        return collision_points
