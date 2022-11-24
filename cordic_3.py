from math import atan, prod, sqrt, pi, degrees, cos, sin
from typing import Tuple, List


def decision(value: float, i: int) -> int:
    """Returns desired decision (d_i) for step value z_i to produce z_i+1

    This looks into the future to see the step that minimizes the loss function

    LOSS = abs(next_step_value)

    :param value: z_i in z_i+1 = z_i - d_i * atan(2 ** -i)
    :param i:     current iteration
    :return:      d_i
    """
    return min(((d, abs(value - d * atan(2 ** -i))) for d in range(-1, 2)), key=lambda t: t[1])[0]


def calculate_A(rounds: int, decisions: List[int]) -> float:
    """Calculates A for N iterations

    This can be A_i or A_n
    This takes into account the decision history in 3 value CORDIC

    :param rounds:      N-rounds to calculate (product from 0 to N - 1)
    :param decisions:   Decision history
    :return:            value of A
    """
    return prod(sqrt(1 + 2 ** (-2 * i)) for i, d in zip(range(rounds), decisions) if d != 0)


def preprocess(phi: float, x: float, y: float, decisions: List[int]) -> Tuple[float, float, float]:
    """Calculates initial parameters for CORDIC to extend angle range

    :param phi:         rotation angle in radians
    :param x:           input X
    :param y:           input Y
    :param decisions:   Decision history
    :return:            x_0, y_0, z_0
    """
    d = decision(phi, 0)
    decisions.append(d)
    return (
        -d * y,
        d * x,
        phi - d * pi / 2,
    )


def gain_compensate(x: float, y: float, N: int, decisions: List[int]) -> Tuple[float, float]:
    """Gain compensates values by A for N-Rounds

    :param x:           float
    :param y:           float
    :param N:           int
    :param decisions:   Decision history
    :return:            transformed x and y
    """
    A = calculate_A(N, decisions)
    return x / A, y / A


def step(x_A: float, y_A: float, z: float, i: int, decisions: List[int]) -> Tuple[float, float, float]:
    """Calculates a CORDIC increment for given iteration i

    :param x_A:         x with gain
    :param y_A:         y with gain
    :param z:           value from previous iteration
    :param i:           int
    :param decisions:   Decision history
    :return:            next values of x, y, z
    """
    d = decision(z, i)
    decisions.append(d)
    return (
        x_A - d * y_A * 2 ** -i,
        y_A + d * x_A * 2 ** -i,
        z - d * atan(2 ** -i),
    )


def cordic(phi: float, x: float, y: float, N: int, output=True):
    if output:
        print('\nCORDIC:')
        print(
            f'|{"I": <2}'
            f'|{"Z (deg)": ^11}'
            f'| d'
            f'|{"atan(2^-i)": ^12}'
            f'|{"Z+1 (deg)": ^11}'
            f'|{"xA": ^11}'
            f'|{"yA": ^11}'
            f'|{"x": ^11}'
            f'|{"y": ^11}'
            f'|'
        )

    # State
    ds = []

    # Store for later
    _x = x
    _y = y

    # Iterate without recursion
    n = 0
    x, y, z = preprocess(phi, x, y, ds)
    z_prev = z

    while n < N:
        x, y, z = step(x, y, z, n, ds)

        if output:
            __x, __y = gain_compensate(x, y, n, ds)
            print(
                f'|{n: <2d}'
                f'|{degrees(z_prev): ^+11.2f}'
                f'|{decision(z_prev, n):+d}'
                f'|{degrees(atan(2 ** -n)): ^+12.2f}'
                f'|{degrees(z): ^+11.2f}'
                f'|{x: ^+11.2f}'
                f'|{y: ^+11.2f}'
                f'|{__x: ^+11.2f}'
                f'|{__y: ^+11.2f}'
                f'|'
            )

        n += 1
        z_prev = z

    if output:
        __x, __y = gain_compensate(x, y, n, ds)
        print(
            f'|{n: <2d}'
            f'|{degrees(z_prev): ^+11.2f}'
            f'|  '
            f'|{"" : ^12}'
            f'|{"" : ^11}'
            f'|{x: ^+11.2f}'
            f'|{y: ^+11.2f}'
            f'|{__x: ^+11.2f}'
            f'|{__y: ^+11.2f}'
            f'|'
        )
        print('\n      Result   [ Reference ] (  |Delta|  )')

    x, y = gain_compensate(x, y, n, ds)
    x_ref = _x * cos(phi) - _y * sin(phi)
    y_ref = _y * cos(phi) + _x * sin(phi)

    if output:
        print(f'x: {x: ^+11.5f} [{x_ref: ^+11.5f}] ({abs(x - x_ref): ^11.5f})')
        print(f'y: {y: ^+11.5f} [{y_ref: ^+11.5f}] ({abs(y - y_ref): ^11.5f})')
        print(f'CORDIC Gain: {calculate_A(n, ds):.6f}')
        print(f'Effective stages: {sum(1 for d in ds if d != 0)}')

    return x, y, z, abs(x - x_ref), abs(y - y_ref)


__all__ = ['cordic']
