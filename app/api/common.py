import os
from copy import deepcopy

import trafilatura
from flask import Blueprint, request, current_app, jsonify
from trafilatura.settings import DEFAULT_CONFIG

common_api = Blueprint("common_api", __name__)

# Configure trafilatura with a browser-like User-Agent to avoid being blocked
_trafilatura_config = deepcopy(DEFAULT_CONFIG)
_trafilatura_config.set(
    'DEFAULT',
    'USER_AGENTS',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0'
)


def verify_api_key(api_key):
    """Verify the provided API key against the configured API_KEY env var."""
    valid_api_key = os.getenv('API_KEY')
    return api_key == valid_api_key

@common_api.route("/")
def entry_status():
    """
    metric api

    response success when server is up
    ---
    tags:
        -   common
    responses:
        200:
            description: server ping-pong response
            schema:
                name: ServerMetircResponse
                type: object
                properties:
                    code:
                        type: integer
                    docs:
                        type: string
                        default: http://127.0.0.1:5000/apidocs
                    service:
                        type: string
    """

    return {
        "service": current_app.config["SWAGGER"]["title"],
        "code": 200,
        "docs": f"{request.url_root}apidocs"
    }

@common_api.post("/extract")
def extract():
    """
    extract api by trafilatura
    ---
    tags:
        -   common
    parameters:
        -   in: header
            name: X-API-Key
            required: true
            type: string
            description: API key for authentication
        -   in: body
            name: body
            required: true
            schema:
                name: ExtractRequest
                type: object
                properties:
                    url:
                        type: string
                        description: url to extract
                    raw_html:
                        type: string
                        description: raw html to extract
                    output_options:
                        type: object
                        description: options for trafilatura extraction
                        properties:
                            include_tables:
                                type: boolean
                            include_links:
                                type: boolean
                            include_formatting:
                                type: boolean
                            favor_precision:
                                type: boolean
                            favor_recall:
                                type: boolean
    responses:
        200:
            description: extract response
            schema:
                name: ExtractResponse
                type: object
                properties:
                    title:
                        type: string
                    author:
                        type: string
                    date:
                        type: string
                    description:
                        type: string
                    sitename:
                        type: string
                    image:
                        type: string
                    categories:
                        type: array
                    tags:
                        type: array
                    text:
                        type: string
    """
    api_key = request.headers.get('X-API-Key')
    if not verify_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    input_data = request.get_json()
    url = input_data.get('url', '')
    html = input_data.get('raw_html', '') or trafilatura.fetch_url(url, config=_trafilatura_config)

    if not html:
        return jsonify({"error": "Failed to fetch URL content"}), 400

    output_options = input_data.get('output_options', {})

    # Build extraction parameters
    allowed_params = [
        'include_tables', 'include_links', 'include_formatting',
        'favor_precision', 'favor_recall'
    ]
    extract_params = {
        param: output_options[param]
        for param in allowed_params
        if param in output_options
    }

    # Extract with metadata and images
    result = trafilatura.bare_extraction(
        html,
        url=url,
        with_metadata=True,
        include_images=True,
        **extract_params
    )

    if not result:
        return jsonify({"error": "Failed to extract content"}), 400

    # Convert Document to dict
    data = result.as_dict() if hasattr(result, 'as_dict') else result

    # Build clean response
    response = {
        "title": data.get("title"),
        "author": data.get("author"),
        "date": data.get("date"),
        "description": data.get("description"),
        "sitename": data.get("sitename"),
        "hostname": data.get("hostname"),
        "url": data.get("url") or url,
        "image": data.get("image"),
        "categories": data.get("categories", []),
        "tags": data.get("tags", []),
        "text": data.get("raw_text") or data.get("text"),
        "language": data.get("language"),
    }

    # Remove None values for cleaner response
    response = {k: v for k, v in response.items() if v is not None}

    return jsonify(response)
