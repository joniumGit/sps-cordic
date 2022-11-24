# Group 18
# Defining parameters
from dataclasses import dataclass
from math import degrees, radians
from typing import Optional


@dataclass
class Task1Params:
    phi_deg: float
    x: float
    y: float
    tolerance_deg: float


@dataclass
class Task3Params:
    phi_0_deg: float
    N: int
    sigma_max: float


# Task 1/2
task1 = Task1Params(
    phi_deg=151.0,
    x=-4.75,
    y=2.25,
    tolerance_deg=0.2,
)
task2 = task1

# Task 3
task3 = Task3Params(
    phi_0_deg=3.0,
    N=9,
    sigma_max=1E-4,
)


def find_N_for_tolerance(
        f,
        phi: float,
        x: float,
        y: float,
        tolerance: float,
        N_max: int = 20,
        opt_angle: bool = True,
) -> Optional[int]:
    """Finds minimal N-rounds for given error tolerance in result x and y

    :param f:           CORDIC implementation
    :param phi:         Rotation angle in radians
    :param x:           float
    :param y:           float
    :param tolerance:   float
    :param N_max:       Maximum rounds, default: 20
    :param opt_angle:   The tolerance should be interpreted as the maximum residual angle
    :return:            Value for N or None if max rounds was reached
    """
    for n in range(N_max):
        if opt_angle:
            max_err = abs(f(phi, x, y, n, output=False)[2])
        else:
            # Accounts for error in components instead of residual angle
            max_err = max(abs(f(phi, x, y, n, output=False)[3:]))
        if max_err < tolerance:
            return n


if __name__ == '__main__':
    from cordic_2 import cordic as cordic_2_value
    from cordic_3 import cordic as cordic_3_value

    for impl in [cordic_2_value, cordic_3_value]:
        # Evaluate for N, maximum 9 as this is near convergence of atan(2 ** -i)
        N_opt = find_N_for_tolerance(
            impl,
            radians(task1.phi_deg),
            task1.x,
            task1.y,
            tolerance=radians(task1.tolerance_deg),
            N_max=100
        )

        if not N_opt:
            raise RuntimeError('Failed to find N')

        # Display results
        _, _, z_err, _, _ = impl(radians(task1.phi_deg), task1.x, task1.y, N_opt)
        print(f'\nResidual angle error (deg): {abs(degrees(z_err)):^.5f} < {task1.tolerance_deg:.2f}')
