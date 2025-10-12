# 🔄 Iterator

A Python-based system that generates high-value website/app ideas and **automatically creates working code** for each one. Each run generates one new idea and builds/iterates actual Replit-ready applications for all existing ideas.

## 🎯 What It Does

1. **`generate.py`** - Generates ONE new high-value product idea
2. **`iterate.py`** - **Builds working code** for EVERY idea in your portfolio

Each idea becomes a real, runnable web application with:
- ✅ Complete source code
- ✅ Working UI
- ✅ API endpoints
- ✅ Replit configuration
- ✅ README documentation

## 🚀 Quick Start

### Local Usage

1. **Generate a new idea**:
   ```bash
   python3 scripts/generate.py
   ```

2. **Build code for all ideas**:
   ```bash
   python3 scripts/iterate.py
   ```
   
   This creates working applications in `projects/idea-{id}-{name}/`

3. **Run a generated project**:
   ```bash
   cd projects/idea-1-*/
   python3 main.py
   # Visit http://localhost:8080
   ```

4. **Optional: Use OpenAI for smarter generation**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   python3 scripts/generate.py
   python3 scripts/iterate.py
   ```

### Replit Usage

1. Import this repository into Replit
2. Click "Run" → generates idea + builds all projects
3. Navigate to `projects/` folder to see generated apps
4. Each project has its own `.replit` file - open and run independently
5. Optional: Add `OPENAI_API_KEY` in Secrets for AI-powered generation

### GitHub Actions Usage

#### Automatic (Scheduled)
- Runs daily at 9 AM UTC
- Generates one new idea
- Builds/updates code for all ideas
- Commits everything back to the repository

#### Manual Trigger
1. Go to "Actions" tab
2. Select "Iterator - Generate and Iterate Ideas"
3. Click "Run workflow"
4. Choose action:
   - `both` - Generate new idea AND build all projects (default)
   - `generate` - Only generate one new idea
   - `iterate` - Only build code for existing ideas

## 📁 Project Structure

```
iterator/
├── .github/workflows/
│   └── iterator.yml              # GitHub Actions workflow
├── scripts/
│   ├── generate.py               # Generate 1 new idea
│   └── iterate.py                # Build code for all ideas
├── projects/                     # 🆕 Generated applications live here!
│   ├── idea-1-{name}/
│   │   ├── main.py              # Working Python web app
│   │   ├── index.html           # Beautiful UI
│   │   ├── .replit              # Replit config
│   │   ├── replit.nix           # Dependencies
│   │   └── README.md            # Project docs
│   ├── idea-2-{name}/
│   └── ...
├── data/
│   └── ideas.json                # State file with all ideas
├── .replit                       # Main iterator config
├── replit.nix                    # Python 3.11 setup
└── README.md                     # This file
```

## 💡 How It Works

### Generation Phase (`generate.py`)

1. Creates ONE high-value, non-trivial product idea
2. Uses GPT-4o-mini if `OPENAI_API_KEY` is set
3. Falls back to sophisticated deterministic generator
4. Focuses on valuable categories:
   - Developer Tools & Infrastructure
   - B2B SaaS & Productivity
   - Niche Marketplaces
   - AI & Machine Learning
   - Fintech & Business
5. Avoids low-value ideas (CRUD apps, to-do lists, recipes, weather)
6. Saves to `data/ideas.json`

### Code Generation Phase (`iterate.py`)

1. **Scans** all existing ideas from `data/ideas.json`
2. For each idea:
   - Checks if project already exists
   - **Generates complete working code**:
     - Python web server (Flask-style or http.server)
     - Beautiful, modern HTML/CSS UI
     - API endpoints with JSON responses
     - Interactive JavaScript frontend
   - Creates Replit configuration (`.replit`, `replit.nix`)
   - Writes comprehensive README
3. Uses **OpenAI GPT-4o-mini** if API key is available (more creative)
4. Uses **smart templates** as fallback (still high quality)
5. Each project is immediately runnable in Replit or locally

### Template System (No API Key Required)

When `OPENAI_API_KEY` is not set, uses category-specific templates:

- **Developer Tools** → Code analysis/scanning web apps
- **SaaS & Productivity** → Dashboard applications
- **Infrastructure & DevOps** → API monitoring services
- **Niche Marketplaces** → Two-sided marketplace UIs
- **Fintech & Business** → Analytics dashboards

All templates include:
- Modern, gradient-based UI design
- Responsive layout
- Interactive features
- API endpoints
- Real-time updates

## 🎨 Generated Application Features

Each generated app includes:

### Frontend
- ✨ Modern, beautiful UI with gradients
- 📱 Responsive design
- ⚡ Interactive elements
- 🎯 Category-specific functionality

### Backend
- 🐍 Python 3.11 (stdlib only)
- 🌐 HTTP server with API endpoints
- 📊 JSON API responses
- 🔄 Real-time data updates

### Configuration
- `.replit` - One-click run in Replit
- `replit.nix` - Python 3.11 dependencies
- `README.md` - Complete documentation
- Executable Python files

## 📊 State Management

All data stored in `data/ideas.json`:

```json
{
  "ideas": [
    {
      "id": 1,
      "title": "Security Scanning Service...",
      "description": "...",
      "category": "Infrastructure & DevOps",
      "target_audience": "Fast-growing startups",
      "key_features": ["Feature 1", "Feature 2"],
      "monetization": "Freemium model...",
      "technical_approach": "Multi-tenant SaaS...",
      "created_at": "2025-10-12T...",
      "updated_at": "2025-10-12T...",
      "iteration": 2,
      "project_path": "projects/idea-1-security-scanning-...",
      "history": [
        {
          "iteration": 1,
          "timestamp": "...",
          "description": "Code generated",
          "files_created": 5,
          "next_steps": ["Add authentication", "..."]
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

- `OPENAI_API_KEY` (optional)
  - If set: Uses GPT-4o-mini for creative idea generation and code
  - If not set: Uses high-quality deterministic templates
  - Recommended for maximum variety and sophistication

### GitHub Actions Schedule

Edit `.github/workflows/iterator.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Daily at 9 AM UTC
```

Change to:
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 1` - Weekly on Mondays
- `0 0 1 * *` - Monthly on the 1st

## 🎯 Example Workflow

```bash
# Day 1: Generate first idea
$ python3 scripts/generate.py
✓ Generated idea #1: "Security Scanning Service..."

# Build the code
$ python3 scripts/iterate.py
✓ Generated 3 files for idea-1

# Run the app
$ cd projects/idea-1-security-scanning-service-*/
$ python3 main.py
🚀 Server running at http://localhost:8080

# Day 2: Add another idea
$ python3 scripts/generate.py
✓ Generated idea #2: "AI-Powered Code Review Platform"

# Update all projects
$ python3 scripts/iterate.py
[1/2] Updating: Security Scanning Service
  ✓ Generated 3 files
[2/2] Building: AI-Powered Code Review Platform
  ✓ Generated 3 files
```

## 📦 No External Dependencies

- ✅ Python 3.11 standard library only
- ✅ Uses: `json`, `os`, `sys`, `hashlib`, `datetime`, `pathlib`, `typing`, `urllib`, `re`
- ✅ Generated apps also use stdlib only
- ✅ Fully portable and self-contained

## 🎨 Idea Quality

### What Gets Generated ✅
- Developer tools (CI/CD, monitoring, security)
- B2B SaaS platforms
- Vertical SaaS for specific industries
- Niche marketplaces
- Fintech applications
- AI/ML platforms
- Infrastructure tools

### What's Explicitly Avoided ❌
- Generic CRUD apps
- To-do lists and task managers
- Recipe websites
- Weather applications
- Basic blog platforms
- Generic content aggregators

## 🚀 Use Cases

1. **Portfolio Building** - Generate a portfolio of working projects
2. **Learning** - Study different application architectures
3. **Rapid Prototyping** - Get MVPs in seconds
4. **Idea Exploration** - See ideas come to life immediately
5. **Teaching** - Demonstrate full-stack development
6. **Hackathons** - Quick project scaffolding

## 🔮 Example Generated Apps

### Developer Tool
```
🚀 Security Scanning Service
📡 Upload configs/code → Get analysis
✨ Beautiful gradient UI
🔍 REST API endpoints
```

### SaaS Dashboard
```
📊 Analytics Dashboard
📈 Real-time stats
💼 Multi-tenant ready
🎨 Modern card-based UI
```

## 🤝 How AI Helps (Optional)

With `OPENAI_API_KEY` set:

**Idea Generation:**
- More creative, unique concepts
- Better descriptions
- Varied technical approaches

**Code Generation:**
- More sophisticated implementations
- Better code organization
- Contextual improvements on iteration

Without API key:
- Still generates high-quality ideas
- Template-based code (proven patterns)
- Consistent, reliable output

## 📝 License

MIT License - Build amazing things! 🚀

---

**Built with Python 3.11 | No external dependencies | Creates real, working apps**
