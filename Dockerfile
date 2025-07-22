# Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y curl unzip libglib2.0-0 libnss3 libgdk-pixbuf2.0-0 libgtk-3-0 libxss1 libasound2 \
    && pip install --no-cache-dir flask playwright beautifulsoup4 jsonschema \
    && python -m playwright install

EXPOSE 8080

CMD ["python", "mcp_playwright_tool.py"]