""" expects to get update on second-time intervals """

def _bound(value, limits):
    """ checks that the value is within the limits """
    lower, upper = limits
    if value is None:
        return None
    if upper is not None and value > upper:
        return upper
    if lower is not None and value < lower:
        return lower
    return value

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

        self._output_limits = (-100.0, 100.0)

        self._proportional = 0
        self._integral = 0
        self._derivative = 0


        self._last_input = None


    def __repr__(self):
        return (
            '{self.__class__.__name__}('
            'Kp={self.Kp!r}, Ki={self.Ki!r}, Kd={self.Kd!r},'
            'setpoint={self.setpoint!r}'
            ')'
        ).format(self=self)


    def update(self, input_):
        """ gets updated control response for the input """
        # must get float for input_ - self.setpoint
        error = self.setpoint - input_
        delta_input = input_ - (self._last_input if self._last_input is not None else input_)

        # proportional term
        self._proportional = self.Kp * error

        # intergral terms
        self._integral += self.Ki * error #(* dt)
        self._integral = _bound(self._integral, self._output_limits)

        self._derivative = -self.Kd * delta_input #(/ dt)
        self._derivative = _bound(self._derivative, self._output_limits)

        output = self._proportional + self._integral + self._derivative
        output = _bound(output, self._output_limits)

        # keep track of state
        self._last_ouput = output
        self._last_input = input_

        return output
