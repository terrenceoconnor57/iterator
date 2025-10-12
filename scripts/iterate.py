#!/usr/bin/env python3
"""
Iterate all existing ideas - evolve, improve, and refine them.
Uses OpenAI API if OPENAI_API_KEY is available, otherwise uses deterministic fallback.
"""

import json
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import urllib.request
import urllib.error

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
STATE_FILE = DATA_DIR / "ideas.json"

# Iteration strategies (deterministic fallback)
ITERATION_STRATEGIES = [
    {
        "name": "Feature Expansion",
        "description": "Add a complementary feature set that extends the core value proposition",
        "examples": [
            "AI-powered analytics and insights",
            "Advanced automation capabilities",
            "Mobile and offline support",
            "Enterprise SSO and security features",
            "Marketplace or ecosystem integrations",
            "White-label and reseller options",
            "Advanced reporting and dashboards",
            "Workflow customization engine",
            "API and webhook platform",
            "Real-time collaboration tools"
        ]
    },
    {
        "name": "Market Expansion",
        "description": "Identify an adjacent market or use case that could benefit from the product",
        "examples": [
            "Expand from SMB to enterprise segment",
            "Launch vertical-specific version for {industry}",
            "Add international support and localization",
            "Create lighter version for individual users",
            "Partner with larger platforms for distribution",
            "Introduce freemium tier to accelerate adoption",
            "Target different department (from IT to Product)",
            "Expand from web to mobile-native experience",
            "Add cross-industry capabilities",
            "Launch partner program for resellers"
        ]
    },
    {
        "name": "Technical Evolution",
        "description": "Improve the technical architecture or implementation approach",
        "examples": [
            "Migrate to edge computing for better latency",
            "Add real-time processing and streaming",
            "Implement advanced caching and optimization",
            "Build native mobile apps with offline-first design",
            "Add blockchain for transparency and trust",
            "Integrate vector databases for semantic search",
            "Implement federated learning for privacy",
            "Add GraphQL API alongside REST",
            "Build plugin architecture for extensibility",
            "Introduce infrastructure automation"
        ]
    },
    {
        "name": "Business Model Innovation",
        "description": "Evolve the monetization or go-to-market strategy",
        "examples": [
            "Add usage-based pricing tier",
            "Introduce marketplace transaction fees",
            "Launch premium support packages",
            "Create certification and training programs",
            "Add professional services offering",
            "Implement revenue sharing with partners",
            "Launch managed service tier",
            "Add white-label licensing option",
            "Introduce outcome-based pricing",
            "Create platform fee for third-party apps"
        ]
    },
    {
        "name": "User Experience Enhancement",
        "description": "Significantly improve the user experience or interface",
        "examples": [
            "Add AI assistant for natural language interactions",
            "Implement smart recommendations and personalization",
            "Create guided onboarding and tutorials",
            "Build visual workflow designer (no-code)",
            "Add customizable templates and presets",
            "Implement predictive suggestions",
            "Create command palette for power users",
            "Add accessibility features (WCAG AAA)",
            "Implement progressive disclosure for complexity",
            "Build interactive data visualizations"
        ]
    },
    {
        "name": "Integration & Ecosystem",
        "description": "Expand integrations and ecosystem partnerships",
        "examples": [
            "Build native integrations with top 10 platforms",
            "Launch app marketplace for third-party extensions",
            "Add Zapier/Make integration support",
            "Integrate with major cloud providers",
            "Build Slack/Teams/Discord bots",
            "Add calendar and scheduling integrations",
            "Integrate with CRM and marketing tools",
            "Support data warehouse connectors",
            "Add GitHub/GitLab/Bitbucket apps",
            "Create browser extensions"
        ]
    },
    {
        "name": "Data & Intelligence",
        "description": "Leverage data and AI to add intelligence layer",
        "examples": [
            "Add predictive analytics and forecasting",
            "Implement anomaly detection and alerting",
            "Build recommendation engine",
            "Add natural language processing for insights",
            "Create automated report generation",
            "Implement intelligent automation triggers",
            "Add benchmarking against industry data",
            "Build custom ML model training",
            "Implement sentiment analysis",
            "Add pattern recognition and insights"
        ]
    },
    {
        "name": "Compliance & Security",
        "description": "Enhance security, privacy, and compliance features",
        "examples": [
            "Achieve SOC 2 Type II certification",
            "Add GDPR compliance tools and data portability",
            "Implement end-to-end encryption",
            "Add audit logging and compliance reporting",
            "Build advanced permission management",
            "Implement data residency options",
            "Add HIPAA compliance for healthcare",
            "Build zero-knowledge architecture",
            "Implement advanced threat detection",
            "Add SAML and advanced auth options"
        ]
    }
]


def load_state() -> Dict:
    """Load the current state from JSON file."""
    if not STATE_FILE.exists():
        print("Error: No ideas found. Run generate.py first.", file=sys.stderr)
        sys.exit(1)
    
    with open(STATE_FILE, 'r') as f:
        return json.load(f)


def save_state(state: Dict) -> None:
    """Save the state to JSON file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def iterate_with_openai(idea: Dict, api_key: str) -> Dict:
    """Iterate an idea using OpenAI API."""
    prompt = f"""You are helping evolve and improve a product idea through iteration. Here's the current idea:

Title: {idea['title']}
Description: {idea['description']}
Category: {idea['category']}
Current Iteration: {idea['iteration']}

Target Audience: {idea['target_audience']}
Key Features: {', '.join(idea['key_features'])}
Monetization: {idea['monetization']}
Technical Approach: {idea['technical_approach']}

Generate the NEXT iteration of this idea by:
1. Identifying a specific way to evolve, expand, or improve it
2. Keeping the core concept but making it more valuable, feasible, or differentiated
3. Being specific and actionable (not generic)

Respond with a JSON object containing:
{{
  "iteration_type": "What kind of iteration (e.g., Feature Expansion, Market Expansion, etc.)",
  "changes_summary": "Brief summary of what's changing",
  "updated_description": "Updated 2-3 sentence description incorporating the changes",
  "new_features": ["Any new features being added"],
  "rationale": "Why this iteration makes the product more valuable"
}}"""

    try:
        data = json.dumps({
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are an expert product strategist who helps evolve product ideas through thoughtful iteration."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "response_format": {"type": "json_object"}
        }).encode('utf-8')

        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            iteration_data = json.loads(content)
            return iteration_data

    except urllib.error.HTTPError as e:
        print(f"OpenAI API error: {e.code} - {e.read().decode('utf-8')}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        raise


def deterministic_choice(seed: str, options: List) -> any:
    """Make a deterministic choice based on a seed."""
    hash_val = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    return options[hash_val % len(options)]


def iterate_fallback(idea: Dict) -> Dict:
    """Iterate an idea using deterministic fallback."""
    # Use idea ID and iteration number as seed
    seed = f"iterate_{idea['id']}_{idea['iteration']}"
    
    # Select iteration strategy
    strategy = deterministic_choice(seed + "_strategy", ITERATION_STRATEGIES)
    iteration_type = strategy["name"]
    
    # Select specific change from strategy examples
    change = deterministic_choice(seed + "_change", strategy["examples"])
    
    # Generate changes summary
    changes_summary = f"{iteration_type}: {change}"
    
    # Update description with the iteration
    updated_description = f"{idea['description']} In this iteration, we're implementing {change.lower()} to {strategy['description'].lower()}."
    
    # Generate new features based on the strategy
    new_features = []
    feature_count = deterministic_choice(seed + "_count", [1, 2, 2, 3])  # Weighted towards 2
    
    feature_pool = {
        "Feature Expansion": [
            "Advanced AI-powered insights and recommendations",
            "Automated workflow orchestration",
            "Real-time collaboration and team features",
            "Custom reporting and analytics dashboards",
            "Mobile app with offline capabilities"
        ],
        "Market Expansion": [
            "Multi-language and localization support",
            "Industry-specific templates and workflows",
            "Enterprise-grade security and compliance",
            "Self-service onboarding and tutorials",
            "Partner and reseller portal"
        ],
        "Technical Evolution": [
            "Edge computing for reduced latency",
            "Advanced caching and performance optimization",
            "Blockchain-based audit trail",
            "GraphQL API with real-time subscriptions",
            "Plugin architecture for extensibility"
        ],
        "Business Model Innovation": [
            "Usage-based pricing model",
            "Professional services and consulting",
            "Premium support with SLA guarantees",
            "White-label and reseller options",
            "Revenue sharing partner program"
        ],
        "User Experience Enhancement": [
            "AI assistant with natural language interface",
            "Visual workflow designer (no-code/low-code)",
            "Smart templates and presets",
            "Personalized recommendations engine",
            "Command palette for power users"
        ],
        "Integration & Ecosystem": [
            "Native integrations with top platforms",
            "Third-party app marketplace",
            "Zapier and Make.com connectors",
            "Slack and Microsoft Teams bots",
            "Browser extension and bookmarklet"
        ],
        "Data & Intelligence": [
            "Predictive analytics and forecasting",
            "Automated anomaly detection and alerts",
            "Custom ML model training",
            "Industry benchmarking and insights",
            "Natural language report generation"
        ],
        "Compliance & Security": [
            "SOC 2 Type II certification",
            "End-to-end encryption at rest and in transit",
            "Advanced audit logging and compliance reports",
            "GDPR and CCPA data tools",
            "Role-based access control (RBAC)"
        ]
    }
    
    available_features = feature_pool.get(iteration_type, feature_pool["Feature Expansion"])
    for i in range(feature_count):
        new_feature = deterministic_choice(f"{seed}_newfeature_{i}", available_features)
        if new_feature not in new_features:
            new_features.append(new_feature)
    
    # Generate rationale
    rationale_options = [
        f"This iteration expands the value proposition by {change.lower()}, opening up new revenue opportunities and increasing customer lifetime value.",
        f"By {change.lower()}, we address a key market need and differentiate from competitors, leading to higher conversion and retention.",
        f"This evolution enhances the core offering through {change.lower()}, making the product more indispensable to our target users.",
        f"Implementing {change.lower()} reduces friction in adoption and positions us for scale in the next phase of growth.",
        f"This strategic iteration leverages {change.lower()} to create a more defensible market position and sustainable competitive advantage."
    ]
    rationale = deterministic_choice(seed + "_rationale", rationale_options)
    
    return {
        "iteration_type": iteration_type,
        "changes_summary": changes_summary,
        "updated_description": updated_description,
        "new_features": new_features,
        "rationale": rationale
    }


def iterate_idea(idea: Dict, api_key: str = None) -> Dict:
    """Iterate a single idea."""
    if api_key:
        try:
            iteration_data = iterate_with_openai(idea, api_key)
            print(f"  ✓ Iterated using OpenAI")
        except Exception as e:
            print(f"  ! OpenAI failed, using fallback: {e}")
            iteration_data = iterate_fallback(idea)
    else:
        iteration_data = iterate_fallback(idea)
        print(f"  ✓ Iterated using fallback")
    
    # Create history entry for current state before updating
    history_entry = {
        "iteration": idea["iteration"],
        "timestamp": idea["updated_at"],
        "description": idea["description"],
        "key_features": idea["key_features"]
    }
    
    # Update idea with iteration
    idea["iteration"] += 1
    idea["updated_at"] = datetime.now().isoformat()
    idea["description"] = iteration_data["updated_description"]
    
    # Add new features to existing features
    for new_feature in iteration_data["new_features"]:
        if new_feature not in idea["key_features"]:
            idea["key_features"].append(new_feature)
    
    # Add to history with iteration details
    history_entry["iteration_type"] = iteration_data["iteration_type"]
    history_entry["changes_summary"] = iteration_data["changes_summary"]
    history_entry["rationale"] = iteration_data["rationale"]
    
    idea["history"].append(history_entry)
    
    return iteration_data


def main():
    """Main function to iterate all ideas."""
    print("=" * 60)
    print("ITERATOR - Iterate All Ideas")
    print("=" * 60)
    
    # Load current state
    state = load_state()
    
    if not state["ideas"]:
        print("\nNo ideas to iterate. Run generate.py first.")
        return
    
    print(f"\nFound {len(state['ideas'])} ideas to iterate")
    
    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print("Using OpenAI API for iterations...")
    else:
        print("No OPENAI_API_KEY found, using deterministic generator...")
    
    print()
    
    # Iterate each idea
    for idx, idea in enumerate(state["ideas"], 1):
        print(f"[{idx}/{len(state['ideas'])}] Iterating: {idea['title']}")
        print(f"  Current iteration: {idea['iteration']}")
        
        iteration_data = iterate_idea(idea, api_key)
        
        print(f"  → {iteration_data['iteration_type']}")
        print(f"  → {iteration_data['changes_summary']}")
        print()
    
    # Update metadata
    state["metadata"]["last_iterate"] = datetime.now().isoformat()
    if "total_iterations" not in state["metadata"]:
        state["metadata"]["total_iterations"] = 0
    state["metadata"]["total_iterations"] += len(state["ideas"])
    
    # Save state
    save_state(state)
    
    print("=" * 60)
    print(f"✓ Successfully iterated {len(state['ideas'])} ideas")
    print(f"State saved to: {STATE_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()

