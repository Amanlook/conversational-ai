"""Flask web server for URL shortener service."""

import datetime
import os
from urllib.parse import urlparse

from flask import Flask, jsonify, redirect, render_template_string, request

from src.helpers.redis import RedisCache
from src.url_shortner.shortner import URLShortener

app = Flask(__name__)

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input[type="url"], input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input[type="url"]:focus, input[type="text"]:focus {
            border-color: #4CAF50;
            outline: none;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #e8f5e8;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }
        .error {
            background-color: #ffe8e8;
            border-left-color: #f44336;
        }
        .short-url {
            font-family: monospace;
            font-size: 18px;
            color: #2196F3;
            word-break: break-all;
        }
        .copy-btn {
            background-color: #2196F3;
            padding: 5px 15px;
            font-size: 14px;
            margin-left: 10px;
            width: auto;
            display: inline-block;
        }
        .copy-btn:hover {
            background-color: #1976D2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 URL Shortener</h1>

        <form id="shortenForm" onsubmit="shortenURL(event)">
            <div class="form-group">
                <label for="url">Enter URL to shorten:</label>
                <input type="url" id="url" name="url" placeholder="https://example.com" required>
            </div>

            <div class="form-group">
                <label for="user_id">Your Name/ID:</label>
                <input type="text" id="user_id" name="user_id" placeholder="Enter your name" required>
            </div>

            <button type="submit">Shorten URL</button>
        </form>

        <div id="result" style="display: none;"></div>
    </div>

    <script>
        async function shortenURL(event) {
            event.preventDefault();

            const url = document.getElementById('url').value;
            const userId = document.getElementById('user_id').value;
            const resultDiv = document.getElementById('result');

            try {
                const response = await fetch('/api/shorten', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        url: url,
                        user_id: userId
                    })
                });

                const data = await response.json();

                if (data.success) {
                    resultDiv.innerHTML = `
                        <div class="result">
                            <strong>Shortened URL:</strong><br>
                            <span class="short-url">${data.short_url}</span>
                            <button class="copy-btn" onclick="copyToClipboard('${data.short_url}')">Copy</button>
                            <br><br>
                            <strong>Short Code:</strong> ${data.short_code}
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div class="result error">
                            <strong>Error:</strong> ${data.error}
                        </div>
                    `;
                }

                resultDiv.style.display = 'block';

            } catch (error) {
                resultDiv.innerHTML = `
                    <div class="result error">
                        <strong>Error:</strong> Failed to shorten URL. Please try again.
                    </div>
                `;
                resultDiv.style.display = 'block';
            }
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                alert('URL copied to clipboard!');
            });
        }
    </script>
</body>
</html>
"""


def is_valid_url(url: str) -> bool:
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


@app.route("/health")
def health_check():
    """Simple health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "message": "URL Shortener is running!",
            "timestamp": datetime.datetime.now().isoformat(),
        }
    )


@app.route("/")
def home():
    """Serve the main URL shortener page."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    """API endpoint to shorten a URL."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        url = data.get("url")
        user_id = data.get("user_id")

        if not url or not user_id:
            return jsonify(
                {"success": False, "error": "URL and user_id are required"}
            ), 400

        if not is_valid_url(url):
            return jsonify({"success": False, "error": "Invalid URL format"}), 400

        # Create URL shortener instance
        shortener = URLShortener(url=url, user_id=user_id)
        short_code = shortener.short_url()

        if not short_code:
            return jsonify(
                {"success": False, "error": "Failed to generate short URL"}
            ), 500

        # Construct the full short URL
        base_url = request.host_url.rstrip("/")
        short_url = f"{base_url}/s/{short_code}"

        return jsonify(
            {
                "success": True,
                "short_url": short_url,
                "short_code": short_code,
                "original_url": url,
            }
        )

    except Exception as e:
        return jsonify(
            {"success": False, "error": f"Internal server error: {str(e)}"}
        ), 500


@app.route("/s/<short_code>")
def redirect_to_url(short_code: str):
    """Redirect short code to original URL."""
    try:
        # Get the original URL from cache
        cache = RedisCache()
        original_url = cache.get_cache(short_code)

        if not original_url:
            return render_template_string("""
                <h1>404 - URL Not Found</h1>
                <p>The short URL you're looking for doesn't exist or has expired.</p>
                <a href="/">Create a new short URL</a>
            """), 404

        return redirect(original_url)

    except Exception as e:
        return render_template_string(f"""
            <h1>Error</h1>
            <p>An error occurred while redirecting: {str(e)}</p>
            <a href="/">Go back to home</a>
        """), 500


@app.route("/api/stats/<short_code>")
def get_url_stats(short_code: str):
    """Get statistics for a short URL."""
    try:
        cache = RedisCache()
        original_url = cache.get_cache(short_code)

        if not original_url:
            return jsonify({"success": False, "error": "Short URL not found"}), 404

        return jsonify(
            {
                "success": True,
                "short_code": short_code,
                "original_url": original_url,
                "exists": True,
            }
        )

    except Exception as e:
        return jsonify(
            {"success": False, "error": f"Error retrieving stats: {str(e)}"}
        ), 500


if __name__ == "__main__":
    # Get port from environment or use default (8080 to avoid AirPlay conflict on macOS)
    port = int(os.environ.get("PORT", 8080))

    print(f"🚀 URL Shortener server starting on http://localhost:{port}")
    print("📝 Open your browser to create short URLs")
    print(f"🔗 Use http://localhost:{port}/s/<code> format for redirects")

    # Configure Flask for development
    app.config["DEBUG"] = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    app.run(host="127.0.0.1", port=port, debug=True, threaded=True, use_reloader=False)
