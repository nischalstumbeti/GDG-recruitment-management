# Supabase Integration Guide

This guide will help you integrate Supabase into your GDG Interview Management System.

## Prerequisites

1. A Supabase account (free tier available at [supabase.com](https://supabase.com))
2. A Supabase project created

## Step 1: Set Up Supabase Database

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Run the SQL schema from `database_schema.sql` to create all tables

## Step 2: Get Your Supabase Credentials

1. Go to **Settings** → **API** in your Supabase project
2. Copy the following:
   - **Project URL** (SUPABASE_URL)
   - **anon/public key** (SUPABASE_KEY)

## Step 3: Configure Supabase in Your Project

### Option A: Using Environment Variables (Recommended)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here
   ```

3. Update `supabase_config.py` to load from environment:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Option B: Direct Configuration

Edit `supabase_config.py` and replace:
- `YOUR_SUPABASE_URL` with your project URL
- `YOUR_SUPABASE_ANON_KEY` with your anon key

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `supabase` - Supabase Python client
- `python-dotenv` - For environment variable management

## Step 5: Update app.py to Use Supabase

Replace JSON file operations with Supabase database calls:

### Before (JSON):
```python
from app import load_json, save_json

users = load_json(USERS_FILE)
save_json(USERS_FILE, users)
```

### After (Supabase):
```python
from db import get_all_users, create_user, update_user

users = get_all_users()
create_user(user_id, passcode, role, name)
update_user(user_id, updates)
```

## Key Changes Needed in app.py

1. **Replace imports:**
   ```python
   # Remove or comment out:
   # from app import load_json, save_json
   
   # Add:
   from db import (
       get_all_users, get_user, create_user, update_user, delete_user,
       get_all_candidates, get_candidate, create_candidate,
       get_all_checklists, get_checklist, save_checklist,
       init_default_user
   )
   ```

2. **Replace `load_json(USERS_FILE)` with `get_all_users()`**
3. **Replace `load_json(CANDIDATES_FILE)` with `get_all_candidates()`**
4. **Replace `load_json(CHECKLISTS_FILE)` with `get_all_checklists()`**
5. **Replace `save_json()` calls with appropriate database functions**

## Example: Updated Login Route

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        passcode = request.form.get('passcode', '').strip()
        
        user = get_user(user_id)  # Changed from load_json
        
        if user and user['passcode'] == passcode:
            # ... rest of login logic ...
            update_user(user_id, {
                'last_login': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip_address': location_info['ip'],
                'location': location_info['location'],
                'isp': location_info['isp']
            })  # Changed from save_json
            # ...
```

## Benefits of Supabase

✅ **Real Database**: PostgreSQL with proper relationships and constraints
✅ **Scalability**: Handles large datasets efficiently
✅ **Real-time**: Optional real-time subscriptions for live updates
✅ **Security**: Row Level Security (RLS) policies
✅ **Backups**: Automatic database backups
✅ **Storage**: Built-in file storage (can replace local uploads folder)

## Troubleshooting

### "Please set your Supabase credentials" error
- Make sure you've configured `supabase_config.py` or set environment variables
- Check that your `.env` file exists and has correct values

### Database errors
- Ensure you've run the SQL schema in Supabase first
- Check that your Supabase project is active
- Verify your API key has the correct permissions
- Make sure tables exist before using the application

### Connection errors
- Check your internet connection
- Verify your Supabase project URL is correct
- Ensure your Supabase project is not paused

## Next Steps

After setup:
1. Test all functionality to ensure everything works
2. Consider enabling Row Level Security (RLS) in Supabase for better security
3. Optionally use Supabase Storage for file uploads
4. Consider using Supabase Auth for enhanced authentication

## Initializing Default Data

The `init_default_user()` function in `db.py` will automatically create a default admin user if one doesn't exist:
- User ID: `admin`
- Passcode: `admin123`
- Role: `admin`

You can call this function when your app starts, or manually create users through the application interface.

