# mcp_playwright_tool.py

from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from jsonschema import validate, ValidationError

app = Flask(__name__)

# === Define the Capability Schema ===
CAPABILITIES = {
    "extract_table": {
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "selector": {"type": "string"}
            },
            "required": ["url", "selector"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {"type": "object"}
                }
            },
            "required": ["data"]
        }
    }
}

# === HTML Table Parser ===
def parse_html_table(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if table is None:
        return []
    headers = [th.text.strip() for th in table.find_all('th')]
    rows = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all(['td', 'th'])
        row_data = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
        rows.append(row_data)
    return rows

# === Playwright Execution ===
def extract_table(url, selector):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(selector)
        table_html = page.locator(selector).inner_html()
        browser.close()
        return {"data": parse_html_table(f"<table>{table_html}</table>")}

# === Flask Route ===
@app.route("/run", methods=["POST"])
def handle_request():
    data = request.get_json()
    action = data.get("action")
    parameters = data.get("parameters")

    if action not in CAPABILITIES:
        return jsonify({"error": "Unsupported action."}), 400

    try:
        validate(instance=parameters, schema=CAPABILITIES[action]["input_schema"])
    except ValidationError as ve:
        return jsonify({"error": f"Invalid parameters: {ve.message}"}), 400

    if action == "extract_table":
        result = extract_table(parameters["url"], parameters["selector"])
        return jsonify(result)

    return jsonify({"error": "Handler not implemented."}), 501

if __name__ == "__main__":
    app.run(port=8080, debug=True)
