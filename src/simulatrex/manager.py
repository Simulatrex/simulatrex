from contextlib import asynccontextmanager
from .simulation import Simulation


@asynccontextmanager
async def simulation_context(identifier, agents=None, environment=None):
    simulation = Simulation(identifier, agents, environment)
    try:
        print(f"Starting simulation {identifier}")
        yield simulation
    finally:
        print(f"Ending simulation {identifier}")
