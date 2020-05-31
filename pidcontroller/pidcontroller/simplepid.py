""" expects to get update on second-time intervals """

class PID():
    """ PID controller """

    def __init__(self, Kp, Ki, Kd, setpoint):
        """
        Initialize the PID controller

        :param Kp: value of the proportional gain
        :param Ki: value for the integral gain
        :param Kd: value for the derivateive gain
        :param setpoint: target value for the control

        """
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.setpoint = setpoint

        self._proportional = 0
        self._integral = 0
        self._derivative = 0



    def __repr__(self):
        return (
            '{self.__class__.__name__}('
            'Kp={self.Kp!r}, Ki={self.Ki!r}, Kd={self.Kd!r},'
            'setpoint={self.setpoint!r}'
            ')'
        ).format(self=self)
