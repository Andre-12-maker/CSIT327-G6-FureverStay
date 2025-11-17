import os
from supabase import create_client
from django.conf import settings

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
