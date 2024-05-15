"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: agent_group.py
Description: AgentGroup class for the simulation

"""

from typing import List, Optional

from simulatrex.agents.generative_agent import GenerativeAgent
from simulatrex.base import Base


class AgentGroup(Base, list):
    def __init__(self, agents: Optional[List[GenerativeAgent]] = None):
        super().__init__()
        if agents is not None:
            self.extend(agents)

    def to_dict(self) -> dict:
        return {"agent_group": [agent.to_dict() for agent in self]}

    @classmethod
    def from_dict(cls, data: dict) -> "AgentGroup":
        agent_data = data.get("agent_group", [])
        agents = [GenerativeAgent.from_dict(agent_dict) for agent_dict in agent_data]
        return cls(agents)
