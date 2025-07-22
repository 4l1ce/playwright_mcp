# Playwright + MCP

## How to run

### 0. Clone this repository

```bash
git clone https://github.com/4l1ce/playwright_mcp.git
cd playwright_mcp
```

### 1. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

Install Python packages:

```bash
pip install -r requirements.txt
```

> Ensure you're using **Python 3.9+**

Playwright:
```bash
playwright install
```
---

### Docker
```bash
docker build -t mcp-playwright-tool .
docker run -p 8080:8080 mcp-playwright-tool
```
---

### 3. Execute request
Requests example in `call_agent.py`
```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{
    "action": "extract_table",
    "parameters": {
      "url": "https://www.w3schools.com/html/html_tables.asp",
      "selector": "#customers"
    }
  }'
```
