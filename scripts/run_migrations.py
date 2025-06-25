"""
Script to run Alembic migrations
"""
import subprocess
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_migrations():
    """Run Alembic migrations"""
    try:
        # Change to project root directory
        os.chdir(project_root)
        
        # Run alembic upgrade command
        cmd = ["uv", "run", "alembic", "upgrade", "head"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Migrations applied successfully!")
            print(result.stdout)
        else:
            print(f"Error running migrations: {result.stderr}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
