#!/usr/bin/env python3
"""
URL Shortener Server Startup Script

This script starts the Flask web server for the URL shortener service.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the server
from src.url_shortner.server import app

if __name__ == "__main__":
    # Use port 8080 to avoid conflict with AirPlay on macOS
    port = 8080

    print("🔗 Starting URL Shortener Server...")
    print(f"📍 Server will be available at: http://localhost:{port}")
    print("📝 Open your browser to start shortening URLs!")
    print("=" * 50)

    # Configure Flask for development
    app.config["DEBUG"] = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    app.run(host="127.0.0.1", port=port, debug=True, threaded=True, use_reloader=False)
