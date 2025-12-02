# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A REST API wrapper around [trafilatura](https://github.com/adbar/trafilatura) - a Python library for web content extraction. The API extracts article text and metadata from URLs or raw HTML.

## Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python -m flask --app app/app.py run

# Run with gunicorn (production-like)
gunicorn -w 2 -k gthread --threads 4 -b 0.0.0.0:5000 app.app:app
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov-report=xml --cov=app -v

# Run a single test file
pytest app/api/test_common.py

# Run a specific test
pytest app/api/test_common.py::test_metric_api
```

### Linting
```bash
pylint app
```

### Docker
```bash
docker compose up --build
```

## Architecture

```
app/
├── app.py              # Flask app entrypoint, initializes swagger and routes
├── error.py            # Custom exception classes (FlaskBaseError, ParameterError)
├── api/
│   ├── __init__.py     # mount_routes() registers blueprints
│   ├── common.py       # API endpoints: / (health), /extract (main endpoint)
│   └── test_common.py  # pytest tests
├── config/
│   └── swagger.py      # Swagger UI configuration
└── service/
    └── swagger.py      # Swagger initialization
```

## API Endpoints

- `GET /` - Health check, returns service info
- `POST /extract` - Extract content from URL or HTML
  - Requires `X-API-Key` header (validated against `API_KEY` env var)
  - Body: `{ "url": "..." }` or `{ "raw_html": "..." }`
  - Optional `output_options`: `include_tables`, `include_links`, `include_formatting`, `favor_precision`, `favor_recall`
  - Returns: `title`, `author`, `date`, `description`, `sitename`, `hostname`, `url`, `image`, `categories`, `tags`, `text`, `language`

## Environment Variables

- `PORT` - Server port (default: 5000)
- `API_KEY` - Required for `/extract` endpoint (default: `test123` via docker-compose)
