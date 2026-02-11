"""
Test which Gemini models work with your API key
Run this before using the app to ensure compatibility
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ No API key found in .env file!")
    print("\n🔧 Quick Fix:")
    print("1. Create a .env file in your project root")
    print("2. Add this line: GEMINI_API_KEY=your_key_here")
    print("3. Get a free key at: https://aistudio.google.com/app/apikey")
    exit(1)

print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}\n")

genai.configure(api_key=api_key)

# Test the updated model list (January 2025 compatible)
test_models = [
    "models/gemini-2.5-flash",      # Latest and fastest
        "models/gemini-flash-latest",   # Auto-updates to latest
        "models/gemini-2.5-pro",        # More powerful
        "models/gemini-2.0-flash",
    
]

print("🧪 Testing Gemini Models:\n")
print("=" * 70)

working_models = []
failed_models = []

for model_name in test_models:
    try:
        print(f"\n🔄 Testing: {model_name}")
        model = genai.GenerativeModel(model_name)
        
        response = model.generate_content(
            "Say 'Hello' in exactly 3 words",
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=50
            )
        )
        
        result_text = response.text.strip()
        print(f"✅ SUCCESS!")
        print(f"   Response: {result_text[:100]}")
        working_models.append(model_name)
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ FAILED")
        print(f"   Error: {error_msg[:150]}")
        failed_models.append((model_name, error_msg))

print("\n" + "=" * 70)
print("\n📊 RESULTS SUMMARY:\n")

if working_models:
    print(f"✅ Working Models ({len(working_models)}):")
    for i, model in enumerate(working_models, 1):
        print(f"   {i}. {model}")
    
    print(f"\n🎯 Your app will use these models in priority order")
else:
    print("❌ No working models found!")
    print("\n🔧 Troubleshooting:")
    print("1. Verify your API key at: https://aistudio.google.com/app/apikey")
    print("2. Check if you have API quota remaining")
    print("3. Ensure stable internet connection")
    print("4. Try generating API key again")

if failed_models:
    print(f"\n⚠️ Failed Models ({len(failed_models)}):")
    for model, error in failed_models:
        print(f"   • {model}")
        if "404" in error or "not found" in error.lower():
            print(f"     → Model not available in your region/plan")
        elif "quota" in error.lower():
            print(f"     → API quota exceeded - wait or upgrade")
        elif "api key" in error.lower():
            print(f"     → API key issue - regenerate key")
        else:
            print(f"     → {error[:80]}")

print("\n" + "=" * 70)
print("\n✨ Next Steps:")
if working_models:
    print("1. ✅ Your API is properly configured!")
    print("2. Run: streamlit run app.py")
    print("3. Start optimizing resumes for 75%+ ATS scores!")
else:
    print("1. Fix the API key issues above")
    print("2. Run this script again to verify")
    print("3. Once working, run: streamlit run app.py")

print("\n💡 TIP: Free tier limits:")
print("   • 15 requests per minute")
print("   • 1,500 requests per day")
print("   • If exceeded, wait 1-2 minutes between requests")
