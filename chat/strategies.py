from typing import ClassVar, Set
from semantic_kernel.agents.strategies import (
    SequentialSelectionStrategy,
    TerminationStrategy,
)
from semantic_kernel.contents.utils.author_role import AuthorRole
from pydantic import Field

ROUTER = "ROUTER"
BUDGETING_ADVISOR = "BUDGETING_ADVISOR"
INVESTMENT_ADVISOR = "INVESTMENT_ADVISOR"
TAX_ADVISOR = "TAX_ADVISOR"
EXPERTS = {BUDGETING_ADVISOR, INVESTMENT_ADVISOR, TAX_ADVISOR}


class RouterSelectionStrategy(SequentialSelectionStrategy):
    router_name: str = Field(default=ROUTER, exclude=True)

    async def select_agent(self, agents, history):
        last = history[-1]
        if last.role == AuthorRole.USER:                        # A
            return next(a for a in agents if a.name == self.router_name)
        if last.name == self.router_name:                       # B
            expert_name = last.content.strip()
            return next((a for a in agents if a.name == expert_name),
                        next(a for a in agents if a.name == self.router_name))
        if last.name in EXPERTS:                                # C
            return next(a for a in agents if a.name == self.router_name)
        return next(a for a in agents if a.name == self.router_name)  # Fallback


class CycleTermination(TerminationStrategy):
    stop_words: ClassVar[Set[str]] = {"stop", "merci", "thank you"}

    async def should_agent_terminate(self, agent, history):
        last = history[-1]
        if last.role == AuthorRole.USER and last.content.lower().strip() in self.stop_words:
            return True
        if last.name in EXPERTS:
            return True
        return False
