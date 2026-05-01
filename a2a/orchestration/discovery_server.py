"""
Agent Card Discovery Server.

Serves the /.well-known/agent-cards endpoint so the presales agent
and other org agents can discover each other's capabilities via A2A.

Run with: uvicorn discovery_server:app --host 0.0.0.0 --port 8080
"""

import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

app = FastAPI(
    title="CC Sales Agent Card Discovery",
    description="A2A agent card discovery endpoint for CC Sales presales agents",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://agents.your-company.com"],
    allow_methods=["GET"],
    allow_headers=["Authorization"],
)

# Paths relative to repo root
REPO_ROOT = Path(__file__).parent.parent.parent
A2A_DIR = REPO_ROOT / "a2a"
AGENTS_DIR = A2A_DIR / "agents"
PRESALES_CARD = A2A_DIR / "agent-card.json"


def _load_all_cards() -> dict[str, dict]:
    """Load all agent cards from the agents/ directory + presales agent card."""
    cards: dict[str, dict] = {}

    # Load presales agent's own card
    if PRESALES_CARD.exists():
        with open(PRESALES_CARD) as f:
            card = json.load(f)
            cards[card["agent"]["id"]] = card

    # Load all org agent cards
    if AGENTS_DIR.exists():
        for card_file in AGENTS_DIR.glob("*-card.json"):
            with open(card_file) as f:
                card = json.load(f)
                agent_id = card["agent"]["id"]
                cards[agent_id] = card
                logger.debug("Loaded agent card: %s", agent_id)

    return cards


@app.get("/.well-known/agent-cards", response_class=JSONResponse)
async def list_agent_cards():
    """Returns all registered agent cards as a list."""
    cards = _load_all_cards()
    return list(cards.values())


@app.get("/.well-known/agent-cards/{agent_id}", response_class=JSONResponse)
async def get_agent_card(agent_id: str):
    """Returns the card for a specific agent by ID."""
    cards = _load_all_cards()
    if agent_id not in cards:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_id}' not registered. Available: {list(cards.keys())}",
        )
    return cards[agent_id]


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    cards = _load_all_cards()
    return {
        "status": "healthy",
        "registered_agents": list(cards.keys()),
        "agent_count": len(cards),
    }
