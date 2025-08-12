#!/usr/bin/env python3
"""
ESG Copilot - Startup Script
AI-powered ESG compliance analysis for Dutch banks
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Main startup function"""
    print("🌍 ESG Copilot - Dutch Banks Compliance Analysis")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("   Please copy env.example to .env and configure your settings.")
        print("   Required environment variables:")
        print("   - OPENAI_API_KEY")
        print("   - DATABASE_URL")
        print("   - SECRET_KEY")
        print()
    
    # Check for required environment variables
    required_vars = ["OPENAI_API_KEY", "DATABASE_URL", "SECRET_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        print("Please set these variables in your .env file or environment.")
        sys.exit(1)
    
    print("✅ Environment configuration validated")
    print("🚀 Starting ESG Copilot...")
    print()
    print("📊 Dashboard: http://localhost:3000")
    print("📚 API Docs: http://localhost:3000/docs")
    print("🔍 Health Check: http://localhost:3000/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the application
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=3000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 ESG Copilot stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting ESG Copilot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 