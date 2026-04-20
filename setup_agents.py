"""
One-time setup script — creates the three pre-sales Claude Managed Agents
and a shared cloud environment, then saves their IDs to config/agents.json.

Run ONCE before using run_presales.py:
    python setup_agents.py

To update an existing agent's configuration, run again and choose to update.
Agent IDs are stable; only a new version is created on update.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from presales.prompts import (
    NBA_AGENT_DESCRIPTION,
    NBA_AGENT_NAME,
    NBA_AGENT_SYSTEM,
    PLANNING_AGENT_DESCRIPTION,
    PLANNING_AGENT_NAME,
    PLANNING_AGENT_SYSTEM,
    RESEARCH_AGENT_DESCRIPTION,
    RESEARCH_AGENT_NAME,
    RESEARCH_AGENT_SYSTEM,
)

load_dotenv()

CONFIG_PATH = Path("config/agents.json")

# All three agents need web access and full file/bash tools for research tasks.
AGENT_TOOLSET = [
    {
        "type": "agent_toolset_20260401",
        "default_config": {"enabled": True},
    }
]


def _print_header(title: str) -> None:
    bar = "=" * 60
    print(f"\n{bar}\n{title}\n{bar}")


def _print_step(n: int, total: int, label: str) -> None:
    print(f"\n[{n}/{total}] {label}...", flush=True)


def _save_config(config: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(f"\n✓  Config saved → {CONFIG_PATH}")


def create_agents(client: anthropic.Anthropic) -> dict:
    """Create all agents and the shared environment from scratch."""
    config: dict = {}

    _print_header("CREATING PRE-SALES AI AGENTS")

    # ── Environment ───────────────────────────────────────────────────────
    _print_step(1, 4, "Creating cloud environment (unrestricted networking for web research)")
    env_name = f"presales-env-{int(time.time())}"
    environment = client.beta.environments.create(
        name=env_name,
        config={
            "type": "cloud",
            # Unrestricted so agents can web_search and web_fetch any domain.
            "networking": {"type": "unrestricted"},
        },
    )
    config["environment_id"] = environment.id
    print(f"   ✓  Environment: {environment.id}  (name: {env_name})")

    # ── Research Agent ────────────────────────────────────────────────────
    _print_step(2, 4, f"Creating {RESEARCH_AGENT_NAME}")
    research_agent = client.beta.agents.create(
        name=RESEARCH_AGENT_NAME,
        description=RESEARCH_AGENT_DESCRIPTION,
        model="claude-opus-4-6",
        system=RESEARCH_AGENT_SYSTEM,
        tools=AGENT_TOOLSET,
    )
    config.setdefault("agents", {})["research"] = {
        "id": research_agent.id,
        "version": research_agent.version,
        "name": RESEARCH_AGENT_NAME,
    }
    print(f"   ✓  {RESEARCH_AGENT_NAME}: {research_agent.id}  (v{research_agent.version})")

    # ── Planning Agent ────────────────────────────────────────────────────
    _print_step(3, 4, f"Creating {PLANNING_AGENT_NAME}")
    planning_agent = client.beta.agents.create(
        name=PLANNING_AGENT_NAME,
        description=PLANNING_AGENT_DESCRIPTION,
        model="claude-opus-4-6",
        system=PLANNING_AGENT_SYSTEM,
        tools=AGENT_TOOLSET,
    )
    config["agents"]["planning"] = {
        "id": planning_agent.id,
        "version": planning_agent.version,
        "name": PLANNING_AGENT_NAME,
    }
    print(f"   ✓  {PLANNING_AGENT_NAME}: {planning_agent.id}  (v{planning_agent.version})")

    # ── NBA Agent ─────────────────────────────────────────────────────────
    _print_step(4, 4, f"Creating {NBA_AGENT_NAME}")
    nba_agent = client.beta.agents.create(
        name=NBA_AGENT_NAME,
        description=NBA_AGENT_DESCRIPTION,
        model="claude-opus-4-6",
        system=NBA_AGENT_SYSTEM,
        tools=AGENT_TOOLSET,
    )
    config["agents"]["nba"] = {
        "id": nba_agent.id,
        "version": nba_agent.version,
        "name": NBA_AGENT_NAME,
    }
    print(f"   ✓  {NBA_AGENT_NAME}: {nba_agent.id}  (v{nba_agent.version})")

    return config


def update_agents(client: anthropic.Anthropic, existing: dict) -> dict:
    """
    Update existing agents with the latest system prompts.
    Creates a new version for each agent; existing sessions keep their pinned version.
    """
    _print_header("UPDATING PRE-SALES AI AGENTS")
    config = dict(existing)

    agent_defs = [
        ("research", RESEARCH_AGENT_NAME, RESEARCH_AGENT_DESCRIPTION, RESEARCH_AGENT_SYSTEM),
        ("planning", PLANNING_AGENT_NAME, PLANNING_AGENT_DESCRIPTION, PLANNING_AGENT_SYSTEM),
        ("nba", NBA_AGENT_NAME, NBA_AGENT_DESCRIPTION, NBA_AGENT_SYSTEM),
    ]

    for i, (key, name, description, system) in enumerate(agent_defs, 1):
        agent_id = existing["agents"][key]["id"]
        _print_step(i, len(agent_defs), f"Updating {name} ({agent_id})")
        updated = client.beta.agents.update(
            agent_id,
            name=name,
            description=description,
            model="claude-opus-4-6",
            system=system,
            tools=AGENT_TOOLSET,
        )
        config["agents"][key]["version"] = updated.version
        print(f"   ✓  New version: {updated.version}")

    return config


def main() -> int:
    client = anthropic.Anthropic()

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            existing = json.load(f)

        print("\nExisting configuration found:")
        print(f"  Environment : {existing.get('environment_id')}")
        for key, info in existing.get("agents", {}).items():
            print(f"  {info['name']}: {info['id']} (v{info['version']})")

        print("\nOptions:")
        print("  1 — Use existing config (no changes)")
        print("  2 — Update agent system prompts (new version, same IDs)")
        print("  3 — Create brand-new agents and environment")
        choice = input("\nChoice [1]: ").strip() or "1"

        if choice == "1":
            print("\nUsing existing configuration — nothing changed.")
            return 0
        elif choice == "2":
            config = update_agents(client, existing)
        elif choice == "3":
            config = create_agents(client)
        else:
            print("Invalid choice.")
            return 1
    else:
        config = create_agents(client)

    _save_config(config)

    _print_header("SETUP COMPLETE")
    print(
        f"""
  Environment : {config['environment_id']}
  Research    : {config['agents']['research']['id']}
  Planning    : {config['agents']['planning']['id']}
  NBA         : {config['agents']['nba']['id']}

Run the workflow:
  python run_presales.py --company "Acme Corp" --website "acme.com"
"""
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
