from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import Base, engine, SessionLocal
from models import Agent

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Allow the React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5174",
    "https://governed-ai-accelerator-react.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data required to create an agent
class AgentCreate(BaseModel):
    name: str
    owner: str
    risk: str
    status: str
    model: str
    cost: str
    run: str | None = None


# Health check
@app.get("/")
def home():
    return {
        "message": "Governed AI Accelerator backend is running!"
    }


# Get all agents
@app.get("/api/agents")
def get_agents():
    db = SessionLocal()

    agents = db.query(Agent).all()

    result = []

    for agent in agents:
        result.append({
            "id": agent.id,
            "name": agent.name,
            "owner": agent.owner,
            "risk": agent.risk,
            "status": agent.status,
            "model": agent.model,
            "cost": agent.cost,
            "run": agent.run,
        })

    db.close()

    return {
        "agents": result
    }


# Register a new agent
@app.post("/api/agents")
def create_agent(agent_data: AgentCreate):
    db = SessionLocal()

    new_agent = Agent(
        name=agent_data.name,
        owner=agent_data.owner,
        risk=agent_data.risk,
        status=agent_data.status,
        model=agent_data.model,
        cost=agent_data.cost,
        run=agent_data.run,
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    result = {
        "id": new_agent.id,
        "name": new_agent.name,
        "owner": new_agent.owner,
        "risk": new_agent.risk,
        "status": new_agent.status,
        "model": new_agent.model,
        "cost": new_agent.cost,
        "run": new_agent.run,
    }

    db.close()

    return result


# Delete an agent
@app.delete("/api/agents/{agent_id}")
def delete_agent(agent_id: int):
    db = SessionLocal()

    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if agent is None:
        db.close()
        return {
            "message": "Agent not found"
        }

    db.delete(agent)
    db.commit()
    db.close()

    return {
        "message": f"Agent {agent_id} deleted successfully"
    }

# edit an agent
@app.put("/api/agents/{agent_id}")
def update_agent(agent_id: int, agent_data: AgentCreate):
    db = SessionLocal()

    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if agent is None:
        db.close()
        return {
            "message": "Agent not found"
        }

    agent.name = agent_data.name
    agent.owner = agent_data.owner
    agent.risk = agent_data.risk
    agent.status = agent_data.status
    agent.model = agent_data.model
    agent.cost = agent_data.cost
    agent.run = agent_data.run

    db.commit()
    db.refresh(agent)

    result = {
        "id": agent.id,
        "name": agent.name,
        "owner": agent.owner,
        "risk": agent.risk,
        "status": agent.status,
        "model": agent.model,
        "cost": agent.cost,
        "run": agent.run,
    }

    db.close()

    return result