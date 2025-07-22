import requests

payload = {
    "action": "extract_table",
    "parameters": {
        "url": "https://www.w3schools.com/html/html_tables.asp",
        "selector": "#customers"
    }
}

response = requests.post("http://localhost:8080/run", json=payload)

if response.ok:
    for row in response.json()["data"]:
        print(row)
else:
    print("Error:", response.json())
