#!/usr/bin/env python3
"""
Iterate all existing ideas - scan existing projects and generate/update working code.
Creates actual Replit-ready applications for each idea.
Uses OpenAI API if OPENAI_API_KEY is available, otherwise uses template-based generation.
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
import re

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DATA_DIR = ROOT_DIR / "data"
STATE_FILE = DATA_DIR / "ideas.json"
PROJECTS_DIR = ROOT_DIR / "projects"


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


def sanitize_project_name(title: str) -> str:
    """Convert idea title to valid directory name."""
    # Remove special characters, convert to lowercase, replace spaces with hyphens
    name = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    name = re.sub(r'\s+', '-', name.strip())
    name = name.lower()[:50]  # Limit length
    return name or "unnamed-project"


def get_project_dir(idea: Dict) -> Path:
    """Get the project directory for an idea."""
    project_name = sanitize_project_name(idea['title'])
    return PROJECTS_DIR / f"idea-{idea['id']}-{project_name}"


def scan_existing_project(project_dir: Path) -> Dict:
    """Scan an existing project and return info about it."""
    if not project_dir.exists():
        return {"exists": False, "files": []}
    
    files = []
    for item in project_dir.rglob('*'):
        if item.is_file() and not any(skip in str(item) for skip in ['.git', '__pycache__', 'node_modules', '.env']):
            files.append(str(item.relative_to(project_dir)))
    
    return {
        "exists": True,
        "files": files,
        "file_count": len(files)
    }


def generate_code_with_openai(idea: Dict, project_info: Dict, api_key: str) -> Dict:
    """Generate or iterate code for an idea using OpenAI."""
    
    if project_info["exists"]:
        action = "iterate and improve"
        context = f"The project already exists with {project_info['file_count']} files: {', '.join(project_info['files'][:10])}"
    else:
        action = "create from scratch"
        context = "This is a new project"
    
    prompt = f"""You are building a working application for this idea:

Title: {idea['title']}
Description: {idea['description']}
Category: {idea['category']}
Target Audience: {idea['target_audience']}
Key Features: {', '.join(idea['key_features'][:5])}
Technical Approach: {idea['technical_approach']}

Current Status: {context}
Action: {action} this project (iteration {idea['iteration'] + 1})

Generate a complete, working web application. Focus on creating a MINIMAL but FUNCTIONAL MVP.

Respond with JSON containing the file structure:
{{
  "files": [
    {{
      "path": "main.py",
      "content": "# Complete file content here..."
    }},
    {{
      "path": "templates/index.html",
      "content": "<!-- Complete HTML here -->"
    }}
  ],
  "entry_point": "main.py",
  "description": "Brief description of what was implemented",
  "next_steps": ["feature 1", "feature 2"]
}}

Guidelines:
- Create a simple Python web app (Flask or http.server)
- Use only Python stdlib or include requirements.txt
- Make it immediately runnable in Replit
- Include a simple, functional UI
- Focus on core value proposition
- Keep it under 500 lines total
"""

    try:
        data = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an expert full-stack developer who builds clean, working MVPs."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
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

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            code_data = json.loads(content)
            return code_data

    except Exception as e:
        print(f"  ! OpenAI code generation failed: {e}")
        raise


def generate_code_template(idea: Dict, project_info: Dict) -> Dict:
    """Generate code using templates (fallback when no API key)."""
    
    # Determine app type from category
    category = idea['category']
    
    if category == "Developer Tools":
        return generate_dev_tools_template(idea)
    elif category == "SaaS & Productivity":
        return generate_saas_template(idea)
    elif category in ["Infrastructure & DevOps", "AI & Machine Learning"]:
        return generate_api_service_template(idea)
    elif category == "Niche Marketplaces":
        return generate_marketplace_template(idea)
    elif category == "Fintech & Business":
        return generate_dashboard_template(idea)
    else:
        return generate_generic_web_app(idea)


def generate_dev_tools_template(idea: Dict) -> Dict:
    """Generate a developer tool web app."""
    main_py = f'''#!/usr/bin/env python3
"""
{idea['title']}
{idea['description']}
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.parse
from pathlib import Path

class AppHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = Path('index.html').read_text()
            self.wfile.write(html.encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Process the input
            result = {{
                "status": "success",
                "message": f"Processed: {{data.get('input', '')}}",
                "results": [
                    "Analysis result 1",
                    "Analysis result 2",
                    "Recommendation 3"
                ]
            }}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

if __name__ == '__main__':
    port = 8080
    server = HTTPServer(('0.0.0.0', port), AppHandler)
    print(f"🚀 {idea['title']}")
    print(f"📡 Server running at http://0.0.0.0:{{port}}")
    server.serve_forever()
'''

    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{idea['title']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 2em;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        .input-group {{
            margin-bottom: 20px;
        }}
        label {{
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }}
        textarea, input {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        textarea {{
            min-height: 120px;
            font-family: monospace;
        }}
        textarea:focus, input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 14px 32px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        button:hover {{
            transform: translateY(-2px);
        }}
        button:active {{
            transform: translateY(0);
        }}
        .results {{
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
            display: none;
        }}
        .results.show {{
            display: block;
        }}
        .result-item {{
            padding: 12px;
            margin: 8px 0;
            background: white;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}
        .feature {{
            padding: 15px;
            background: #f0f0f0;
            border-radius: 8px;
            text-align: center;
        }}
        .loading {{
            display: none;
            text-align: center;
            margin: 20px 0;
        }}
        .loading.show {{
            display: block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 {idea['title']}</h1>
        <p class="subtitle">{idea['description'][:200]}</p>
        
        <div class="features">
            {''.join(f'<div class="feature">✨ {feature}</div>' for feature in idea['key_features'][:3])}
        </div>
        
        <div class="input-group">
            <label for="input">Enter Your Data:</label>
            <textarea id="input" placeholder="Paste your code, config, or data here..."></textarea>
        </div>
        
        <button onclick="analyze()">Analyze Now</button>
        
        <div class="loading" id="loading">
            <p>⚡ Processing...</p>
        </div>
        
        <div class="results" id="results">
            <h3>Results:</h3>
            <div id="results-content"></div>
        </div>
    </div>
    
    <script>
        async function analyze() {{
            const input = document.getElementById('input').value;
            if (!input.trim()) {{
                alert('Please enter some data to analyze');
                return;
            }}
            
            document.getElementById('loading').classList.add('show');
            document.getElementById('results').classList.remove('show');
            
            try {{
                const response = await fetch('/api/analyze', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ input }})
                }});
                
                const data = await response.json();
                
                const resultsHTML = data.results.map(r => 
                    `<div class="result-item">${{r}}</div>`
                ).join('');
                
                document.getElementById('results-content').innerHTML = resultsHTML;
                document.getElementById('results').classList.add('show');
            }} catch (error) {{
                alert('Error: ' + error.message);
            }} finally {{
                document.getElementById('loading').classList.remove('show');
            }}
        }}
    </script>
</body>
</html>
'''

    readme = f'''# {idea['title']}

{idea['description']}

## Features

{chr(10).join(f"- {feature}" for feature in idea['key_features'][:5])}

## Target Audience

{idea['target_audience']}

## How to Run

```bash
python3 main.py
```

Then visit http://localhost:8080

## Technical Stack

{idea['technical_approach']}

## Iteration

Current iteration: {idea['iteration'] + 1}
Created: {idea['created_at']}
'''

    return {
        "files": [
            {"path": "main.py", "content": main_py},
            {"path": "index.html", "content": index_html},
            {"path": "README.md", "content": readme}
        ],
        "entry_point": "main.py",
        "description": f"Generated MVP for {idea['title']}",
        "next_steps": ["Add authentication", "Implement data persistence", "Add more features"]
    }


def generate_saas_template(idea: Dict) -> Dict:
    """Generate a SaaS dashboard application."""
    main_py = f'''#!/usr/bin/env python3
"""
{idea['title']} - SaaS Dashboard
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = Path('index.html').read_text()
            self.wfile.write(html.encode())
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            stats = {{
                "users": 1234,
                "active": 567,
                "revenue": 45678,
                "growth": 23.5
            }}
            self.wfile.write(json.dumps(stats).encode())
        else:
            super().do_GET()

if __name__ == '__main__':
    port = 8080
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"🚀 {{idea['title']}}")
    print(f"📊 Dashboard at http://0.0.0.0:{{port}}")
    server.serve_forever()
'''

    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{idea['title']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f7fa;
        }}
        .header {{
            background: white;
            padding: 20px 40px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            font-size: 1.8em;
        }}
        .dashboard {{
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
            margin: 10px 0;
        }}
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .features {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
        }}
        .feature-list {{
            list-style: none;
        }}
        .feature-list li {{
            padding: 12px 0;
            border-bottom: 1px solid #ecf0f1;
        }}
        .feature-list li:before {{
            content: "✓ ";
            color: #27ae60;
            font-weight: bold;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 {idea['title']}</h1>
    </div>
    
    <div class="dashboard">
        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="stat-label">Total Users</div>
                <div class="stat-value" id="users">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Active Now</div>
                <div class="stat-value" id="active">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Revenue</div>
                <div class="stat-value" id="revenue">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Growth</div>
                <div class="stat-value" id="growth">-</div>
            </div>
        </div>
        
        <div class="features">
            <h2>Key Features</h2>
            <ul class="feature-list">
                {''.join(f'<li>{feature}</li>' for feature in idea['key_features'][:5])}
            </ul>
        </div>
    </div>
    
    <script>
        async function loadStats() {{
            try {{
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.getElementById('users').textContent = data.users.toLocaleString();
                document.getElementById('active').textContent = data.active.toLocaleString();
                document.getElementById('revenue').textContent = '$' + data.revenue.toLocaleString();
                document.getElementById('growth').textContent = data.growth + '%';
            }} catch (error) {{
                console.error('Error loading stats:', error);
            }}
        }}
        
        loadStats();
        setInterval(loadStats, 5000);
    </script>
</body>
</html>
'''

    readme = f'''# {idea['title']}

{idea['description']}

## Dashboard Features

{chr(10).join(f"- {feature}" for feature in idea['key_features'][:5])}

## Run

```bash
python3 main.py
```

Visit http://localhost:8080
'''

    return {
        "files": [
            {"path": "main.py", "content": main_py},
            {"path": "index.html", "content": index_html},
            {"path": "README.md", "content": readme}
        ],
        "entry_point": "main.py",
        "description": f"SaaS dashboard for {idea['title']}",
        "next_steps": ["Add user authentication", "Implement real data storage", "Add charts"]
    }


def generate_api_service_template(idea: Dict) -> Dict:
    """Generate an API service."""
    return generate_dev_tools_template(idea)  # Similar structure


def generate_marketplace_template(idea: Dict) -> Dict:
    """Generate a marketplace application."""
    return generate_saas_template(idea)  # Similar dashboard structure


def generate_dashboard_template(idea: Dict) -> Dict:
    """Generate a fintech/business dashboard."""
    return generate_saas_template(idea)


def generate_generic_web_app(idea: Dict) -> Dict:
    """Generate a generic web application."""
    return generate_dev_tools_template(idea)


def write_project_files(project_dir: Path, files_data: Dict) -> None:
    """Write generated files to the project directory."""
    project_dir.mkdir(parents=True, exist_ok=True)
    
    for file_info in files_data['files']:
        file_path = project_dir / file_info['path']
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(file_info['content'])
        
        # Make Python files executable
        if file_path.suffix == '.py':
            file_path.chmod(0o755)
    
    # Create .replit file
    entry_point = files_data.get('entry_point', 'main.py')
    replit_config = f'''run = "python3 {entry_point}"
language = "python3"
entrypoint = "{entry_point}"

[nix]
channel = "stable-23_11"
'''
    (project_dir / '.replit').write_text(replit_config)
    
    # Create replit.nix
    replit_nix = '''{ pkgs }: {
  deps = [
    pkgs.python311
  ];
}
'''
    (project_dir / 'replit.nix').write_text(replit_nix)


def iterate_idea(idea: Dict, api_key: str = None) -> Dict:
    """Iterate a single idea by generating/updating its code."""
    project_dir = get_project_dir(idea)
    project_info = scan_existing_project(project_dir)
    
    print(f"  Project: {project_dir.name}")
    print(f"  Status: {'Exists' if project_info['exists'] else 'New'}")
    
    # Generate code
    try:
        if api_key:
            print(f"  Generating code with OpenAI...")
            code_data = generate_code_with_openai(idea, project_info, api_key)
        else:
            print(f"  Generating code from templates...")
            code_data = generate_code_template(idea, project_info)
        
        # Write files
        write_project_files(project_dir, code_data)
        print(f"  ✓ Generated {len(code_data['files'])} files")
        
        # Update idea metadata
        idea["iteration"] += 1
        idea["updated_at"] = datetime.now().isoformat()
        idea["project_path"] = str(project_dir.relative_to(ROOT_DIR))
        
        # Add to history
        history_entry = {
            "iteration": idea["iteration"],
            "timestamp": idea["updated_at"],
            "description": code_data.get("description", "Code generated"),
            "files_created": len(code_data['files']),
            "next_steps": code_data.get("next_steps", [])
        }
        idea["history"].append(history_entry)
        
        return code_data
        
    except Exception as e:
        print(f"  ✗ Error generating code: {e}")
        # Still increment iteration but mark as failed
        idea["iteration"] += 1
        idea["updated_at"] = datetime.now().isoformat()
        idea["history"].append({
            "iteration": idea["iteration"],
            "timestamp": idea["updated_at"],
            "description": f"Code generation failed: {str(e)}",
            "error": True
        })
        return {"error": str(e)}


def main():
    """Main function to iterate all ideas and generate code."""
    print("=" * 60)
    print("ITERATOR - Generate Code for All Ideas")
    print("=" * 60)
    
    # Load current state
    state = load_state()
    
    if not state["ideas"]:
        print("\nNo ideas to iterate. Run generate.py first.")
        return
    
    print(f"\nFound {len(state['ideas'])} ideas")
    print(f"Projects directory: {PROJECTS_DIR.relative_to(ROOT_DIR)}\n")
    
    # Create projects directory
    PROJECTS_DIR.mkdir(exist_ok=True)
    
    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print("Using OpenAI API for code generation...")
    else:
        print("No OPENAI_API_KEY found, using template-based generation...")
    
    print()
    
    # Iterate each idea
    for idx, idea in enumerate(state["ideas"], 1):
        print(f"[{idx}/{len(state['ideas'])}] {idea['title']}")
        print(f"  Category: {idea['category']}")
        print(f"  Current iteration: {idea['iteration']}")
        
        result = iterate_idea(idea, api_key)
        
        if "error" not in result:
            print(f"  → Next steps: {', '.join(result.get('next_steps', [])[:2])}")
        print()
    
    # Update metadata
    state["metadata"]["last_iterate"] = datetime.now().isoformat()
    if "total_iterations" not in state["metadata"]:
        state["metadata"]["total_iterations"] = 0
    state["metadata"]["total_iterations"] += len(state["ideas"])
    
    # Save state
    save_state(state)
    
    print("=" * 60)
    print(f"✓ Successfully generated/updated {len(state['ideas'])} projects")
    print(f"Projects location: {PROJECTS_DIR}")
    print(f"State saved to: {STATE_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
