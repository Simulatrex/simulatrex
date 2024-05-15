"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: environment.py
Description: Environment class for the simulation

"""

import logging

from simulatrex.agents.generative_agent import GenerativeAgent


class Environment:
    def __init__(
        self,
        identifier: str,
        entities: list[str] = None,
        logger=logging.getLogger("simulation_logger"),
    ):
        self.identifier = identifier
        self.entities = entities if entities is not None else []

        self._logger = logger

    async def interact(self, agents: list[GenerativeAgent]):
        self._logger.info(
            f"Environment {self.identifier} is facilitating interaction among agents."
        )
        for agent in agents:
            await agent.act()

    def to_dict(self):
        return {"id": self.identifier, "entities": self.entities}
