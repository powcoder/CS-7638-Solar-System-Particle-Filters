https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
from math import *
import random

######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

G = 6.6743e-11


class Body:
    """A body of mass.

    Attributes:
        r(List): the position vector of the body as [x, y]
        v(List): the velocity vector of the body as [v_x, v_y]
        mass(float): the mass of the body
    """

    def __init__(self, r, v, mass, measurement_noise):
        """
        Initialize a Body
        If no r position vector or v velocity vector is provided, sets these at default value [0, 0, 0]
        :param r: List[float, float]. The position of the body, such as [x, y]
        :param v: List[float, float]. The velocity of the body, such as [vx, vy]
        :param mass: float. The mass of the body
        :param measurement_noise: float. The measurement noise of the gravimeter, if any, on the body.
        """
        self.r = r if r is not None else [0, 0]
        self.v = v if v is not None else [0, 0]
        self.mass = mass
        self.measurement_noise = measurement_noise

    @classmethod
    def create_body_at_xy_in_orbit(cls, r, mass, measurement_noise, mass_sun):
        """
        Given a position vector and mass of sun, initializes a Body in circular orbit
        """
        x = r[0]
        y = r[1]
        radius_body = sqrt(x**2 + y**2)
        angle = atan2(y, x)

        velocity_magnitude = sqrt(G * mass_sun / radius_body)  # m/s
        heading = angle + pi / 2  # perpendicular
        velocity_x = velocity_magnitude * cos(heading)
        velocity_y = velocity_magnitude * sin(heading)
        return cls(r, [velocity_x, velocity_y], mass, measurement_noise)

    def compute_gravity_magnitude(self, planets):
        """
        Computes the magnitude of the sum of gravitational acceleration vectors
        from the planets at this body.
        """
        gravity = [0., 0.]
        for body in planets:
            # acceleration = G * M / r^2 = G * M / |r|^2 * -r / |r|
            direction = [body.r[i] - self.r[i] for i in range(2)]
            # catch for divide by zero by shifting it 1 meter
            if direction[0] == 0 and direction[1] == 0:
                direction[0] = 1
            c = G * body.mass / (direction[0] ** 2 + direction[1] ** 2) ** (3./2)
            gravity_by_body = [direction[0] * c, direction[1] * c]
            gravity = [gravity[i] + gravity_by_body[i] for i in range(2)]

        magnitude = sqrt(gravity[0] ** 2 + gravity[1] ** 2)
        return magnitude

    def sense(self, planets):
        """
        Measures the magnitude of the sum of gravitational acceleration vectors
        from the planets at this body.
        """
        measurement = self.compute_gravity_magnitude(planets)
        return random.gauss(measurement, self.measurement_noise)

    def get_radius(self):
        """ Returns the radius or distance from center """
        return sqrt(self.r[0]**2 + self.r[1]**2)

    def __repr__(self):
        """This allows us to print a Body's position

        Returns:
            String representation of a Body
        """
        return f'(r=[{self.r[0]:.0f}, {self.r[1]:.0f}], v=[{self.v[0]:.0f}, {self.v[1]:.0f}], mass={self.mass:.2f})'
