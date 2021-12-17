import math

def theta_convert(input):
    pi = math.pi
    # convert rad domain to [-pi, pi]
    if input >=0:
        input = math.fmod(input, 2*pi)
        if input > pi:
            input -= 2*pi
            output = input
        else:
            output = input
    else:
        input *= -1
        input = math.fmod(input, 2*pi)
        if input > pi:
            input -= 2*pi
            output = input*-1
        else:
            output = input*-1
    return output