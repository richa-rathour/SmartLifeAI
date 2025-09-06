"""
Setup script for SmartLife AI Backend
Helps users get started quickly with the application
"""

import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists("env_example.txt"):
        try:
            with open("env_example.txt", "r") as src:
                content = src.read()
            
            with open(".env", "w") as dst:
                dst.write(content)
            
            print("✅ .env file created from template")
            print("⚠️  Please edit .env file and add your OpenAI API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env_example.txt not found")
        return False

def check_openai_key():
    """Check if OpenAI API key is set"""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            if "your_openai_api_key_here" in content:
                print("⚠️  Please update .env file with your actual OpenAI API key")
                return False
            elif "OPENAI_API_KEY=" in content:
                print("✅ OpenAI API key appears to be set")
                return True
    
    print("⚠️  OpenAI API key not found in .env file")
    return False

def main():
    """Main setup function"""
    print("🚀 SmartLife AI Backend Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Check OpenAI key
    check_openai_key()
    
    print("\n🎉 Setup completed!")
    print("\n📝 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run the application: python app.py")
    print("3. Test the API: python test_api.py")
    print("\n📖 For detailed instructions, see README.md")
    
    return True

if __name__ == "__main__":
    main()
