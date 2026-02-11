import subprocess
import os

print("🔍 Checking .gitignore setup...\n")

# Check if .gitignore exists
if os.path.exists(".gitignore"):
    print("✅ .gitignore file exists")
    
    with open(".gitignore", "r") as f:
        content = f.read()
        
        if ".env" in content:
            print("✅ .env is in .gitignore")
        else:
            print("❌ .env NOT in .gitignore - ADD IT NOW!")
        
        if ".venv" in content or "venv/" in content:
            print("✅ Virtual environment is in .gitignore")
        else:
            print("⚠️  Consider adding .venv/ to .gitignore")
else:
    print("❌ .gitignore file NOT FOUND - CREATE IT!")

# Check if .env exists
if os.path.exists(".env"):
    print("✅ .env file exists")
else:
    print("⚠️  .env file not found")

# Check git status
try:
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )
    
    if ".env" in result.stdout:
        print("❌ WARNING: .env is being tracked by Git!")
        print("   Run: git rm --cached .env")
    else:
        print("✅ .env is properly ignored by Git")
        
except Exception as e:
    print(f"ℹ️  Git not initialized or not in a Git repo: {e}")

print("\n✨ Check complete!")