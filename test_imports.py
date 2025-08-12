#!/usr/bin/env python3
"""
Simple import test to verify all modules can be imported correctly
"""

def test_imports():
    """Test all imports"""
    try:
        # Test basic imports
        print("Testing basic imports...")
        import asyncio
        import json
        import os
        from datetime import datetime
        print("✅ Basic imports successful")
        
        # Test FastAPI imports
        print("Testing FastAPI imports...")
        from fastapi import FastAPI
        print("✅ FastAPI imports successful")
        
        # Test LangChain imports
        print("Testing LangChain imports...")
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from langchain_community.vectorstores import Chroma
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        print("✅ LangChain imports successful")
        
        # Test ChromaDB imports
        print("Testing ChromaDB imports...")
        import chromadb
        print("✅ ChromaDB imports successful")
        
        # Test other dependencies
        print("Testing other dependencies...")
        import aiohttp
        import feedparser
        from bs4 import BeautifulSoup
        print("✅ Other dependencies successful")
        
        print("\n🎉 All imports successful! The application should work correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install missing dependencies using: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports() 