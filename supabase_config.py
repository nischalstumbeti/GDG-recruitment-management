"""
Supabase Configuration
Set your Supabase credentials here or use environment variables
"""
import os
from supabase import create_client, Client

# Try to load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use environment variables or direct config

# Supabase configuration
# Get these from your Supabase project settings: https://app.supabase.com/project/_/settings/api
SUPABASE_URL = os.getenv('SUPABASE_URL', 'YOUR_SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'YOUR_SUPABASE_ANON_KEY')

def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    if SUPABASE_URL == 'YOUR_SUPABASE_URL' or SUPABASE_KEY == 'YOUR_SUPABASE_ANON_KEY':
        print("\n" + "="*60)
        print("ERROR: Supabase credentials not configured!")
        print("="*60)
        print("\nTo fix this, you have two options:\n")
        print("Option 1: Edit supabase_config.py directly")
        print("  - Replace 'YOUR_SUPABASE_URL' with your Supabase project URL")
        print("  - Replace 'YOUR_SUPABASE_ANON_KEY' with your Supabase anon key")
        print("\nOption 2: Create a .env file in the project root:")
        print("  SUPABASE_URL=https://your-project.supabase.co")
        print("  SUPABASE_KEY=your-anon-key-here")
        print("\nGet your credentials from:")
        print("  https://app.supabase.com/project/_/settings/api")
        print("="*60 + "\n")
        raise ValueError("Supabase credentials not configured. See error message above.")
    
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        if "Invalid API key" in str(e) or "invalid" in str(e).lower():
            print("\n" + "="*60)
            print("ERROR: Invalid Supabase API key!")
            print("="*60)
            print("\nPlease verify your Supabase credentials:")
            print("  1. Check that SUPABASE_URL is correct")
            print("  2. Check that SUPABASE_KEY is the 'anon' or 'public' key (not service_role)")
            print("  3. Get fresh credentials from:")
            print("     https://app.supabase.com/project/_/settings/api")
            print("="*60 + "\n")
        raise

