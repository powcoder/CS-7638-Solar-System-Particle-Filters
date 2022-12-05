https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
import random
import math

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

PI = math.pi

for i in range(1, 10+1):
    test_case = i
    sun_mass = random.uniform(40, 60)
    planets = []
    num_planets = num_planets = 1 if 2 <= i <= 4 else random.randint(3, 5)
    dist_from_sun = 0
    for _ in range(num_planets):
        dist_from_sun += random.uniform(.9, 1)
        angle = random.uniform(0, 2*math.pi)
        planet_init_x = dist_from_sun * math.cos(angle)
        planet_init_y = dist_from_sun * math.sin(angle)
        planet_mass = random.uniform(1, 1000)      # 1 <= planet_mass <= 1000
        planets.append(((planet_init_x, planet_init_y), planet_mass))
    target_dist = random.uniform(.7, 4)
    target_angle = random.uniform(0, 2*math.pi)
    target_init_x = target_dist * math.cos(target_angle)
    target_init_y = target_dist * math.sin(target_angle)
    target_mass = random.uniform(.01, .05)
    target = ((target_init_x, target_init_y), target_mass)
    elliptical_orbit_factor = 1 if i < 8 else random.uniform(.5, .75)
    map_seed = random.randint(1, 5000)
    measurement_noise = random.uniform(1e-7, 1e-8)

    output = """'test_case': {},
     'sun_mass': {},
     'planets': {},
     'elliptical_orbit_factor': {},
     'target': {},
     'map_seed': {},
     'measurement_noise': {},
     'max_steps': 300
""".format(i, sun_mass, planets, elliptical_orbit_factor, target, map_seed, measurement_noise)

    print("    {" + output + "    },")
