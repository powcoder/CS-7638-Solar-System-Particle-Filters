https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
import math
import random
import unittest
import multiprocessing as mproc
import queue
import traceback
from solar_system import SolarSystem, AU

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

########################################################################
# For debugging set the time limit to a big number (like 600 or more)
# Note, if you turn on Verbose Logging
# or Plotting of Particles, you will want to increase this
# number from the 15 used in grading to a much higher value.
# If you have a fast computer, you may want to reduce this
# number to match your computer's speed to that of the
# VM used by GradeScope
########################################################################
TIME_LIMIT = 15  # seconds

########################################################################
# Additional flags for debug output and visualization
########################################################################
VERBOSE = False  # False for grading
PLOT_PARTICLES = False  # False for grading  (Set to True for Visualization!)

########################################################################
# Toggles for different parts of the assignment
########################################################################
PART_A = True  # Enable/disable Part A (Estimation) - True for grading
PART_B = True  # Enable/disable Part B (Steering) - True for grading

########################################################################
# If your debugger does not handle multiprocess debugging very easily
# then when debugging set the following flag true.
########################################################################
DEBUGGING_SINGLE_PROCESS = False

WINDOW_SIZE = 500  # Size of the window in "units"

# Note for Mac OS High Sierra users having problems with
# "an error occurred while attempting to obtain endpoint for listener" errors:
# Running with the following environment variable fixed this issue for one student.
# OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
# Looks like a problem specific to Mac OS High Sierra and internal threading libraries.

PI = math.pi
CREDIT_PER_PASS = 7  # points per test case pass.

# 10 test cases, ran in both parts A & B for 20 total.
# Max score if you get all test cases is potentially 140, but capped at 101 
# This means you do not need to get all test cases for a full score.

# The real test cases will be generated using generate_params_planet.py
# You are welcome to make your own test cases
# and share them on Piazza to expose issues that these test cases may miss.

MASS_SUN = 1.98847e30    # NOT FOR STUDENT USE
MASS_EARTH = 5.97219e24  # NOT FOR STUDENT USE

GLOBAL_PARAMETERS = [None,
                     # Note that sun_mass is multiplied by MASS_SUN,
                     # distances are multiplied by AU
                     # and planet/target masses are multiplied by MASS_EARTH

                     # Cases 1-2 have no noise.
                     # Cases 2-4 have a single planet.
                     # Cases 1, 5-10 have 3-5 planets.
                     # Cases 8-10 have elliptical planet orbits.

                     # Case 1 has no noise to make things easy for you!
                     {'test_case': 1,
                      'sun_mass': 43.842061607797625,
                      'planets': [((-0.9122000568392201, 0.307965701950435), 743.109985022544),
                                  ((1.0405026545494007, 1.565422786259), 198.63961059006155),
                                  ((-0.03098529348182052, -2.8597720510726266), 795.9959700442942)],
                      'elliptical_orbit_factor': 1,
                      'target': ((0.6560702910754909, 0.6560702910754909), 0.012056073017406379),
                      'map_seed': 3193,
                      'measurement_noise': 0,
                      'max_steps': 300
                      },
                     # Case 2 also has no noise
                     {'test_case': 2,
                      'sun_mass': 40.32651123452419,
                      'planets': [((0.748307466022684, -0.5501621585566954), 697.5659122010433)],
                      'elliptical_orbit_factor': 1,
                      'target': ((1.7448493082830823, -0.33922659527285975), 0.019530496057453304),
                      'map_seed': 2832,
                      'measurement_noise': 0,
                      'max_steps': 300
                      },
                     {'test_case': 3,
                      'sun_mass': 45.9390279105321,
                      'planets': [((-0.9804211803264786, -0.1715964281996233), 419.5934553172455)],
                      'elliptical_orbit_factor': 1,
                      'target': ((-2.225980367790211, -0.8399415743473132), 0.020020151506820256),
                      'map_seed': 1818,
                      'measurement_noise': 3.940227066209606e-08,
                      'max_steps': 300
                      },
                     {'test_case': 4,
                      'sun_mass': 46.68269826828132,
                      'planets': [((0.02695849446593085, 0.9637141458293313), 381.5299176351419)],
                      'elliptical_orbit_factor': 1,
                      'target': ((1.9126536132602072, 1.9126536132602072), 0.042374002771617604),
                      'map_seed': 3436,
                      'measurement_noise': 4.099203572901015e-08,
                      'max_steps': 300
                      },
                     {'test_case': 5,
                      'sun_mass': 49.36514115433552,
                      'planets': [((0.37243183622600984, -0.8842770214598261), 39.23145152714938),
                                  ((-0.6364793108767857, 1.8110452173486102), 136.28986540103276),
                                  ((0.06879472039655281, -2.9089969870426433), 173.0925410323392),
                                  ((-2.05583996748208, 3.265628185919691), 240.91483717124333)],
                      'elliptical_orbit_factor': 1,
                      'target': ((-0.36547756780945817, -0.36547756780945817), 0.0424805207809843),
                      'map_seed': 2672,
                      'measurement_noise': 9.181367944633899e-08,
                      'max_steps': 300
                      },
                     {'test_case': 6,
                      'sun_mass': 48.72824939209266,
                      'planets': [((0.3256689474273499, 0.8394736695676479), 442.8386636243171),
                                  ((1.7721240103548457, 0.35620373389299514), 514.8383043205001),
                                  ((-2.3207568542426897, -1.454273232137246), 40.05692612187196),
                                  ((-3.2966247766210475, 1.6857290194583818), 666.2068260714155)],
                      'elliptical_orbit_factor': 1,
                      'target': ((-2.4329187338980494, -2.4329187338980494), 0.02574382490665504),
                      'map_seed': 2742,
                      'measurement_noise': 9.858204257266145e-08,
                      'max_steps': 300
                      },
                     {'test_case': 7,
                      'sun_mass': 54.0938761021251,
                      'planets': [((-0.231602556934255, -0.889870387863436), 25.370281838622464),
                                  ((-1.5784244672580832, 0.9554054019225564), 393.11294534231115),
                                  ((0.8375908071936017, -2.7011732727305793), 382.6190953707185),
                                  ((2.5603586898940254, -2.721123602053259), 748.5978823302723),
                                  ((-2.9749561600471552, 3.5875544722242947), 801.73840561633)],
                      'elliptical_orbit_factor': 1,
                      'target': ((-2.561679975171908, -0.1786219211871244), 0.024327715938244218),
                      'map_seed': 4687,
                      'measurement_noise': 8.2442001068741e-08,
                      'max_steps': 300
                      },
                     {'test_case': 8,
                      'sun_mass': 51.42491139397881,
                      'planets': [((-0.8822853436169761, 0.35956874874350164), 202.629302718903),
                                  ((1.6041334569510557, 1.0467146998751635), 475.0665454825634),
                                  ((2.500103605684226, -1.462887693110299), 204.90588999278523),
                                  ((2.8683176141710107, -2.562869682480658), 258.229807739354),
                                  ((3.1599286499947588, 3.594378979419109), 976.8801103238544)],
                      'elliptical_orbit_factor': 0.7473696829601248,
                      'target': ((0.30414513207533167, 0.8538929820336406), 0.015488566252828347),
                      'map_seed': 3454,
                      'measurement_noise': 3.246153585769787e-08,
                      'max_steps': 300
                      },
                     {'test_case': 9,
                      'sun_mass': 44.65547999808227,
                      'planets': [((0.6348717055275535, -0.6923360388055648), 593.3821544996055),
                                  ((1.4979452945200982, -1.169299103527468), 360.2409619519721),
                                  ((1.15963923726884, 2.5827195690908415), 367.6590824762749),
                                  ((3.747648062849885, 0.1346082262665511), 346.3476965183801),
                                  ((4.4009787368270175, 1.568320682246742), 708.1145889638916)],
                      'elliptical_orbit_factor': 0.5131219019570615,
                      'target': ((-1.678502067820535, -1.678502067820535), 0.03332174377942925),
                      'map_seed': 4265,
                      'measurement_noise': 7.965728904474786e-08,
                      'max_steps': 300
                      },
                     {'test_case': 10,
                      'sun_mass': 43.91101670058105,
                      'planets': [((-0.6159704854212522, 0.7572261480543556), 745.260269507586),
                                  ((-1.773657035462997, -0.7715133207842724), 294.17182205477417),
                                  ((-2.473479942931434, -1.4355488298363925), 68.31428555435444)],
                      'elliptical_orbit_factor': 0.6005628722695515,
                      'target': ((2.7329789298341423, 2.7329789298341423), 0.04180544561258218),
                      'map_seed': 1859,
                      'measurement_noise': 4.359226973135861e-08,
                      'max_steps': 300
                      },

]


# Try importing the student code here:

try:
    import solar_locator

    planet1Exc = None
except Exception as e:
    print("Error importing solar_locator.py:", e)
    planet1Exc = e


class PlanetSimulator(object):
    """Run student submission code.

    Attributes:
        satellite_steps(Queue): synchronized queue to store planet steps.
        satellite_found(Queue): synchronized queue to store if planet located.
        satellite_error(Queue): synchronized queue to store exception messages.
    """

    def __init__(self):

        if DEBUGGING_SINGLE_PROCESS:

            self.satellite_steps = queue.Queue(1)
            self.satellite_found = queue.Queue(1)
            self.satellite_error = queue.Queue(1)

        else:

            self.satellite_steps = mproc.Queue(1)
            self.satellite_found = mproc.Queue(1)
            self.satellite_error = mproc.Queue(1)

    def _reset(self):
        """Reset submission results.
        """
        while not self.satellite_steps.empty():
            self.satellite_steps.get()

        while not self.satellite_found.empty():
            self.satellite_found.get()

        while not self.satellite_error.empty():
            self.satellite_found.get()

    @staticmethod
    def distance(p, q):
        """Calculate the distance between two points.

        Args:
            p(tuple): point 1.
            q(tuple): point 2.

        Returns:
            distance between points.
        """
        x1, y1 = p[0], p[1]
        x2, y2 = q

        dx = x2 - x1
        dy = y2 - y1

        return math.sqrt(dx ** 2 + dy ** 2)

    def simulate_without_sos(self, estimate_next_pos, params):
        """Run simulation only to locate planet.

        Args:
            estimate_next_pos(func): Student submission function to estimate next planet position.
            params(dict): Test parameters.

        Raises:
            Exception if error running submission.
        """
        self._reset()

        # make the test somewhat repeatable by seeding the RNG.
        random.seed(params['map_seed'])

        # build world
        planets_r_and_mass = []
        for planet_params in params['planets']:
            planet_r = tuple(v * AU for v in planet_params[0])
            planet_mass = planet_params[1] * MASS_EARTH
            planets_r_and_mass.append((planet_r, planet_mass))

        solar_system = SolarSystem(mass_sun=MASS_SUN * params['sun_mass'],
                                   planets_r_and_mass=planets_r_and_mass,
                                   elliptical_orbit_factor=params['elliptical_orbit_factor'])

        target_r = tuple(v * AU for v in params['target'][0])
        target_mass = params['target'][1] * MASS_EARTH
        target = SolarSystem.init_body_in_orbit_at_x_and_y(
            mass_sun=solar_system.sun.mass,
            r=target_r,
            mass_body=target_mass,
            measurement_noise=params['measurement_noise'])

        tolerance = .01 * AU
        other_info = None
        steps = 0

        # Set up the particle plotter if requested
        if PLOT_PARTICLES:
            import turtle  # Only import if plotting is on.
            turtle.setup(width=WINDOW_SIZE, height=WINDOW_SIZE)
            turtle.setworldcoordinates(-5, -5, 5, 5)

            # paint bg black
            turtle.clearscreen()
            turtle.colormode(255)
            turtle.bgcolor("black")
            turtle.delay(0)
            turtle.hideturtle()
            turtle.penup()

            # set starting point for satellite trail
            turtle.setposition(target.r[0] / AU, target.r[1] / AU)
            turtle.pencolor("red")
            turtle.pendown()
            turtle.ht()

            # declare turtles
            sun_turtle = None
            planet_turtle_list = None
            target_turtle = None
            estimate_turtle = None
            turtle_list = []
            time_turtle = turtle.Turtle(visible=False)
            time_turtle.setposition(3, -5)

            tc_turtle = turtle.Turtle(visible=False)
            tc_turtle.setposition(-5, -5)
            tc_turtle.color("white")
            tc_turtle.write(f'Test Case: {params["test_case"]}')

        try:
            while steps < params['max_steps']:

                # Invoke student function to get student result
                gravimeter_measurement = target.sense(solar_system.planets)
                result = estimate_next_pos(solar_system=solar_system, gravimeter_measurement=gravimeter_measurement, other=other_info)
                if len(result) == 3:
                    xy_estimate, other_info, optional_points_to_plot = result
                    if not isinstance(optional_points_to_plot, list):
                        raise TypeError(f"Expected returned optional_points_to_plot to be a list "
                                        f"but it was actually a {type(optional_points_to_plot)}")
                    if len(optional_points_to_plot) > 0:
                        if not isinstance(optional_points_to_plot[0], tuple):
                            raise TypeError(f"Expected the element in optional_points_to_plot to be a tuple "
                                            f"but it was actually a {type(optional_points_to_plot[0])}")
                        if len(optional_points_to_plot[0]) < 2 or len(optional_points_to_plot[0]) > 3:
                            raise TypeError(f"Expected the element in optional_points_to_plot to have 2-3 elements, "
                                            f"such as (x,y) or (x,y,h), "
                                            f"but it had {len(optional_points_to_plot[0])} elements: "
                                            f"{optional_points_to_plot[0]}")
                elif len(result) == 2:
                    xy_estimate, other_info = result
                    optional_points_to_plot = None
                else:
                    msg = "estimate_next_pos did not return correct number of return values!"
                    print(msg)
                    raise TypeError(msg)

                if not isinstance(xy_estimate, tuple):
                    raise TypeError(f"Expected the returned xy_estimate to be a tuple "
                                    f"but it was actually a {type(xy_estimate)}")
                if len(xy_estimate) != 2:
                    raise TypeError(f"Expected the returned xy_estimate to have 2 elements, such as (x,y), "
                                    f"but it had {len(optional_points_to_plot[0])} elements: {xy_estimate}")

                # Calculate the actual result position of the target next timestep.
                target = solar_system.move_body(target)
                target_pos = (target.r[0], target.r[1])

                # Rotate the solar system for the next timestep
                solar_system.move_planets()

                if PLOT_PARTICLES:

                    s = turtle.getscreen()
                    s.tracer(0, 1)

                    # plot particles
                    if optional_points_to_plot:
                        # Add turtles if needed.
                        while len(optional_points_to_plot) > len(turtle_list):
                            new_turtle = turtle.Turtle()
                            new_turtle.penup()
                            turtle_list.append(new_turtle)

                        # remove turtles if needed.
                        while len(optional_points_to_plot) < len(turtle_list):
                            turtle_list[-1].hideturtle()
                            turtle_list = turtle_list[0:-1]

                        # paint particles
                        for i in range(len(optional_points_to_plot)):
                            t = turtle_list[i]
                            p = optional_points_to_plot[i]
                            # Optionally plot heading if provided by student
                            if len(p) > 2:
                                t.shape("triangle")
                                t.shapesize(0.2, 0.4)
                                t.settiltangle(p[2] * 180 / math.pi)
                            else:
                                t.shape("circle")
                                t.shapesize(0.1, 0.1)
                            t.fillcolor("white")
                            t.color("white")
                            t.setposition(p[0] / AU, p[1] / AU)

                    # Draw the target satellite.
                    if target_turtle is not None:
                        target_turtle.hideturtle()
                    if target_turtle is None:
                        target_turtle = turtle.Turtle()
                        target_turtle.shape("circle")
                        target_turtle.shapesize(.25, .25)
                        target_turtle.pencolor("red")
                        target_turtle.fillcolor("red")
                        target_turtle.penup()
                    target_turtle.setposition(target_pos[0] / AU, target_pos[1] / AU)
                    target_turtle.showturtle()

                    # move planet target turtle and trail
                    turtle.setposition(target.r[0] / AU, target.r[1] / AU)

                    # Draw the student estimate of the satellite
                    if estimate_turtle is not None:
                        estimate_turtle.hideturtle()
                    if estimate_turtle is None:
                        estimate_turtle = turtle.Turtle()
                        estimate_turtle.shape("square")
                        estimate_turtle.shapesize(.2, .2)
                        estimate_turtle.fill = False
                        estimate_turtle.color("cyan")
                        estimate_turtle.penup()
                    estimate_turtle.setposition(xy_estimate[0] / AU, xy_estimate[1] / AU)
                    estimate_turtle.showturtle()

                    # Draw the sun
                    if sun_turtle is not None:
                        sun_turtle.hideturtle()
                    if sun_turtle is None:
                        sun_turtle = turtle.Turtle()
                        sun_turtle.shape("circle")
                        sun_turtle.shapesize(.75, .75)
                        sun_turtle.fill = False
                        sun_turtle.color("yellow")
                        sun_turtle.penup()
                    sun_turtle.setposition(0, 0)
                    sun_turtle.showturtle()

                    # Draw the planets
                    if planet_turtle_list is None:
                        planet_turtle_list = [turtle.Turtle() for _ in range(solar_system.get_num_planets())]
                        for i, planet_turtle in enumerate(planet_turtle_list or []):
                            size = .1 + solar_system.planets[i].mass / MASS_EARTH / 1000 * .4
                            planet_turtle.shape("circle")
                            planet_turtle.shapesize(size, size)
                            planet_turtle.pencolor("lime")
                            planet_turtle.fillcolor("lime")
                            planet_turtle.penup()
                            x = solar_system.planets[i].r[0] / AU
                            y = solar_system.planets[i].r[1] / AU
                            planet_turtle.setposition(x, y)
                            planet_turtle.pendown()
                    else:
                        for i, planet_turtle in enumerate(planet_turtle_list or []):
                            x = solar_system.planets[i].r[0] / AU
                            y = solar_system.planets[i].r[1] / AU
                            planet_turtle.setposition(x, y)
                            planet_turtle.showturtle()

                    # Draw steps
                    time_turtle.clear()
                    time_turtle.color("white")
                    time_turtle.write(f'Time Step: {steps}')

                    s.update()

                separation = self.distance(xy_estimate, target_pos)
                if separation < tolerance:
                    self.satellite_found.put(True)
                    self.satellite_steps.put(steps)
                    return

                steps += 1

                if VERBOSE is True:
                    print(
                        "\nStep: {} Actual ({})  Predicted: ({})\n  Difference = {}\n  Gravity Magnitude={}".format(
                            steps, target_pos, xy_estimate, separation, gravimeter_measurement))
                    if optional_points_to_plot is not None and len(optional_points_to_plot) > 0:
                        particle_dist = []
                        for p in optional_points_to_plot:
                            dist = self.distance(p, target_pos)
                            particle_dist.append(dist)
                        pMin = min(particle_dist)
                        pMax = max(particle_dist)
                        pAvg = sum(particle_dist) / float(len(particle_dist))
                        print("{} Particles, Min dist: {}, Avg dist: {}, Max Dist: {}".format(len(optional_points_to_plot), pMin,
                                                                                              pAvg, pMax))

            self.satellite_found.put(False)
            self.satellite_steps.put(steps)

        except:
            self.satellite_error.put(traceback.format_exc())

    def simulate_with_sos(self, next_angle, params):
        #Run simulation allow satellite to fire SOS messages.
        """
        Args:
            next_angle(func): Student submission function for angle to send sos message.
            params(dict): Test parameters.

        Raises:
            Exception if error running submission.
        """
        self._reset()

        # make the test somewhat repeatable by seeding the RNG.
        random.seed(params['map_seed'])

        # build world
        planets_r_and_mass = []
        for planet_params in params['planets']:
            planet_r = tuple(v * AU for v in planet_params[0])
            planet_mass = planet_params[1] * MASS_EARTH
            planets_r_and_mass.append((planet_r, planet_mass))

        solar_system = SolarSystem(mass_sun=MASS_SUN * params['sun_mass'],
                                   planets_r_and_mass=planets_r_and_mass,
                                   elliptical_orbit_factor=params['elliptical_orbit_factor'])

        target_r = tuple(v * AU for v in params['target'][0])
        target_mass = params['target'][1] * MASS_EARTH
        target = SolarSystem.init_body_in_orbit_at_x_and_y(
            mass_sun=solar_system.sun.mass,
            r=target_r,
            mass_body=target_mass,
            measurement_noise=params['measurement_noise'])

        tolerance = .05 * AU
        other_info = None
        steps = 0

        sos_trans_steps = 3
        hits = 0
        success_hits = 10
        bodies = solar_system.planets
        num_planets = solar_system.get_num_planets()

        # Set up the particle plotter if requested
        if PLOT_PARTICLES:
            import turtle  # Only import if plotting is on.
            turtle.tracer(n=0)
            turtle.setup(width=WINDOW_SIZE, height=WINDOW_SIZE)
            turtle.setworldcoordinates(-5, -5, 5, 5)

            # paint bg black
            turtle.clearscreen()
            turtle.colormode(255)
            turtle.bgcolor("black")
            turtle.delay(0)
            turtle.hideturtle()
            turtle.penup()

            # set starting point for satellite trail
            turtle.setposition(target.r[0] / AU, target.r[1] / AU)
            turtle.pencolor("red")
            turtle.pendown()
            turtle.ht()

            # declare turtles
            sun_turtle = None
            planet_turtle_list = None
            target_turtle = None
            estimate_turtle = None
            comms_turtle = None
            turtle_list = []
            time_turtle = turtle.Turtle(visible=False)
            time_turtle.setposition(3, -5)

            tc_turtle = turtle.Turtle(visible=False)
            tc_turtle.setposition(-5, -5)
            tc_turtle.color("white")
            tc_turtle.write(f'Test Case: {params["test_case"]}')

            msg_turtle = turtle.Turtle(visible=False)
            msg_turtle.setposition(-3, -5)
            msg_turtle.color("white")
            msg_turtle.write(f'Message Transmission Progress:')

            progress_squares = []
            color_map = [
                '#FF4E11',
                '#FF8E15',
                '#FF8E15',
                '#FAB733',
                '#FAB733',
                '#E8DE04',
                '#E8DE04',
                '#00D100',
                '#00D100',
                '#00D100',
            ]

            for i in range(success_hits):
                sq = turtle.Turtle(visible=False)
                sq.setposition(.2+(.2*i), -5)
                sq.color("white")
                sq.fillcolor(color_map[i])
                for i in range(4):
                        sq.forward(.2)
                        sq.left(90)
                progress_squares.append(sq)

        try:
            while steps < params['max_steps']:

                # Invoke student function to get student result
                gravimeter_measurement = target.sense(solar_system.planets)
                result = next_angle(solar_system=solar_system, gravimeter_measurement=gravimeter_measurement, other=other_info)
                if len(result) == 4:
                    bearing, xy_estimate, other_info, optional_points_to_plot = result

                    if not isinstance(optional_points_to_plot, list):
                        raise TypeError(f"Expected returned optional_points_to_plot to be a list "
                                        f"but it was actually a {type(optional_points_to_plot)}")
                    if len(optional_points_to_plot) > 0:
                        if not isinstance(optional_points_to_plot[0], tuple):
                            raise TypeError(f"Expected the element in optional_points_to_plot to be a tuple "
                                            f"but it was actually a {type(optional_points_to_plot[0])}")
                        if len(optional_points_to_plot[0]) < 2 or len(optional_points_to_plot[0]) > 3:
                            raise TypeError(f"Expected the element in optional_points_to_plot to have 2-3 elements, "
                                            f"such as (x,y) or (x,y,h), "
                                            f"but it had {len(optional_points_to_plot[0])} elements: "
                                            f"{optional_points_to_plot[0]}")
                elif len(result) == 3:
                    bearing, xy_estimate, other_info = result
                    optional_points_to_plot = None
                else:
                    print("next_angle did not return correct number of return values!")

                if not isinstance(bearing, float):
                    raise TypeError(f"Expected the returned bearing to be a float "
                                    f"but it was actually a {type(bearing)}")
                if not isinstance(xy_estimate, tuple):
                    raise TypeError(f"Expected the returned xy_estimate to be a tuple "
                                    f"but it was actually a {type(xy_estimate)}")
                if len(xy_estimate) != 2:
                    raise TypeError(f"Expected the returned xy_estimate to have 2 elements, such as (x,y), "
                                    f"but it had {len(optional_points_to_plot[0])} elements: {xy_estimate}")

                # Calculate actual result position and bearing of the target next timestep
                target = solar_system.move_body(target)
                target_pos = (target.r[0], target.r[1])
                bearing = max(-PI, bearing)
                bearing = min(bearing, PI)

                # Rotate the solar system for the next timestep
                solar_system.move_planets()

                hit = False

                if steps % sos_trans_steps == 0:

                    # Transmit SoS towards home planet
                    home_planet_index = num_planets - 1
                    home_planet_vect = bodies[home_planet_index].r
                    home_planet_loc = (home_planet_vect[0], home_planet_vect[1])
                    target_x, target_y = target_pos

                    t0 = (home_planet_vect[0] - target_x) * math.cos(bearing) + (home_planet_vect[1] - target_y) * math.sin(bearing)

                    closest_point = (target_x + t0*math.cos(bearing) , target_y + t0*math.sin(bearing))
                    separation = self.distance(home_planet_loc, closest_point)

                    point1 = (target_x / AU, target_y / AU)
                    point2 = (target_x / AU + WINDOW_SIZE * math.cos(bearing),
                              target_y / AU + WINDOW_SIZE * math.sin(bearing))

                    if separation < tolerance:
                        point2 = ((target_x + t0 * math.cos(bearing)) / AU, (target_y + t0 * math.sin(bearing)) / AU)
                        hit = True
                        hits += 1
                    else:
                        pass

                    sos_attempt = True

                else:
                    sos_attempt = False

                if PLOT_PARTICLES:

                    s = turtle.getscreen()
                    s.tracer(0, 1)

                    # plot particles
                    if optional_points_to_plot:

                        # Add turtles if needed.
                        while len(optional_points_to_plot) > len(turtle_list):
                            new_turtle = turtle.Turtle()
                            new_turtle.penup()
                            turtle_list.append(new_turtle)

                        # remove turtles if needed.
                        while len(optional_points_to_plot) < len(turtle_list):
                            turtle_list[-1].hideturtle()
                            turtle_list = turtle_list[0:-1]

                        # paint particles
                        for i in range(len(optional_points_to_plot)):
                            t = turtle_list[i]
                            p = optional_points_to_plot[i]
                            # Optionally plot heading if provided by student
                            if len(p) > 2:
                                t.shape("triangle")
                                t.shapesize(0.2, 0.4)
                                t.settiltangle(p[2] * 180 / math.pi)
                            else:
                                t.shape("circle")
                                t.shapesize(0.1, 0.1)
                            t.fillcolor("white")
                            t.color("white")
                            t.setposition(p[0] / AU, p[1] / AU)

                    # Draw the target satellite.
                    if target_turtle is not None:
                        target_turtle.hideturtle()
                    if target_turtle is None:
                        target_turtle = turtle.Turtle()
                        target_turtle.shape("circle")
                        target_turtle.shapesize(.25, .25)
                        target_turtle.pencolor("red")
                        target_turtle.fillcolor("red")
                        target_turtle.penup()
                    target_turtle.setposition(target_pos[0] / AU, target_pos[1] / AU)
                    target_turtle.showturtle()

                    # move planet target turtle and trail
                    turtle.setposition(target.r[0] / AU, target.r[1] / AU)

                    # Draw the student estimate of the satellite
                    if estimate_turtle is not None:
                        estimate_turtle.hideturtle()
                    if estimate_turtle is None:
                        estimate_turtle = turtle.Turtle()
                        estimate_turtle.shape("square")
                        estimate_turtle.shapesize(.2, .2)
                        estimate_turtle.fill = False
                        estimate_turtle.color("cyan")
                        estimate_turtle.penup()
                    estimate_turtle.setposition(xy_estimate[0] / AU, xy_estimate[1] / AU)
                    estimate_turtle.showturtle()

                    # Draw the sun
                    if sun_turtle is not None:
                        sun_turtle.hideturtle()
                    if sun_turtle is None:
                        sun_turtle = turtle.Turtle()
                        sun_turtle.shape("circle")
                        sun_turtle.shapesize(.75, .75)
                        sun_turtle.fill = False
                        sun_turtle.color("yellow")
                        sun_turtle.penup()
                    sun_turtle.setposition(0, 0)
                    sun_turtle.showturtle()

                    # Draw the planets
                    if planet_turtle_list is None:
                        planet_turtle_list = [turtle.Turtle() for _ in range(solar_system.get_num_planets())]
                        for i, planet_turtle in enumerate(planet_turtle_list or []):
                            size = .1 + solar_system.planets[i].mass / MASS_EARTH / 1000 * .4
                            planet_turtle.shape("circle")
                            planet_turtle.shapesize(size, size)
                            planet_turtle.pencolor("lime")
                            planet_turtle.fillcolor("lime")
                            if i == home_planet_index:
                                planet_turtle.pencolor("skyblue")
                                planet_turtle.fillcolor("magenta")
                            planet_turtle.penup()
                            x = solar_system.planets[i].r[0] / AU
                            y = solar_system.planets[i].r[1] / AU
                            planet_turtle.setposition(x, y)
                            planet_turtle.pendown()
                    else:
                        for i, planet_turtle in enumerate(planet_turtle_list or []):
                            x = solar_system.planets[i].r[0] / AU
                            y = solar_system.planets[i].r[1] / AU
                            planet_turtle.setposition(x, y)
                            planet_turtle.showturtle()

                    # Draw steps
                    time_turtle.clear()
                    time_turtle.color("white")
                    time_turtle.write(f'Time Step: {steps}')

                    # Draw communication towards target planet.
                    if comms_turtle is not None:
                        comms_turtle.hideturtle()
                    if comms_turtle is None:
                        comms_turtle = turtle.Turtle()
                        comms_turtle.pencolor("red")
                        comms_turtle.penup()
                    if sos_attempt == True:
                        if hit:
                            comms_turtle.pencolor("green")
                            sq = progress_squares[hits-1]
                            sq.begin_fill()
                            for i in range(4):
                                sq.forward(.2)
                                sq.left(90)
                            sq.end_fill()
                        else:
                            comms_turtle.pencolor("red")

                        comms_turtle.goto(point1)
                        comms_turtle.pendown()
                        comms_turtle.goto(point2)
                        comms_turtle.penup()
                    else:
                        comms_turtle.clear()

                    s.update()

                if hits >= success_hits:
                    self.satellite_found.put(True)
                    self.satellite_steps.put(steps)
                    return

                steps += 1

            self.satellite_found.put(False)
            self.satellite_steps.put(steps)

        except:
            self.satellite_error.put(traceback.format_exc())


NOT_FOUND = "Part {} - Test Case {}: planet took {} step(s) which exceeded the {} allowable step(s)."


class CaseRunner(unittest.TestCase):
    """Run test case using specified parameters.

    Attributes:
        simulator(PlanetSimulator): Simulation.
    """

    @classmethod
    def setUpClass(cls):
        """Setup test class.
        """
        cls.simulator = PlanetSimulator()

    def run_with_params(self, k, test_params, test_method, student_method):
        """Run test case with parameters.

        Args:
            k(int): Test case global parameters.
            test_params(dict): Test parameters.
            test_method(func): Test function.
            student_method(func): Student submission function.
        """
        test_params.update(GLOBAL_PARAMETERS[k])

        error_message = ''
        steps = None
        planet_found = False

        if DEBUGGING_SINGLE_PROCESS:
            test_method(student_method, test_params)
        else:
            test_process = mproc.Process(target=test_method, args=(student_method, test_params))

            try:
                test_process.start()
                test_process.join(TIME_LIMIT)
            except Exception as exp:
                error_message += str(exp) + ' '

            if test_process.is_alive():
                test_process.terminate()
                error_message = ('Test aborted due to CPU timeout. ' +
                                 'Test was expected to finish in fewer than {} second(s).'.format(TIME_LIMIT))
                print(error_message)

        if not error_message:
            if not self.simulator.satellite_error.empty():
                error_message += self.simulator.satellite_error.get()

            if not self.simulator.satellite_found.empty():
                planet_found = self.simulator.satellite_found.get()

            if not self.simulator.satellite_steps.empty():
                steps = self.simulator.satellite_steps.get()

        self.assertFalse(error_message, error_message)
        self.assertTrue(planet_found, NOT_FOUND.format(test_params['part'],
                                                       test_params['test_case'],
                                                       steps,
                                                       test_params['max_steps']))


class PartATestCase(CaseRunner):
    """Test Part A (localization only, no messaging)

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """

    def setUp(self):
        """Setup for each test case.
        """

        if planet1Exc:
            raise planet1Exc

        self.test_method = self.simulator.simulate_without_sos
        self.student_method = solar_locator.estimate_next_pos

        self.params = dict()
        self.params['part'] = 'A'

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


class PartBTestCase(CaseRunner):
    """Test Part B (localization and messaging SOS to home planet )

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """

    def setUp(self):
        """Setup for each test case.
        """

        if planet1Exc:
            raise planet1Exc

        self.test_method = self.simulator.simulate_with_sos
        self.student_method = solar_locator.next_angle

        self.params = dict()
        self.params['part'] = 'B'

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


# This flag is used to check whether project files listed in the json have been modified.
# Modifications include (but are mot limited to) print statements, changing flag values, etc.
# If you have modified the project files in some way, The results may not be accurate
# turn file_checker on by setting the flag to True to ensure you are running against
# the same framework as the Gradescope autograder.
file_checker = False  # set to True to turn file checking on

if file_checker:
    import json
    import hashlib
    import pathlib
    print("File checking is turned on.")
    with open('file_check.json', 'r') as openfile:
        json_dict = json.load(openfile)

    modified_files = []
    for file in json_dict:
        f = str(file)
        try:
            file_hash = hashlib.md5(pathlib.Path(file).read_bytes()).hexdigest()
            if file_hash != json_dict[f]:
                modified_files.append(f)
        except:
            print(f'File ({f}) not in project folder.')

    if len(modified_files) == 0:
        print("You are running against the same framework as the Gradescope autograder.")
    else:
        print("Warning. The following files have been modified and the results may not be accurate:")
        print(", ".join(modified_files))

# Only run all of the test automatically if this file was executed from the command line.
# Otherwise, let Nose/py.test do it's own thing with the test cases.
if __name__ == "__main__":
    student_id = solar_locator.who_am_i()
    if student_id:
        cases = []
        if PART_A is True:
            cases.append(PartATestCase)
        if PART_B is True:
            cases.append(PartBTestCase)
        suites = [unittest.TestSuite(unittest.TestLoader().loadTestsFromTestCase(case)) for case in cases]

        total_passes = 0

        try:
            for i, suite in zip(list(range(1, 1 + len(suites))), suites):
                print("====================\nTests for Part {}:".format(i))

                result = unittest.TestResult()
                suite.run(result)

                for x in result.errors:
                    print(x[0], x[1])
                for x in result.failures:
                    print(x[0], x[1])

                num_errors = len(result.errors)
                num_fails = len(result.failures)
                num_passes = result.testsRun - num_errors - num_fails
                total_passes += num_passes

                print("Successes: {}\nFailures: {}\n".format(num_passes, num_errors + num_fails))

                # We cap the maximum score to 101 if they pass more than 12.5 test cases.
                overall_score = total_passes * CREDIT_PER_PASS
        except Exception as e:
            print(e)
            overall_score = 0
        if overall_score > 100:
            print("Score above 100:", overall_score, " capped to 101!")
            overall_score = 101
        print("====================\nOverall Score: {}".format(overall_score))
    else:
        print("Student ID not specified.  Please fill in 'whoami' variable.")
        print('score: 0')
