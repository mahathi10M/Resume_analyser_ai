"""
Utility script to check which Gemini models are available in your API
Run this to see what models you can actually use
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("🔍 Checking available Gemini models...\n")
print("=" * 70)

try:
    # List all available models
    available_models = []
    
    for model in genai.list_models():
        # Check if model supports generateContent
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"✅ {model.name}")
            print(f"   Description: {model.description}")
            print(f"   Methods: {', '.join(model.supported_generation_methods)}")
            print()
    
    print("=" * 70)
    print(f"\n📊 Total available models: {len(available_models)}")
    print("\n💡 RECOMMENDED MODELS FOR YOUR APP:\n")
    
    # Filter for commonly used models
    recommended = []
    for model_name in available_models:
        if 'flash' in model_name.lower() or 'pro' in model_name.lower():
            recommended.append(model_name)
    
    if recommended:
        print("Use these in your code:")
        for i, model in enumerate(recommended[:5], 1):
            # Remove 'models/' prefix for cleaner code
            clean_name = model.replace('models/', '')
            print(f"{i}. '{clean_name}'")
    else:
        print("Use any from the list above")
    
    print("\n" + "=" * 70)
    print("\n🔧 HOW TO FIX YOUR CODE:\n")
    
    if recommended:
        print("Replace model names in resume_generator.py and app.py with:")
        print("\nmodel_priority = [")
        for model in recommended[:3]:
            clean_name = model.replace('models/', '')
            print(f'    "{clean_name}",')
        print("]")
    
    print("\n" + "=" * 70)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nPossible issues:")
    print("1. Check your API key is valid")
    print("2. Check internet connection")
    print("3. Verify API access at: https://aistudio.google.com/")

print("\n✅ Done! Use the recommended models in your code.")
