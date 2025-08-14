from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, FilePurpose
from dotenv import load_dotenv

load_dotenv()

project = AIProjectClient(
    endpoint="https://timothee-cronier-demo-resource.services.ai.azure.com/api/projects/timothee-cronier-demo",
    credential=DefaultAzureCredential(),
)
print("hey")

def list_agents():
    """
    List all agents in the project.
    """
    return project.agents.list_agents()