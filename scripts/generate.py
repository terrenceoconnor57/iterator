#!/usr/bin/env python3
"""
Generate one high-value website/app idea and add it to the state.
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

# High-value idea templates (deterministic fallback)
IDEA_TEMPLATES = [
    {
        "category": "Developer Tools",
        "templates": [
            "A platform that automatically {action} for {audience} by analyzing {data_source}",
            "An AI-powered tool that helps developers {solve_problem} by {method}",
            "A collaborative workspace for {team_type} to {accomplish_task} in real-time",
            "A code intelligence platform that {analyzes} and provides {insights}",
            "An API monitoring service that {tracks} and {optimizes} for better performance"
        ]
    },
    {
        "category": "SaaS & Productivity",
        "templates": [
            "An intelligent automation platform for {industry} that {streamlines_process}",
            "A vertical SaaS for {niche_market} professionals to {manage_workflow}",
            "A data analytics dashboard that {aggregates} and {visualizes} for {decision_makers}",
            "A workflow orchestration tool that {coordinates} across {systems}",
            "An AI copilot for {profession} that {assists_with} using {technology}"
        ]
    },
    {
        "category": "Niche Marketplaces",
        "templates": [
            "A marketplace connecting {provider_type} with {consumer_type} for {specific_need}",
            "A B2B platform where {sellers} can {transact} with {buyers} in the {industry} space",
            "A curated network of {specialist_type} offering {premium_service}",
            "A peer-to-peer platform for {asset_type} sharing in {geographic_niche}",
            "An enterprise marketplace for {resource_type} with built-in {value_add}"
        ]
    },
    {
        "category": "Infrastructure & DevOps",
        "templates": [
            "A cloud-native {service_type} that {solves_problem} with {unique_approach}",
            "An observability platform focused on {specific_metric} for {tech_stack}",
            "A deployment automation tool that {simplifies} for {target_audience}",
            "A security scanning service that detects {threat_type} and prevents {risk_type} in {environment}",
            "An infrastructure-as-code solution that {enables} through {innovation}"
        ]
    },
    {
        "category": "AI & Machine Learning",
        "templates": [
            "An ML model marketplace for {use_case} with {differentiator}",
            "An AI training platform optimized for {model_type} on {data_type}",
            "A no-code ML tool that lets {users} build {applications} without {expertise}",
            "An AI-powered {domain} assistant that {capability} using {technique}",
            "A synthetic data generation platform for {industry} compliance and {purpose}"
        ]
    },
    {
        "category": "Fintech & Business",
        "templates": [
            "A payment infrastructure for {market_segment} with {innovative_feature}",
            "An automated {financial_process} platform for {business_type}",
            "A compliance-as-a-service tool for {regulation} in {industry}",
            "An embedded finance solution that {enables} for {platform_type}",
            "A treasury management system for {company_size} with {ai_capability}"
        ]
    }
]

IDEA_VARIABLES = {
    "action": ["optimizes performance", "detects vulnerabilities", "refactors legacy code", "generates documentation", "manages dependencies"],
    "audience": ["enterprise teams", "open-source maintainers", "startup founders", "scaling companies", "remote teams"],
    "data_source": ["GitHub repositories", "production logs", "API traffic", "user behavior patterns", "infrastructure metrics"],
    "solve_problem": ["reduce technical debt", "prevent security breaches", "optimize cloud costs", "improve code quality", "accelerate deployments"],
    "method": ["ML-powered suggestions", "static analysis", "runtime profiling", "collaborative reviews", "automated testing"],
    "team_type": ["distributed engineering", "product", "security", "DevOps", "data science"],
    "accomplish_task": ["debug complex systems", "architect scalable solutions", "manage incidents", "plan sprints", "review pull requests"],
    "analyzes": ["dependency chains", "performance bottlenecks", "security surfaces", "code complexity", "API contracts"],
    "insights": ["actionable recommendations", "cost-saving opportunities", "risk assessments", "optimization strategies", "best practices"],
    "tracks": ["SLA compliance", "error rates", "latency patterns", "resource utilization", "API health"],
    "optimizes": ["caching strategies", "query performance", "network routing", "resource allocation", "load balancing"],
    "threat_type": ["zero-day vulnerabilities", "misconfigurations", "compliance violations", "performance regressions", "anomalous behavior"],
    "risk_type": ["data breaches", "service outages", "cost overruns", "regulatory penalties", "security incidents"],
    "industry": ["healthcare", "fintech", "logistics", "manufacturing", "real estate"],
    "streamlines_process": ["reduces manual work by 80%", "automates compliance reporting", "integrates disparate systems", "eliminates data silos", "accelerates time-to-market"],
    "niche_market": ["construction", "legal", "dental", "HVAC", "property management"],
    "manage_workflow": ["schedule jobs efficiently", "track project milestones", "manage client relationships", "optimize resource allocation", "automate billing"],
    "aggregates": ["multi-source data", "cross-platform metrics", "customer feedback", "market signals", "operational KPIs"],
    "visualizes": ["trends and anomalies", "predictive insights", "real-time dashboards", "custom reports", "executive summaries"],
    "decision_makers": ["C-suite executives", "product managers", "operations teams", "growth marketers", "investment committees"],
    "coordinates": ["microservices", "third-party APIs", "data pipelines", "human approvals", "cross-team processes"],
    "systems": ["legacy and modern infrastructure", "cloud and on-premise", "internal and external tools", "automated and manual workflows", "structured and unstructured data"],
    "profession": ["sales teams", "customer success", "recruiters", "compliance officers", "financial analysts"],
    "assists_with": ["lead qualification", "customer onboarding", "candidate screening", "risk assessment", "financial modeling"],
    "technology": ["natural language processing", "predictive analytics", "computer vision", "reinforcement learning", "knowledge graphs"],
    "provider_type": ["vetted specialists", "certified professionals", "local experts", "freelance consultants", "verified vendors"],
    "consumer_type": ["enterprise buyers", "SMB owners", "project managers", "procurement teams", "individual clients"],
    "specific_need": ["emergency services", "specialized expertise", "project-based work", "ongoing maintenance", "strategic consulting"],
    "sellers": ["manufacturers", "distributors", "service providers", "software vendors", "equipment suppliers"],
    "transact": ["negotiate contracts", "procure materials", "license software", "outsource services", "lease equipment"],
    "buyers": ["procurement departments", "operations managers", "IT directors", "facility managers", "supply chain teams"],
    "specialist_type": ["domain experts", "fractional executives", "technical architects", "industry consultants", "transformation leaders"],
    "premium_service": ["strategic advisory", "hands-on implementation", "custom integrations", "white-glove support", "outcome-based projects"],
    "asset_type": ["industrial equipment", "specialized software", "computing resources", "professional expertise", "intellectual property"],
    "geographic_niche": ["urban markets", "emerging regions", "enterprise campuses", "remote locations", "cross-border corridors"],
    "resource_type": ["cloud compute", "specialized talent", "proprietary data", "licensed content", "managed services"],
    "value_add": ["instant provisioning", "usage-based pricing", "compliance certification", "24/7 support", "SLA guarantees"],
    "service_type": ["observability platform", "data pipeline", "API gateway", "secret management", "backup solution"],
    "solves_problem": ["reduces complexity", "improves reliability", "cuts operational costs", "accelerates development", "enhances security"],
    "unique_approach": ["edge computing", "serverless architecture", "zero-trust security", "GitOps workflows", "AI-driven automation"],
    "specific_metric": ["business impact", "user experience", "cost efficiency", "security posture", "environmental sustainability"],
    "tech_stack": ["Kubernetes clusters", "serverless functions", "microservices", "monolithic applications", "edge networks"],
    "simplifies": ["multi-cloud deployments", "blue-green releases", "rollback procedures", "environment provisioning", "configuration management"],
    "target_audience": ["platform teams", "DevOps engineers", "SREs", "cloud architects", "security teams"],
    "environment": ["cloud workloads", "container images", "CI/CD pipelines", "production systems", "supply chains"],
    "enables": ["self-service infrastructure", "policy-as-code", "automated governance", "cost attribution", "disaster recovery"],
    "innovation": ["natural language interfaces", "visual programming", "AI-assisted generation", "drift detection", "predictive scaling"],
    "use_case": ["fraud detection", "personalization", "forecasting", "recommendation", "anomaly detection"],
    "differentiator": ["explainability", "low-latency inference", "domain-specific fine-tuning", "continuous learning", "regulatory compliance"],
    "model_type": ["large language models", "computer vision", "time series", "reinforcement learning", "graph neural networks"],
    "data_type": ["multimodal data", "streaming data", "sensitive data", "edge data", "synthetic data"],
    "users": ["business analysts", "domain experts", "product teams", "researchers", "entrepreneurs"],
    "applications": ["predictive models", "intelligent automation", "custom classifiers", "recommendation engines", "chatbots"],
    "expertise": ["coding skills", "ML knowledge", "data science degree", "cloud infrastructure", "mathematical background"],
    "domain": ["legal research", "medical diagnosis", "code review", "content creation", "design"],
    "capability": ["analyzes documents", "generates insights", "provides recommendations", "automates workflows", "answers queries"],
    "technique": ["retrieval-augmented generation", "few-shot learning", "fine-tuned models", "multi-agent systems", "knowledge graphs"],
    "purpose": ["model training", "testing", "privacy preservation", "bias mitigation", "scenario simulation"],
    "market_segment": ["gig economy", "cross-border commerce", "subscription businesses", "enterprise procurement", "creator economy"],
    "innovative_feature": ["instant settlement", "embedded banking", "crypto rails", "dynamic routing", "fraud prevention AI"],
    "financial_process": ["accounts payable", "revenue recognition", "expense management", "cash flow forecasting", "financial close"],
    "business_type": ["mid-market companies", "fast-growing startups", "enterprise subsidiaries", "franchise networks", "holding companies"],
    "regulation": ["SOC 2", "GDPR", "HIPAA", "PCI-DSS", "SOX"],
    "platform_type": ["marketplaces", "SaaS products", "e-commerce platforms", "vertical software", "B2B networks"],
    "company_size": ["venture-backed startups", "mid-market firms", "multinational corporations", "private equity portfolios", "public companies"],
    "ai_capability": ["cash position optimization", "automated reconciliation", "fraud detection", "predictive analytics", "risk scoring"]
}


def load_state() -> Dict:
    """Load the current state from JSON file."""
    DATA_DIR.mkdir(exist_ok=True)
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"ideas": [], "metadata": {"created": datetime.now().isoformat(), "total_runs": 0}}


def save_state(state: Dict) -> None:
    """Save the state to JSON file."""
    DATA_DIR.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def generate_with_openai(api_key: str) -> Dict:
    """Generate a high-value idea using OpenAI API."""
    prompt = """Generate ONE innovative, high-value website or application idea that:
- Solves a real, specific problem for a defined audience
- Has clear monetization potential
- Is technically feasible but non-trivial
- Avoids generic concepts (no to-do lists, recipe sites, weather apps, basic CRUD apps)
- Focuses on B2B SaaS, developer tools, niche marketplaces, fintech, AI/ML platforms, or infrastructure

Respond with a JSON object containing:
{
  "title": "Concise, descriptive title",
  "description": "2-3 sentences explaining the idea, target market, and value proposition",
  "category": "The category (e.g., Developer Tools, SaaS, Fintech, etc.)",
  "target_audience": "Who would use this",
  "key_features": ["feature1", "feature2", "feature3"],
  "monetization": "How it makes money",
  "technical_approach": "Brief technical overview"
}"""

    try:
        data = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an expert product strategist and startup advisor who generates innovative, high-value product ideas."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
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
            idea = json.loads(content)
            return idea

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


def generate_fallback_idea(run_count: int) -> Dict:
    """Generate a high-quality idea using deterministic fallback."""
    # Use run count as seed for deterministic but varied results
    seed = f"idea_gen_{run_count}"
    
    # Select category
    category_data = deterministic_choice(seed + "_category", IDEA_TEMPLATES)
    category = category_data["category"]
    
    # Select template
    template = deterministic_choice(seed + "_template", category_data["templates"])
    
    # Fill in template with deterministic choices
    filled_template = template
    placeholders = []
    import re
    for match in re.finditer(r'\{(\w+)\}', template):
        placeholders.append(match.group(1))
    
    for i, placeholder in enumerate(placeholders):
        if placeholder in IDEA_VARIABLES:
            choice = deterministic_choice(f"{seed}_{i}_{placeholder}", IDEA_VARIABLES[placeholder])
            filled_template = filled_template.replace(f"{{{placeholder}}}", choice, 1)
    
    # Generate additional fields
    description = filled_template
    
    # Create title from description (use key words, 6-10 words max)
    words = [w.strip('.,;:()') for w in description.split() if w.strip('.,;:()')]
    # Skip common starting articles and take meaningful words
    start_idx = 0
    if words and words[0].lower() in ['a', 'an', 'the']:
        start_idx = 1
    title_words = words[start_idx:min(start_idx + 10, len(words))]
    # Capitalize important words (title case)
    title = " ".join(word.capitalize() if word.lower() not in ['a', 'an', 'the', 'for', 'in', 'on', 'at', 'to', 'by', 'with', 'and', 'or', 'that', 'of'] 
                     else word.lower() 
                     for word in title_words)
    # Ensure first word is capitalized
    if title:
        title = title[0].upper() + title[1:]
    
    # Generate features based on category
    feature_templates = {
        "Developer Tools": ["Intelligent code analysis", "Real-time collaboration", "CI/CD integration", "Custom reporting dashboards", "API-first architecture"],
        "SaaS & Productivity": ["Automated workflows", "Advanced analytics", "Third-party integrations", "Role-based access control", "Mobile-first design"],
        "Niche Marketplaces": ["Verified user profiles", "Escrow payment system", "Rating and review system", "Advanced search and filters", "Transaction dispute resolution"],
        "Infrastructure & DevOps": ["Auto-scaling", "Multi-cloud support", "Built-in monitoring", "Zero-downtime deployments", "Infrastructure as Code"],
        "AI & Machine Learning": ["Pre-trained models", "Custom training pipelines", "Real-time inference", "Model versioning", "Explainability tools"],
        "Fintech & Business": ["Bank-level security", "Automated reconciliation", "Multi-currency support", "Compliance reporting", "RESTful API access"]
    }
    
    features = []
    base_features = feature_templates.get(category, ["Advanced features", "User-friendly interface", "Scalable architecture"])
    i = 0
    while len(features) < 3 and i < 10:  # Max 10 attempts to avoid infinite loop
        feature = deterministic_choice(f"{seed}_feature_{i}", base_features)
        if feature not in features:
            features.append(feature)
        i += 1
    
    # Generate monetization
    monetization_options = [
        "Subscription-based pricing (Basic/Pro/Enterprise tiers)",
        "Usage-based pricing with free tier",
        "Transaction fees on platform activity",
        "Freemium model with paid advanced features",
        "Enterprise licensing with custom SLAs",
        "Per-seat pricing for team accounts"
    ]
    monetization = deterministic_choice(f"{seed}_monetization", monetization_options)
    
    # Generate target audience
    audience_options = [
        "Enterprise development teams",
        "Fast-growing startups",
        "SMB owners and operators",
        "DevOps and platform engineers",
        "Product and engineering leaders",
        "Industry-specific professionals"
    ]
    target_audience = deterministic_choice(f"{seed}_audience", audience_options)
    
    # Generate technical approach
    tech_options = [
        "Cloud-native architecture with microservices and event-driven design",
        "Serverless backend with GraphQL API and React frontend",
        "Kubernetes-based platform with distributed data processing",
        "AI/ML pipeline using modern transformer models and vector databases",
        "Real-time collaboration using WebSockets and CRDTs",
        "Multi-tenant SaaS with PostgreSQL and Redis caching"
    ]
    technical_approach = deterministic_choice(f"{seed}_tech", tech_options)
    
    return {
        "title": title,
        "description": description,
        "category": category,
        "target_audience": target_audience,
        "key_features": features,
        "monetization": monetization,
        "technical_approach": technical_approach
    }


def generate_idea(state: Dict) -> Dict:
    """Generate a new idea using OpenAI or fallback."""
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if api_key:
        print("Using OpenAI API to generate idea...")
        try:
            idea_content = generate_with_openai(api_key)
            print("✓ Generated idea using OpenAI")
        except Exception as e:
            print(f"OpenAI API failed, falling back to deterministic generator: {e}")
            idea_content = generate_fallback_idea(state["metadata"]["total_runs"])
    else:
        print("No OPENAI_API_KEY found, using deterministic generator...")
        idea_content = generate_fallback_idea(state["metadata"]["total_runs"])
        print("✓ Generated idea using fallback generator")
    
    # Create full idea object
    idea_id = len(state["ideas"]) + 1
    idea = {
        "id": idea_id,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "iteration": 0,
        **idea_content,
        "history": []
    }
    
    return idea


def main():
    """Main function to generate and save a new idea."""
    print("=" * 60)
    print("ITERATOR - Generate New Idea")
    print("=" * 60)
    
    # Load current state
    state = load_state()
    print(f"\nCurrent state: {len(state['ideas'])} existing ideas")
    
    # Generate new idea
    new_idea = generate_idea(state)
    
    # Add to state
    state["ideas"].append(new_idea)
    state["metadata"]["total_runs"] += 1
    state["metadata"]["last_generate"] = datetime.now().isoformat()
    
    # Save state
    save_state(state)
    
    print(f"\n✓ Successfully generated idea #{new_idea['id']}")
    print(f"\nTitle: {new_idea['title']}")
    print(f"Category: {new_idea['category']}")
    print(f"Description: {new_idea['description']}")
    print(f"\nTarget Audience: {new_idea['target_audience']}")
    print(f"Monetization: {new_idea['monetization']}")
    print(f"\nKey Features:")
    for feature in new_idea['key_features']:
        print(f"  - {feature}")
    print(f"\nTechnical Approach: {new_idea['technical_approach']}")
    print(f"\nState saved to: {STATE_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()

