https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
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

#These import statements give you access to library functions which you may
# (or may not?) want to use.
from math import *
import random
from body import *
from solar_system import *


def estimate_next_pos(solar_system, gravimeter_measurement, other=None):
    """
    Estimate the next (x,y) position of the satelite.
    This is the function you will have to write for part A.

    :param solar_system: SolarSystem
        A model of the positions, velocities, and masses
        of the planets in the solar system, as well as the sun.
    :param gravimeter_measurement: float
        A floating point number representing
        the measured magnitude of the gravitation pull of all the planets
        felt at the target satellite at that point in time.
    :param other: any
        This is initially None, but if you return an OTHER from
        this function call, it will be passed back to you the next time it is
        called, so that you can use it to keep track of important information
        over time. (We suggest you use a dictionary so that you can store as many
        different named values as you want.)
    :return:
        estimate: Tuple[float, float]. The (x,y) estimate of the target satellite at the next timestep
        other: any. Any additional information you'd like to pass between invocations of this function
        optional_points_to_plot: List[Tuple[float, float, float]].
            A list of tuples like (x,y,h) to plot for the visualization
    """

    # example of how to get the gravity magnitude at a body in the solar system:
    particle = Body(r=[1*AU, 1*AU], v=[0, 0], mass=0, measurement_noise=0)
    particle_gravimeter_measurement = particle.compute_gravity_magnitude(planets=solar_system.planets)

    # You must return a tuple of (x,y) estimate, and OTHER (even if it is NONE)
    # in this order for grading purposes.

    xy_estimate = (0, 0)  # Sample answer, (X,Y) as a tuple.

    # TODO - remove this canned answer which makes this template code
    # pass one test case once you start to write your solution....
    xy_estimate = (129744950838.85445, 36955392255.3185)

    # You may optionally also return a list of (x,y,h) points that you would like
    # the PLOT_PARTICLES=True visualizer to plot for visualization purposes.
    # If you include an optional third value, it will be plotted as the heading
    # of your particle.

    optional_points_to_plot = [(1*AU, 1*AU), (2*AU, 2*AU), (3*AU, 3*AU)]  # Sample (x,y) to plot
    optional_points_to_plot = [(1*AU, 1*AU, 0.5), (2*AU, 2*AU, 1.8), (3*AU, 3*AU, 3.2)]  # (x,y,heading)

    return xy_estimate, other, optional_points_to_plot


def next_angle(solar_system, gravimeter_measurement, other=None):
    """
    Gets the next angle at which to send out an sos message to the home planet,
    the last planet in the solar system's planet list.
    This is the function you will have to write for part B.

    The input parameters are exactly the same as for part A.

    :return:
        bearing: float. The absolute angle from the satellite to send an sos message
        estimate: Tuple[float, float]. The (x,y) estimate of the target satellite at the next timestep
        other: any. Any additional information you'd like to pass between invocations of this function
        optional_points_to_plot: List[Tuple[float, float, float]].
            A list of tuples like (x,y,h) to plot for the visualization
    """
    # At what angle to send an SOS message this timestep
    bearing = 0.0
    estimate = (110172640485.32968, -66967324464.19617)

    # You may optionally also return a list of (x,y) or (x,y,h) points that
    # you would like the PLOT_PARTICLES=True visualizer to plot.
    #
    # optional_points_to_plot = [ (1*AU,1*AU), (2*AU,2*AU), (3*AU,3*AU) ]  # Sample plot points
    # return bearing, estimate, other, optional_points_to_plot

    return bearing, estimate, other


def who_am_i():
    # Please specify your GT login ID in the whoami variable (ex: jsmith222).
    whoami = ''
    return whoami
