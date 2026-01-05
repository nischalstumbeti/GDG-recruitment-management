"""
Database module - Supabase integration
Replaces JSON file operations with Supabase database calls
"""
from supabase_config import get_supabase_client
from datetime import datetime
from typing import Dict, List, Optional, Any

def get_user(user_id: str) -> Optional[Dict]:
    """Get a single user by user_id"""
    try:
        supabase = get_supabase_client()
        response = supabase.table('users_re26').select('*').eq('user_id', user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_all_users() -> Dict[str, Dict]:
    """Get all users, returns as dict with user_id as key (for compatibility)"""
    try:
        supabase = get_supabase_client()
        response = supabase.table('users_re26').select('*').execute()
        users_dict = {}
        for user in response.data:
            users_dict[user['user_id']] = user
        return users_dict
    except Exception as e:
        print(f"Error getting users: {e}")
        return {}

def create_user(user_id: str, passcode: str, role: str, name: str) -> bool:
    """Create a new user"""
    try:
        supabase = get_supabase_client()
        supabase.table('users_re26').insert({
            'user_id': user_id,
            'passcode': passcode,
            'role': role,
            'name': name,
            'last_login': None,
            'ip_address': None,
            'location': None,
            'isp': None
        }).execute()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def update_user(user_id: str, updates: Dict) -> bool:
    """Update user information"""
    try:
        supabase = get_supabase_client()
        supabase.table('users_re26').update(updates).eq('user_id', user_id).execute()
        return True
    except Exception as e:
        print(f"Error updating user: {e}")
        return False

def delete_user(user_id: str) -> bool:
    """Delete a user"""
    try:
        supabase = get_supabase_client()
        supabase.table('users_re26').delete().eq('user_id', user_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False

def get_candidate(register_id: str) -> Optional[Dict]:
    """Get a single candidate by register_id"""
    try:
        supabase = get_supabase_client()
        response = supabase.table('candidates_re26').select('*').eq('register_id', register_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting candidate: {e}")
        return None

def get_all_candidates() -> Dict[str, Dict]:
    """Get all candidates, returns as dict with register_id as key"""
    try:
        supabase = get_supabase_client()
        response = supabase.table('candidates_re26').select('*').execute()
        candidates_dict = {}
        for candidate in response.data:
            candidates_dict[candidate['register_id']] = candidate
        return candidates_dict
    except Exception as e:
        print(f"Error getting candidates: {e}")
        return {}

def create_candidate(candidate_data: Dict) -> bool:
    """Create a new candidate"""
    try:
        supabase = get_supabase_client()
        supabase.table('candidates_re26').insert(candidate_data).execute()
        return True
    except Exception as e:
        print(f"Error creating candidate: {e}")
        return False

def update_candidate(register_id: str, updates: Dict) -> bool:
    """Update candidate information"""
    try:
        supabase = get_supabase_client()
        supabase.table('candidates_re26').update(updates).eq('register_id', register_id).execute()
        return True
    except Exception as e:
        print(f"Error updating candidate: {e}")
        return False

def get_checklist(register_id: str) -> Optional[Dict]:
    """Get checklist for a candidate, including technical skills"""
    try:
        supabase = get_supabase_client()
        # Get checklist
        checklist_response = supabase.table('checklists_re26').select('*').eq('register_id', register_id).execute()
        
        if not checklist_response.data:
            return None
        
        checklist = checklist_response.data[0]
        
        # Get technical skills
        skills_response = supabase.table('technical_skills_re26').select('*').eq('register_id', register_id).execute()
        checklist['technical_skills'] = [
            {'technology': skill['technology'], 'skill_level': skill['skill_level']}
            for skill in skills_response.data
        ]
        
        return checklist
    except Exception as e:
        print(f"Error getting checklist: {e}")
        return None

def get_all_checklists() -> Dict[str, Dict]:
    """Get all checklists with technical skills"""
    try:
        supabase = get_supabase_client()
        # Get all checklists
        checklists_response = supabase.table('checklists_re26').select('*').execute()
        
        # Get all technical skills
        skills_response = supabase.table('technical_skills_re26').select('*').execute()
        
        # Group skills by register_id
        skills_by_register = {}
        for skill in skills_response.data:
            register_id = skill['register_id']
            if register_id not in skills_by_register:
                skills_by_register[register_id] = []
            skills_by_register[register_id].append({
                'technology': skill['technology'],
                'skill_level': skill['skill_level']
            })
        
        # Combine checklists with skills
        checklists_dict = {}
        for checklist in checklists_response.data:
            register_id = checklist['register_id']
            checklist['technical_skills'] = skills_by_register.get(register_id, [])
            checklists_dict[register_id] = checklist
        
        return checklists_dict
    except Exception as e:
        print(f"Error getting checklists: {e}")
        return {}

def save_checklist(register_id: str, checklist_data: Dict) -> bool:
    """Save or update a checklist with technical skills"""
    try:
        supabase = get_supabase_client()
        
        # Extract technical skills
        technical_skills = checklist_data.pop('technical_skills', [])
        
        # Prepare checklist data (remove technical_skills if present)
        # Note: updated_at is handled by database trigger, created_at by default
        checklist_record = {
            'register_id': register_id,
            'practical_experience': checklist_data.get('practical_experience', ''),
            'communication_skills': checklist_data.get('communication_skills', ''),
            'time_management': checklist_data.get('time_management', ''),
            'leadership_ability': checklist_data.get('leadership_ability', ''),
            'interviewer_comments': checklist_data.get('interviewer_comments', ''),
            'faculty_comments': checklist_data.get('faculty_comments', ''),
            'interview_taken_by': checklist_data.get('interview_taken_by', ''),
            'reviewed_by': checklist_data.get('reviewed_by', ''),
            'remarks': checklist_data.get('remarks', '')
        }
        
        # Check if checklist exists
        existing = supabase.table('checklists_re26').select('checklist_id').eq('register_id', register_id).execute()
        
        if existing.data:
            # Update existing checklist (trigger will auto-update updated_at)
            supabase.table('checklists_re26').update(checklist_record).eq('register_id', register_id).execute()
        else:
            # Create new checklist (defaults will set created_at and updated_at)
            supabase.table('checklists_re26').insert(checklist_record).execute()
        
        # Delete existing technical skills for this register_id
        supabase.table('technical_skills_re26').delete().eq('register_id', register_id).execute()
        
        # Insert new technical skills
        if technical_skills:
            skills_to_insert = [
                {
                    'register_id': register_id,
                    'technology': skill['technology'],
                    'skill_level': skill['skill_level']
                }
                for skill in technical_skills if skill.get('technology')
            ]
            if skills_to_insert:
                supabase.table('technical_skills_re26').insert(skills_to_insert).execute()
        
        return True
    except Exception as e:
        print(f"Error saving checklist: {e}")
        return False

def init_default_user():
    """Initialize default admin user if it doesn't exist"""
    try:
        admin = get_user('admin')
        if not admin:
            create_user('admin', 'admin123', 'admin', 'Administrator')
            return True
        return False
    except Exception as e:
        print(f"Error initializing default user: {e}")
        return False

