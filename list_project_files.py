#!/usr/bin/env python3
import os

def list_project_files():
    """List all important project files"""
    print("=== WordSearch Extreme Project Structure ===\n")
    
    important_files = [
        "manage.py",
        "requirements.txt", 
        "README.md",
        ".gitignore",
        "db.sqlite3",
        "wordsearch_project/settings.py",
        "wordsearch_project/urls.py",
        "wordsearch/models.py",
        "wordsearch/views.py", 
        "wordsearch/urls.py",
        "wordsearch/admin.py",
        "wordsearch/serializers.py",
        "templates/base.html",
        "templates/wordsearch/home.html",
        "templates/wordsearch/puzzle_list.html",
        "templates/wordsearch/puzzle_detail.html",
        "templates/wordsearch/puzzle_create.html",
        "wordsearch/static/css/style.css",
        ".vscode/settings.json",
        ".vscode/launch.json",
        "wordsearch-extreme.code-workspace"
    ]
    
    for file_path in important_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path:<50} ({size:>6} bytes)")
        else:
            print(f"✗ {file_path:<50} (missing)")
    
    print(f"\n=== Directory Structure ===")
    for root, dirs, files in os.walk('.'):
        # Skip some directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', 'venv_new', 'staticfiles']]
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Show first 5 files per directory
            if not file.startswith('.') and not file.endswith('.pyc'):
                print(f"{subindent}{file}")
        if len(files) > 5:
            print(f"{subindent}... and {len(files) - 5} more files")

if __name__ == "__main__":
    list_project_files()
