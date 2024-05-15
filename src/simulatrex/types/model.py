"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: model.py
Description: Types for the LLMs

"""

from enum import Enum
from simulatrex.llms.utils.memory import LongTermMemory, ShortTermMemory


class LanguageModelId(Enum):
    GPT_4_TURBO = "gpt-4-0125-preview"
    GPT_4 = "gpt-4"
    GPT_3_5_Turbo = "gpt-3.5-turbo"
    LLAMA_2_70B_CHAT_HF = "llama-2-70b-chat-hf"
    LLAMA_2_13B_CHAT_HF = "llama-2-13b-chat-hf"
    MISTRAL_7B_CHAT_HF = "mistral-7b-chat-hf"
    MIXTRAL_8x7B_INSTRUCT = "mixtral-8x7B-instruct-v0.1"


class AgentType(Enum):
    LLMAgent = "LLM_AGENT"


class AgentMemory:
    def __init__(self, id: str, decay_factor: int) -> None:
        self.decay_factor = decay_factor
        self.short_term_memory = ShortTermMemory(id, decay_factor)
        self.long_term_memory = LongTermMemory(id)
