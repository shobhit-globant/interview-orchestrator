"""
Script to create a new Alembic migration
Usage: python scripts/create_migration.py "migration message"
"""
import subprocess
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def create_migration(message: str):
    """Create a new Alembic migration"""
    try:
        # Change to project root directory
        os.chdir(project_root)
        
        # Run alembic revision command
        cmd = ["uv", "run", "alembic", "revision", "--autogenerate", "-m", message]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Migration created successfully: {message}")
            print(result.stdout)
        else:
            print(f"Error creating migration: {result.stderr}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_migration.py 'migration message'")
        sys.exit(1)
    
    message = sys.argv[1]
    success = create_migration(message)
    sys.exit(0 if success else 1)
