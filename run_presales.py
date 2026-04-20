"""
Pre-Sales AI Workflow — CLI entry point.

Runs the full three-phase pipeline (Research → Account Plan → Next Best Actions)
for a prospect company using Anthropic Claude Managed Agents.

Prerequisites:
    1. Set ANTHROPIC_API_KEY in .env (copy from .env.example)
    2. Run  python setup_agents.py  once to create the agents

Usage examples:
    # Minimal — just a company name
    python run_presales.py --company "Acme Corp"

    # Full context for richer output
    python run_presales.py \\
        --company "TechCorp Inc" \\
        --website "techcorp.io" \\
        --industry "FinTech" \\
        --contact "Jane Smith, CTO; Bob Lee, VP Engineering" \\
        --use-case "Replace legacy data pipeline with modern lakehouse" \\
        --context "Inbound from partner, urgent Q3 close target" \\
        --output outputs/techcorp_presales.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from presales.orchestrator import run_presales_workflow


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="run_presales",
        description="Pre-Sales AI Workflow powered by Anthropic Claude Managed Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--company",
        required=True,
        metavar="NAME",
        help="Prospect company name (required)",
    )
    p.add_argument(
        "--website",
        metavar="URL",
        help="Company website or LinkedIn URL",
    )
    p.add_argument(
        "--industry",
        metavar="VERTICAL",
        help="Industry / vertical (e.g. 'FinTech', 'Healthcare', 'E-commerce')",
    )
    p.add_argument(
        "--contact",
        metavar="CONTACTS",
        help=(
            "Known contact(s) at the company "
            "(e.g. 'Jane Smith, CTO; Bob Lee, VP Engineering')"
        ),
    )
    p.add_argument(
        "--use-case",
        metavar="TEXT",
        dest="use_case",
        help="Why you believe this prospect needs your solution",
    )
    p.add_argument(
        "--context",
        metavar="TEXT",
        help="Any additional deal context (deal source, partner intro, urgency, etc.)",
    )
    p.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Save full results to a JSON file (e.g. outputs/acme.json)",
    )
    p.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress real-time streaming output; only print a final summary",
    )
    return p


def main() -> int:
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print(
            "Error: ANTHROPIC_API_KEY is not set.\n"
            "Add it to a .env file (see .env.example) or export it directly.",
            file=sys.stderr,
        )
        return 1

    args = build_parser().parse_args()

    results = run_presales_workflow(
        company_name=args.company,
        company_website=args.website,
        contact_info=args.contact,
        industry=args.industry,
        use_case=args.use_case,
        additional_context=args.context,
        verbose=not args.quiet,
    )

    # ── Save to file ──────────────────────────────────────────────────────
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n✓  Full results saved → {out_path}")

    # ── Quiet-mode summary ────────────────────────────────────────────────
    if args.quiet:
        sep = "=" * 60
        print(f"\n{sep}")
        print(f"RESULTS SUMMARY  ·  {args.company}")
        print(sep)

        def _preview(text: str, chars: int = 400) -> str:
            return text[:chars].strip() + (" …" if len(text) > chars else "")

        print("\n── RESEARCH (preview) ──")
        print(_preview(results["research"]))

        print("\n── ACCOUNT PLAN (preview) ──")
        print(_preview(results["account_plan"]))

        print("\n── NEXT BEST ACTIONS (preview) ──")
        print(_preview(results["next_best_actions"]))

        if not args.output:
            print(
                "\nTip: run with  --output outputs/result.json  to save the full report."
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
