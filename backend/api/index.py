"""
Vercel serverless function entry point
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

# Vercel expects a handler
def handler(request, context):
    return app(request, context)
