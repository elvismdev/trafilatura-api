# Trafilatura REST API

A REST API wrapper around [Trafilatura](https://github.com/adbar/trafilatura) for extracting article content and metadata from web pages.

## Features

- Extract article text, title, author, date, and more from any URL
- Featured image extraction
- Categories and tags detection
- Language detection
- API key authentication
- Docker support
- Swagger UI documentation

## Quick Start

### Using Docker Compose

```bash
git clone https://github.com/elvismdev/trafilatura-api.git
cd trafilatura-api
docker compose up --build
```

The API will be available at `http://localhost:5000`

### Using Docker

```bash
docker run -d -p 5000:5000 ghcr.io/elvismdev/trafilatura-api:latest
```

## API Endpoints

### Health Check

```
GET /
```

Returns service status and documentation URL.

### Extract Content

```
POST /extract
```

Extracts article content and metadata from a URL or raw HTML.

**Headers:**
```
Content-Type: application/json
X-API-Key: test123
```

**Request Body:**
```json
{
  "url": "https://example.com/article",
  "output_options": {
    "include_tables": true,
    "include_links": true,
    "favor_recall": true
  }
}
```

Or with raw HTML:
```json
{
  "raw_html": "<html>...</html>",
  "url": "https://example.com/article"
}
```

**Response:**
```json
{
  "title": "Article Title",
  "author": "Author Name",
  "date": "2025-12-01",
  "description": "Article excerpt or meta description",
  "sitename": "Example News",
  "hostname": "example.com",
  "url": "https://example.com/article",
  "image": "https://example.com/featured-image.jpg",
  "categories": ["News", "Technology"],
  "tags": ["AI", "Machine Learning"],
  "text": "Full article content...",
  "language": "en"
}
```

**Output Options:**

| Option | Type | Description |
|--------|------|-------------|
| `include_tables` | boolean | Include table content |
| `include_links` | boolean | Preserve hyperlinks in text |
| `include_formatting` | boolean | Keep text formatting |
| `favor_precision` | boolean | Prefer less text but higher accuracy |
| `favor_recall` | boolean | Prefer more text even if uncertain |

## Usage Examples

### Basic extraction

```bash
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{"url": "https://example.com/article"}'
```

### With output options

```bash
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{
    "url": "https://example.com/article",
    "output_options": {
      "include_links": true,
      "favor_recall": true
    }
  }'
```

## Swagger Documentation

Interactive API documentation is available at:
```
http://localhost:5000/apidocs
```

## Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m flask --app app/app.py run

# Run tests
pytest -v
```

## Deployment

### QNAP Container Station

1. Pull image: `ghcr.io/elvismdev/trafilatura-api:latest`
2. Create container with port mapping `5000:5000`

### GitHub Container Registry

Images are automatically built and pushed on every commit to `master`:
```
ghcr.io/elvismdev/trafilatura-api:latest
```

## License

MIT
