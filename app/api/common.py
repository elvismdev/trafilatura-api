from flask import Blueprint, request, current_app, jsonify
from copy import deepcopy
import trafilatura
from trafilatura.settings import DEFAULT_CONFIG
import os

common_api = Blueprint("common_api", __name__)

# Configure trafilatura with a browser-like User-Agent to avoid being blocked
_trafilatura_config = deepcopy(DEFAULT_CONFIG)
_trafilatura_config.set(
    'DEFAULT',
    'USER_AGENTS',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
)

def verify_api_key(api_key):
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
    # json api
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
                            include_comments:
                                type: boolean
                            include_tables:
                                type: boolean
                            include_links:
                                type: boolean
                            include_formatting:
                                type: boolean
                            include_images:
                                type: boolean
                            output_format:
                                type: string
                                enum: [csv, json, html, markdown, txt, xml, xmltei]
                            with_metadata:
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
                    text:
                        type: string
    """
    api_key = request.headers.get('X-API-Key')
    if not verify_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    input = request.get_json()
    html = input.get('raw_html', '') or trafilatura.fetch_url(input['url'], config=_trafilatura_config)
    output_options = input.get('output_options', {})
    allowed_params = ['include_comments', 'include_tables', 'include_links', 'include_formatting', 'include_images', 'output_format', 'with_metadata', 'favor_precision', 'favor_recall']
    extract_params = {param: output_options[param] for param in allowed_params if param in output_options}
    article = trafilatura.extract(html, **extract_params)
    return {"output": article}
