"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: simulation.py
Description: Simulation class for the simulation

"""

import logging

from simulatrex.agents.generative_agent import GenerativeAgent
from simulatrex.environment import Environment


class Simulation:
    def __init__(
        self,
        identifier: str,
        epochs: int = 1,
        interactions: list[str] = None,
        agents: list[GenerativeAgent] = [],
        environment: Environment = None,
        logger: logging.Logger = None,
    ):
        self.identifier = identifier
        self.epochs = epochs
        self.interactions = interactions if interactions is not None else []

        self._agents = agents if agents is not None else []
        self._environment = environment
        self._logger = (
            logger if logger is not None else logging.getLogger("simulation_logger")
        )

    @property
    def agents(self):
        return self._agents

    @agents.setter
    def agents(self, value):
        self._agents = value

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        self._environment = value

    async def run(self):
        self._logger.info(f"Simulation {self.identifier} started.")
        for _ in range(self.epochs):
            if self.environment:
                await self.environment.interact(self.agents)
            for interaction in self.interactions:
                self._logger.info(f"Executing interaction: {interaction}")
        self._logger.info(f"Simulation {self.identifier} ended.")

    def to_dict(self):
        return {
            "id": self.identifier,
            "epochs": self.epochs,
            "interactions": self.interactions,
        }
