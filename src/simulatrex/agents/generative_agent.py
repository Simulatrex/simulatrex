"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: generative_agent.py
Description: Generative Agent class for the simulation

"""

from __future__ import annotations
import copy
import logging
from typing import Union

from simulatrex.associative_memory import associate_memory
from simulatrex.llms.models import OpenAILanguageModel
from simulatrex.types.agent import ActionSpec, AgentResponse

from simulatrex.base import Base
from simulatrex.experiments.questions.question import Question
from simulatrex.types.model import LanguageModelId
from simulatrex.utils.errors import AgentCombinationError


class GenerativeAgent(Base):
    """An agent represents a human in the simulation."""

    default_instruction = """Respond to each question by fully assuming a human persona. Maintain this character consistently and without deviation."""

    attributes = {}
    rules = {}
    instructions = {}

    def __init__(
        self,
        identifier: str,
        attributes: dict = None,
        instructions: str = None,
        llm_model_id: LanguageModelId = LanguageModelId.GPT_4_TURBO,
        user_controlled: bool = False,
        logger=logging.getLogger("simulation_logger"),
        verbose: bool = False,
    ):
        self.identifier = identifier
        self.attributes = attributes or dict()
        self.instructions = instructions or self.default_instruction

        self._llm = OpenAILanguageModel(llm_model_id) if llm_model_id else None
        self._user_controlled = user_controlled
        self._logger = logger
        self._verbose = verbose

    @property
    def id(self) -> str:
        return self.identifier

    def copy(self) -> GenerativeAgent:
        """Creates a copy of the agent."""
        return copy.deepcopy(self)

    async def act(self, actions: ActionSpec) -> AgentResponse:
        """Generates a response to a question."""
        if self._llm:
            for action in actions:
                response = await self._llm.ask(f"Generate an action for: {action}.")
                self._logger.info(
                    f"Agent {self.identifier} action for {action}: {response}"
                )
        else:
            raise ValueError(f"Agent {self.identifier} has no LLM to generate action.")

    def to_dict(self) -> dict[str, Union[dict, bool]]:
        """Serializes to a dictionary."""
        return {
            "identifier": self.identifier,
            "attributes": self.attributes,
            "instructions": self.instructions,
            "llm_model_id": self._llm.model_id,
            "user_controlled": self._user_controlled,
            "verbose": self._verbose,
        }

    @classmethod
    def from_dict(cls, agent_dict: dict[str, Union[dict, bool]]) -> GenerativeAgent:
        """Deserializes from a dictionary."""
        return cls(**agent_dict)
