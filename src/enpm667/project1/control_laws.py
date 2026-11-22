
import math

def sign(value: float) -> float:
    if value <= 0:
        return -1
    if value > 0:
        return 1

def sat(value: float, clamp_val: float) -> float:
    if value > clamp_val:
        return clamp_val
    if value < -clamp_val:
        return -clamp_val

    return value

def equation_8(k: float, E: float, theta: float, theta_dot: float, ng: float) -> float:
    val = k*(E - 0) * sign(theta_dot * math.cos(theta))

    return sat(val, ng)

def equation_9() -> float:
    pass

def bangbang_control(theta: float, theta_star: float, ng: float):
    if theta >= math.pi and theta < 3*math.pi/2:
        # swing to horizontal
        return ng
    elif theta >= 3*math.pi/2 and theta < 2*math.pi - theta_star:
        # swing up
        return -ng
    elif theta >= 2*math.pi - theta_star and theta < 2*math.pi:
        # kill energy before top
        return ng
    else:
        # upright, stop
        return 0

def equation_14(n: float) -> float:
    theta_star = math.asin(1 - (1/n))

    return theta_star

def equation_19(k: float, G: float, ng: float) -> float:
    return sat(k*G, ng)