# Supabase Quick Start Guide

## Error: "Invalid API key"

If you're seeing this error, you need to configure your Supabase credentials.

## Step 1: Get Your Supabase Credentials

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project (or create a new one)
3. Go to **Settings** → **API**
4. Copy:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon public key** (long string starting with `eyJ...`)

## Step 2: Configure Credentials

### Option A: Using .env file (Recommended)

1. Create a file named `.env` in the project root
2. Add your credentials:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-key-here
   ```

### Option B: Edit supabase_config.py directly

1. Open `supabase_config.py`
2. Replace `YOUR_SUPABASE_URL` with your project URL
3. Replace `YOUR_SUPABASE_ANON_KEY` with your anon key

## Step 3: Run the SQL Schema

Before using the app, you need to create the database tables:

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Copy and paste the contents of `database_schema.sql`
4. Click **Run** to execute the SQL

## Step 4: Restart Your Flask App

After configuring credentials, restart your Flask application.

## Troubleshooting

- **"Invalid API key"**: Make sure you're using the **anon/public** key, not the service_role key
- **"Table doesn't exist"**: Run the SQL schema from `database_schema.sql` first
- **Connection errors**: Check your internet connection and verify the project URL is correct

