import os
import sys
from dotenv import load_dotenv

print("🔍 Checking setup...\n")

# Check if in virtual environment
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("✅ Virtual environment is active")
else:
    print("⚠️  Virtual environment not active")

# Load .env
load_dotenv()

# Check API key
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print(f"✅ API Key loaded: {api_key[:10]}...{api_key[-4:]}")
else:
    print("❌ API Key NOT found in .env")

# Check required packages
packages = {
    'streamlit': 'streamlit',
    'faiss': 'faiss-cpu', 
    'sentence_transformers': 'sentence-transformers',
    'google.generativeai': 'google-generativeai',
    'dotenv': 'python-dotenv'
}

print("\n📦 Checking packages:")
for package, install_name in packages.items():
    try:
        __import__(package.replace('-', '_'))
        print(f"✅ {package}")
    except ImportError:
        print(f"❌ {package} - Run: pip install {install_name}")

print("\n✨ Setup check complete!")