from database import SessionLocal
from models import Agent


db = SessionLocal()


agents = [
    Agent(
        name="Invoice Risk Analyzer",
        owner="Priya Sharma",
        risk="High",
        status="Production-ready",
        model="Llama-3-70B",
        cost="$8,420",
        run="Oct 01, 10:24 AM",
    ),
    Agent(
        name="Document Extractor",
        owner="Arjun Nair",
        risk="Medium",
        status="Running",
        model="Mixtral",
        cost="$5,210",
        run="Oct 01, 09:12 AM",
    ),
    Agent(
        name="CRM Enrichment Agent",
        owner="Karthik R",
        risk="Low",
        status="Ready",
        model="GPT-4.1",
        cost="$2,980",
        run="Sep 30, 06:41 PM",
    ),
    Agent(
        name="Dynamic Pricing Agent",
        owner="Neha Gupta",
        risk="High",
        status="Approval pending",
        model="Llama-3-70B",
        cost="$0",
        run="—",
    ),
    Agent(
        name="Customer Support Agent",
        owner="Rohit Mehta",
        risk="Medium",
        status="Ready",
        model="GPT-4.1",
        cost="$3,860",
        run="Oct 01, 08:15 AM",
    ),
]


db.add_all(agents)
db.commit()

print("5 agents added successfully!")

db.close()