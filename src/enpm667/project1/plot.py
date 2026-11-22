import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

THIS_DIR = Path(__file__).parent

SAVE_DIR = THIS_DIR.parent.parent.parent / "project1"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

class Plotter():

    def __init__(self, name: str) -> None:
        self.name = name
        self.filename = name.replace(" ", "_").replace("=", "_")

        self.num_points = 0
        self.ts = []
        self.thetas = []
        self.e_norms = []
        self.us = []

    def add_data(self, t: float, theta: float, e_norm: float, u: float) -> None:
        self.ts.append(t)
        self.thetas.append(theta)
        self.e_norms.append(e_norm)
        self.us.append(u)
        self.num_points += 1

    def plot(self) -> tuple:

        fig, axs = plt.subplots(3, 1, figsize=(18, 18))

        # plot thetas
        axs[0].plot(self.ts, self.thetas)
        axs[0].set_title("Pendulum Angle (theta)")
        axs[0].set_ylabel("Angle (radians)")

        # plot normalized energy
        axs[1].plot(self.ts, self.e_norms)
        axs[1].set_title("Normalized Energy (E)")
        # axs[0].set_ylabel("A")

        # plot control signal
        axs[2].plot(self.ts, self.us)
        axs[2].set_title("Control Signal (u)")
        # axs[2].set_ylabel("m/s^2")

        for i in range(3):
            axs[i].set_xlabel("Time (s)")

        fig.suptitle(f"{self.name}")
        fig.savefig(SAVE_DIR / f"{self.filename}_plots.png")

        return fig, axs

class TwoPendulumPlotter(Plotter):

    def __init__(self, name: str) -> None:
        self.name = name
        self.filename = name.replace(" ", "_").replace("=", "_")

        self.p1_plotter = Plotter("p1")
        self.p2_plotter = Plotter("p2")

    def add_data(self, t: float, theta: tuple, e_norm: tuple, u: float) -> None:
        self.p1_plotter.add_data(t, theta[0], e_norm[0], u)
        self.p2_plotter.add_data(t, theta[1], e_norm[1], u)

    def plot(self) -> None:
    
        fig, axs = plt.subplots(3, 1, figsize=(18, 18))

        # plot thetas
        axs[0].plot(self.p1_plotter.ts, self.p1_plotter.thetas, label="p1")
        axs[0].plot(self.p2_plotter.ts, self.p2_plotter.thetas, label="p2")
        axs[0].set_title("Pendulum Angles (theta)")
        axs[0].legend()
        axs[0].set_ylabel("Angle (radians)")

        # plot normalized energy
        axs[1].plot(self.p1_plotter.ts, self.p1_plotter.e_norms, label="p1")
        axs[1].plot(self.p2_plotter.ts, self.p2_plotter.e_norms, label="p2")
        axs[1].legend()
        axs[1].set_title("Normalized Energy (E)")
        # axs[0].set_ylabel("A")

        # plot control signal
        # same for both pendulums
        axs[2].plot(self.p1_plotter.ts, self.p1_plotter.us)
        axs[2].set_title("Control Signal (u)")

        for i in range(3):
            axs[i].set_xlabel("Time (s)")

        fig.suptitle(f"{self.name}")
        fig.savefig(SAVE_DIR / f"{self.filename}_plots.png")

