import os
from supabase import create_client, Client

class SupabaseService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if url and key:
            self.supabase: Client = create_client(url, key)
        else:
            self.supabase = None
            print("Supabase credentials not found in environment variables.")

    def save_analysis(self, original_text, analysis_result, user_email):
        if not self.supabase:
            return None
        
        try:
            data = {
                "original_text": original_text,
                "classification": analysis_result.get("classification"),
                "suggested_response": analysis_result.get("suggested_response"),
                "reasoning": analysis_result.get("reasoning"),
                "subject": analysis_result.get("subject", "No Subject"),
                "sender": analysis_result.get("sender", "Unknown"),
                "analyzed_by": user_email
            }
            
            result = self.supabase.table("emails").insert(data).execute()
            return result.data
        except Exception as e:
            print(f"Error saving to Supabase: {e}")
            return None

    def get_history(self, user_email, limit=10):
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table("emails")\
                .select("*")\
                .eq("analyzed_by", user_email)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error fetching from Supabase: {e}")
            return []

    def delete_analysis(self, analysis_id):
        if not self.supabase:
            return False
        
        try:
            self.supabase.table("emails").delete().eq("id", analysis_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting from Supabase: {e}")
            return False
