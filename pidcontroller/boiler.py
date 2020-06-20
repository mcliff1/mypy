from pidcontroller.simplepid import PID

class Boiler():
    """
    starts at 20, power adjusts temp, slow constant heat loss
    """
    def __init__(self, init_temp):
        self.temp = init_temp
        self._power_limit = 10.0

    def update(self, power):
        if power > 0:
            self.temp += power

        if power > self._power_limit:
            self.temp += self._power_limit

        # steady heat loss
        self.temp -= 0.02
        return self.temp


if __name__ == '__main__':
    water_temp = 20.0
    boiler = Boiler(water_temp)
    pid = PID(5, 0.01, 0.1, water_temp)
    t, p = [], []
    for _ in range(10):
        power = pid.update(water_temp)
        water_temp = boiler.update(power)
        t += [water_temp]
        p += [power]
    print(p)
    print(t)
