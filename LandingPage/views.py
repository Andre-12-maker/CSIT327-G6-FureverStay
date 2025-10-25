from django.shortcuts import render
from django.db import connection

def home(request):
    return render(request, 'home.html')

def check_db_connection():
    try:
        connection.ensure_connection()
        return True
    except Exception:
        return False
