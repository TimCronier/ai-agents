import os, asyncio
from functools import cache
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AgentGroupChat, AzureAIAgent
from .strategies import RouterSelectionStrategy, CycleTermination, ROUTER
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
# IDs stockés dans .env (placé à la racine du projet)
ROUTER_ID  = os.getenv("AGENT_ID_ROUTER")   
BUDGET_ID  = os.getenv("AGENT_ID_BUDGET")   
INVEST_ID  = os.getenv("AGENT_ID_INVEST")   
TAX_ID     = os.getenv("AGENT_ID_TAX")      

###############################################################################
# 1) Client Azure : singleton
###############################################################################
@cache
async def get_client():
    creds = DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True,
    )
    cm = AzureAIAgent.create_client(credential=creds)
    client = await cm.__aenter__()
    return client, cm          # retourne le context-manager pour le shutdown

###############################################################################
# 2) GroupChat partagé : singleton aussi
###############################################################################
_chat_lock = asyncio.Lock()
_chat: AgentGroupChat | None = None

async def get_shared_group_chat() -> AgentGroupChat:
    global _chat
    if _chat:
        return _chat

    async with _chat_lock:
        if _chat:                # double-check après l’attente
            return _chat

        client, _ = await get_client()

        # Récupération des définitions
        router_def = await client.agents.get_agent(agent_id=ROUTER_ID)
        budget_def = await client.agents.get_agent(agent_id=BUDGET_ID)
        invest_def = await client.agents.get_agent(agent_id=INVEST_ID)
        tax_def    = await client.agents.get_agent(agent_id=TAX_ID)

        # Wrappers
        router = AzureAIAgent(client=client, definition=router_def)
        budget = AzureAIAgent(client=client, definition=budget_def)
        invest = AzureAIAgent(client=client, definition=invest_def)
        tax    = AzureAIAgent(client=client, definition=tax_def)

        _chat = AgentGroupChat(
            agents=[router, budget, invest, tax],
            selection_strategy=RouterSelectionStrategy(router_name=ROUTER),
            termination_strategy=CycleTermination(
                agents=[], maximum_iterations=30, automatic_reset=True
            ),
        )
    return _chat