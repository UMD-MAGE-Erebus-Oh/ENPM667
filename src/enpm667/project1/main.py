
import numpy as np
import math
import matplotlib.pyplot as plt

from enpm667.project1.plot import Plotter, TwoPendulumPlotter
from enpm667.project1.control_laws import (
    equation_8,
    equation_14,
    bangbang_control,
    equation_19
)
from enpm667.project1.sim import SinglePendulumSimulator, MinTimeSimulator

from pathlib import Path

THIS_DIR = Path(__file__).parent

SAVE_DIR = THIS_DIR.parent.parent.parent / "project1"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

theta_0 = math.pi
theta_dot_0 = 0

dt = 0.001

def ssds():
    w_0 = 1
    n = 2.1
    k = 100

    sim = SinglePendulumSimulator(
        name="Single Swing Double Switch n=2.1",
        w_0 = w_0,
        n = n,
        init_state = [theta_0, theta_dot_0],
        k = k,
        max_time=6,
        dt = dt
    )
    sim.run_simulation()

def ssts():
    w_0 = 1
    n = 1.5
    k = 100

    sim = SinglePendulumSimulator(
        name="Single Swing Triple Switch n=1.5",
        w_0 = w_0,
        n = n,
        init_state = [theta_0, theta_dot_0],
        k = k,
        max_time=6,
        dt = dt
    )
    sim.run_simulation()

def multi():
    w_0 = 1
    n = 0.25
    k = 100

    sim = SinglePendulumSimulator(
        name="Five Swings n=0.25",
        w_0 = w_0,
        n = n,
        init_state = [theta_0, theta_dot_0],
        k = k,
        max_time=20,
        dt = dt
    )
    sim.run_simulation()

def bangbang():

    # n = 2.1
    w_0 = 1
    n = 2.1
    theta_star = equation_14(n)

    plotter = Plotter(name = "Min Time n=2.1")

    state = [theta_0, theta_dot_0]

    sim = MinTimeSimulator(
        name="Min Time n=2.1",
        w_0 = w_0,
        n = n,
        init_state = [theta_0, theta_dot_0],
        max_time=5,
        dt = dt
    )
    sim.run_simulation()

    sim_baseline = SinglePendulumSimulator(
        name="Baseline Single Swing Double Switch n=2.1",
        w_0 = w_0,
        n = n,
        init_state = [theta_0, theta_dot_0],
        k = 100,
        max_time=5,
        dt = dt
    )
    sim_baseline.run_simulation()

    # plot both
    plotter = sim.plotter
    baseline_plotter = sim_baseline.plotter

    fig, axs = plt.subplots(3, 1, figsize=(18, 18))

    axs[0].plot(plotter.ts, plotter.thetas, label="Min Time")
    axs[0].plot(baseline_plotter.ts, baseline_plotter.thetas, label="Standard")
    axs[0].set_title("Pendulum Angles (theta)")
    axs[0].legend()
    axs[0].set_ylabel("Angle (radians)")

    axs[1].plot(plotter.ts, plotter.e_norms, label="Min Time")
    axs[1].plot(baseline_plotter.ts, baseline_plotter.e_norms, label="Standard")
    axs[1].legend()
    axs[1].set_title("Normalized Energy (E)")

    axs[2].plot(plotter.ts, plotter.us, label="Min Time")
    axs[2].plot(baseline_plotter.ts, baseline_plotter.us, label="Standard")
    axs[2].legend()
    axs[2].set_title("Control Signal (u)")

    for i in range(3):
        axs[i].set_xlabel("Time (s)")

    fig.suptitle(f"{plotter.name}")
    fig.savefig(SAVE_DIR / f"{plotter.filename}_plots.png")


    # n = 5
    w_0 = 1
    n = 5

    plotter = Plotter(name = "Min Time n=5")


    sim = MinTimeSimulator(
        name="Min Time n=5",
        w_0 = w_0,
        n = n,
        init_state = [theta_0, theta_dot_0],
        max_time=5,
        dt = dt
    )
    sim.run_simulation()

    sim_baseline = SinglePendulumSimulator(
        name="Baseline Single Swing Double Switch n=5",
        w_0 = w_0,
        n = n,
        init_state = [theta_0, theta_dot_0],
        k = 100,
        max_time=5,
        dt = dt
    )
    sim_baseline.run_simulation()

    # plot both
    plotter = sim.plotter
    baseline_plotter = sim_baseline.plotter

    fig, axs = plt.subplots(3, 1, figsize=(18, 18))

    axs[0].plot(plotter.ts, plotter.thetas, label="Min Time")
    axs[0].plot(baseline_plotter.ts, baseline_plotter.thetas, label="Standard")
    axs[0].set_title("Pendulum Angles (theta)")
    axs[0].legend()
    axs[0].set_ylabel("Angle (radians)")

    axs[1].plot(plotter.ts, plotter.e_norms, label="Min Time")
    axs[1].plot(baseline_plotter.ts, baseline_plotter.e_norms, label="Standard")
    axs[1].legend()
    axs[1].set_title("Normalized Energy (E)")

    axs[2].plot(plotter.ts, plotter.us, label="Min Time")
    axs[2].plot(baseline_plotter.ts, baseline_plotter.us, label="Standard")
    axs[2].legend()
    axs[2].set_title("Control Signal (u)")

    for i in range(3):
        axs[i].set_xlabel("Time (s)")

    fig.suptitle(f"{plotter.name}")
    fig.savefig(SAVE_DIR / f"{plotter.filename}_plots.png")

def twopend():
    w_01 = 1
    w_02 = 2
    n = 1.5
    k = 20

    plotter = TwoPendulumPlotter(name = "Two Pendulums n=1.5")

    # theta 1, theta 2
    state = [theta_0, theta_dot_0, theta_0, theta_dot_0]

    for t in np.arange(0, 10, dt):
        # compute E normalized from state
        E1 = (0.5/w_01**2) * state[1]**2 + math.cos(state[0]) - 1
        E2 = (0.5/w_02**2) * state[3]**2 + math.cos(state[2]) - 1

        G = E1 * state[1] * math.cos(state[0]) + E2 * state[3] * math.cos(state[2])

        # compute v = u/g (normalized u) from the state
        v = equation_19(
            k = k,
            G = G,
            ng = n
        )

        plotter.add_data(t, (state[0], state[2]), (E1, E2), v)

        # update state
        theta_dot_dot1 = w_01**2 * (math.sin(state[0]) - v * math.cos(state[0]))
        state[1] += theta_dot_dot1 * dt
        state[0] += state[1] * dt

        theta_dot_dot2 = w_02**2 * (math.sin(state[2]) - v * math.cos(state[2]))
        state[3] += theta_dot_dot2 * dt
        state[2] += state[3] * dt

    plotter.plot()

def main():
    print("ENPM667: Project 1")

    # SSDS
    ssds()

    # SSTSTriple Switch
    ssts()

    # Multi-swing
    multi()

    # Min-time
    bangbang()

    # two pendulums
    twopend()

if __name__ == "__main__":
    main()