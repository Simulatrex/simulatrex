"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: generative_audiences.py
Description: Defines the generative audience class for the simulation

"""

# from typing import List, Optional
# from simulatrex.agent import LLMAgent
# from simulatrex.agents.utils.spawn import spawn_agent
# from simulatrex.llms.utils.types import CognitiveModel
# from simulatrex.types import InitialConditions
# from simulatrex.llm_utils.models import OpenAILanguageModel


# class TargetAudienceRelationship:
#     def __init__(
#         self,
#         role_name: str,
#         type: str,
#         strength: float,
#     ):
#         self.role_name = role_name
#         self.type = type
#         self.strength = strength

#     def summary(self) -> str:
#         return f"{self.type.capitalize()} with {self.role_name} at a strength level of {self.strength}"


# class TargetAudience:
#     def __init__(
#         self,
#         id: str,
#         role: str,
#         responsibilities: str,
#         initial_conditions: Optional[InitialConditions] = None,
#         relationships: List[TargetAudienceRelationship] = [],
#     ):
#         self.id = id
#         self.role = role
#         self.responsibilities = responsibilities
#         self.initial_conditions = initial_conditions
#         self.agents = []
#         self.cognitive_model_id = "gpt-4-1106-preview"
#         self.relationships = relationships

#     async def spawn_agents(self, num_agents: int) -> List[LLMAgent]:
#         cognitive_model = OpenAILanguageModel(
#             model_id=CognitiveModel.GPT_4, agent_id=self.id
#         )
#         for _ in range(num_agents):
#             relationships_summary = "; ".join([r.summary() for r in self.relationships])
#             agent = await spawn_agent(
#                 cognitive_model,
#                 self.cognitive_model_id,
#                 self.role,
#                 self.responsibilities,
#                 relationships_summary,
#                 self.initial_conditions,
#             )
#             self.agents.append(agent)

#         return self.agents
