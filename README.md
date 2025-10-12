# 🔄 Iterator

A Python-based system that generates high-value website/app ideas and iteratively evolves them over time. Each run generates one new idea and iterates all existing ideas, creating a living portfolio of product concepts that continuously improve.

## 🎯 Features

- **Smart Idea Generation**: Creates one high-value, non-trivial idea per run
- **Continuous Iteration**: Evolves all existing ideas with each run
- **Dual-Mode Operation**: Works with OpenAI API or deterministic fallback
- **Cross-Platform**: Runs on GitHub Actions (scheduled/manual) and locally (including Replit)
- **Quality First**: Avoids low-value ideas (to-do lists, recipes, weather apps, generic CRUD)
- **Zero Dependencies**: Uses Python 3.11 stdlib only

## 🚀 Quick Start

### Local Usage

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd iterator
   ```

2. **Run the generator** (creates one new idea):
   ```bash
   python scripts/generate.py
   ```

3. **Run the iterator** (evolves all existing ideas):
   ```bash
   python scripts/iterate.py
   ```

4. **Optional: Set OpenAI API key** for AI-powered generation:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   python scripts/generate.py
   python scripts/iterate.py
   ```

### Replit Usage

1. Import this repository into Replit
2. Click the "Run" button (runs both generate and iterate)
3. Optional: Add `OPENAI_API_KEY` in Secrets (lock icon in sidebar)

The `.replit` file is configured to run both scripts automatically.

### GitHub Actions Usage

#### Automatic (Scheduled)
- Runs daily at 9 AM UTC automatically
- Generates one new idea and iterates all existing ones
- Commits results back to the repository

#### Manual Trigger
1. Go to "Actions" tab in your GitHub repository
2. Select "Iterator - Generate and Iterate Ideas"
3. Click "Run workflow"
4. Choose action:
   - `both` - Generate new idea AND iterate all ideas (default)
   - `generate` - Only generate one new idea
   - `iterate` - Only iterate existing ideas

#### Setup
1. Add `OPENAI_API_KEY` to repository secrets (optional):
   - Go to Settings → Secrets and variables → Actions
   - Add new secret named `OPENAI_API_KEY`
   - Without this, the system uses deterministic fallback

## 📁 Project Structure

```
iterator/
├── .github/
│   └── workflows/
│       └── iterator.yml          # GitHub Actions workflow
├── scripts/
│   ├── generate.py               # Generate one new idea
│   └── iterate.py                # Iterate all existing ideas
├── data/
│   └── ideas.json                # State file (auto-created)
├── .replit                       # Replit configuration
├── replit.nix                    # Replit dependencies
└── README.md                     # This file
```

## 💡 How It Works

### Generation (`generate.py`)
1. Checks for `OPENAI_API_KEY` environment variable
2. If present: Uses GPT-4 to generate a creative, high-value idea
3. If absent: Uses deterministic algorithm with curated templates
4. Focuses on valuable categories:
   - Developer Tools & Infrastructure
   - B2B SaaS & Productivity
   - Niche Marketplaces
   - AI & Machine Learning Platforms
   - Fintech & Business Solutions
5. Avoids low-value patterns (generic CRUD, to-do lists, etc.)
6. Saves idea with metadata to `data/ideas.json`

### Iteration (`iterate.py`)
1. Loads all existing ideas from state
2. For each idea, applies an evolution strategy:
   - Feature Expansion
   - Market Expansion
   - Technical Evolution
   - Business Model Innovation
   - User Experience Enhancement
   - Integration & Ecosystem
   - Data & Intelligence
   - Compliance & Security
3. Updates description and adds new features
4. Tracks complete history of all iterations
5. Saves updated state back to file

### State Management
All data is stored in `data/ideas.json`:
```json
{
  "ideas": [
    {
      "id": 1,
      "title": "Idea Title",
      "description": "Full description...",
      "category": "Developer Tools",
      "target_audience": "Enterprise teams",
      "key_features": ["Feature 1", "Feature 2"],
      "monetization": "Subscription-based...",
      "technical_approach": "Cloud-native...",
      "created_at": "2025-10-12T...",
      "updated_at": "2025-10-12T...",
      "iteration": 2,
      "history": [
        {
          "iteration": 0,
          "timestamp": "...",
          "iteration_type": "Feature Expansion",
          "changes_summary": "...",
          "rationale": "..."
        }
      ]
    }
  ],
  "metadata": {
    "created": "2025-10-12T...",
    "total_runs": 5,
    "total_iterations": 20,
    "last_generate": "2025-10-12T...",
    "last_iterate": "2025-10-12T..."
  }
}
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY` (optional): OpenAI API key for AI-powered generation
  - If not set, uses high-quality deterministic fallback
  - Recommended for maximum creativity and variety

### GitHub Actions Schedule
Edit `.github/workflows/iterator.yml` to change the schedule:
```yaml
schedule:
  - cron: '0 9 * * *'  # Daily at 9 AM UTC
```

Common cron patterns:
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 1` - Weekly on Mondays
- `0 0 1 * *` - Monthly on the 1st

## 📊 Deterministic Fallback

When `OPENAI_API_KEY` is not set, the system uses a sophisticated deterministic generator:

- **60+ curated templates** across 6 high-value categories
- **400+ variable combinations** for unique ideas
- **Deterministic seeding** based on run count for reproducibility
- **8 evolution strategies** for iterations
- **Quality-focused**: Only generates ideas worth building

The fallback ensures consistent, high-quality output without external dependencies.

## 🎨 Idea Categories

### Generated Ideas Focus On:
- **Developer Tools**: CI/CD, observability, code intelligence, API tools
- **SaaS & Productivity**: Vertical SaaS, workflow automation, analytics
- **Niche Marketplaces**: B2B platforms, specialized networks
- **Infrastructure & DevOps**: Cloud-native services, deployment tools
- **AI & Machine Learning**: ML platforms, AI assistants, data tools
- **Fintech & Business**: Payment systems, compliance, financial tools

### Explicitly Avoided:
- Generic CRUD applications
- To-do list variants
- Recipe or cooking sites
- Weather applications
- Simple content aggregators
- Basic blog platforms

## 🤝 Contributing

Feel free to:
- Add new idea templates to `IDEA_TEMPLATES`
- Expand `IDEA_VARIABLES` with more options
- Add iteration strategies to `ITERATION_STRATEGIES`
- Improve the OpenAI prompts
- Enhance the output formatting

## 📝 License

MIT License - feel free to use this for your own idea generation!

## 🔮 Example Output

```
=============================================================
ITERATOR - Generate New Idea
=============================================================

Current state: 3 existing ideas
Using deterministic generator...
✓ Generated idea using fallback generator

✓ Successfully generated idea #4

Title: An observability platform focused on
Category: Infrastructure & DevOps
Description: An observability platform focused on business impact for Kubernetes clusters that reduces complexity with edge computing.

Target Audience: Fast-growing startups
Monetization: Subscription-based pricing (Basic/Pro/Enterprise tiers)

Key Features:
  - Auto-scaling
  - Built-in monitoring
  - Infrastructure as Code

Technical Approach: Cloud-native architecture with microservices and event-driven design

State saved to: /path/to/data/ideas.json
=============================================================
```

## 🎯 Use Cases

- **Product Ideation**: Generate startup ideas for brainstorming
- **Portfolio Building**: Maintain a living portfolio of product concepts
- **Learning**: Study how ideas evolve and improve over iterations
- **Inspiration**: Use as creative prompts for actual projects
- **Teaching**: Demonstrate product thinking and iteration strategies

---

**Built with Python 3.11 | No external dependencies | Works everywhere**
