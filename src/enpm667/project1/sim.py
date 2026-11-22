
import numpy as np

from enpm667.project1.plot import Plotter
from enpm667.project1.control_laws import (
    equation_8,
    equation_14,
    bangbang_control,
    equation_19
)
import math


class Simulator():

    def __init__(
            self,
            name: str,
            max_time: int = 6,
            dt: float = 1e-3
        ) -> None:
        self.name = name
        self.max_time = max_time
        self.dt = dt

    def run_simulation(self):
        raise NotImplementedError

class SinglePendulumSimulator(Simulator):
    def __init__(
            self,
            name: str,
            w_0: float,
            n = float,
            init_state = list,
            k: float = 100,
            max_time: int = 6,
            dt: float = 1e-3
        ) -> None:
        super().__init__(
            name = name,
            max_time=max_time,
            dt=dt
        )
        self.w_0 = w_0
        self.n = n
        self.k = k
        self.init_state = init_state
        self.plotter = Plotter(name = self.name)

    def run_simulation(self):
        state = self.init_state.copy()

        for t in np.arange(0, self.max_time, self.dt):
            # compute E normalized from state
            E = (0.5/self.w_0**2) * state[1]**2 + math.cos(state[0]) - 1 

            # compute v = u/g (normalized u) from the state
            v = equation_8(
                k = self.k,
                E = E,
                theta=state[0],
                theta_dot=state[1],
                ng = self.n
            )

            self.plotter.add_data(t, state[0], E, v)
            
            # update state
            theta_dot_dot = self.w_0**2 * (math.sin(state[0]) - v * math.cos(state[0]))
            state[1] += theta_dot_dot * self.dt
            state[0] += state[1] * self.dt
    
        return self.plotter.plot()


class MinTimeSimulator(SinglePendulumSimulator):

    def __init__(
            self,
            name: str,
            w_0: float,
            n = float,
            init_state = list,
            max_time: int = 6,
            dt: float = 1e-3
        ) -> None:
        super().__init__(
            name = name,
            w_0 = w_0,
            n = n,
            init_state=init_state,
            k = 100,
            max_time=max_time,
            dt=dt
        )
        self.theta_star = equation_14(n)

        self.plotter = Plotter(name = self.name)

    def run_simulation(self):
        state = self.init_state.copy()

        for t in np.arange(0, self.max_time, self.dt):
            # compute E normalized from state
            E = (0.5/self.w_0**2) * state[1]**2 + math.cos(state[0]) - 1 

            # compute v = u/g (normalized u) from the state
            v = bangbang_control(
                theta=state[0],
                theta_star=self.theta_star,
                ng = self.n
            )

            self.plotter.add_data(t, state[0], E, v)
            
            # update state
            theta_dot_dot = self.w_0**2 * (math.sin(state[0]) - v * math.cos(state[0]))
            state[1] += theta_dot_dot * self.dt
            state[0] += state[1] * self.dt
    
        return self.plotter.plot()