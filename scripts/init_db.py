"""
Database initialization script
Run this to create initial database tables and seed data
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from app.core.config import settings
from app.core.database import Base
from app.models import *  # Import all models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Create all database tables"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        raise

def seed_initial_data():
    """Seed initial data like user roles and skill categories"""
    try:
        from sqlalchemy.orm import sessionmaker
        from app.models.user import UserRole
        from app.models.candidate import SkillCategory, Skill
        from app.core.security import get_password_hash
        from app.models.user import User
        
        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        logger.info("Seeding initial data...")
        
        # Create default user roles
        roles = [
            {"name": "super_admin", "description": "Super administrator with full access"},
            {"name": "admin", "description": "Administrator with full company access"},
            {"name": "hr_manager", "description": "HR manager with recruitment access"},
            {"name": "interviewer", "description": "Interviewer with interview access"},
            {"name": "viewer", "description": "Read-only access to company data"}
        ]
        
        for role_data in roles:
            existing_role = db.query(UserRole).filter(UserRole.name == role_data["name"]).first()
            if not existing_role:
                role = UserRole(**role_data)
                db.add(role)
        
        # Create skill categories
        skill_categories = [
            {"name": "Programming Languages", "description": "Programming and scripting languages"},
            {"name": "Web Technologies", "description": "Web development technologies"},
            {"name": "Databases", "description": "Database systems and technologies"},
            {"name": "Cloud Platforms", "description": "Cloud computing platforms"},
            {"name": "DevOps Tools", "description": "Development and operations tools"},
            {"name": "Frameworks", "description": "Software frameworks and libraries"},
            {"name": "Mobile Development", "description": "Mobile application development"},
            {"name": "Data Science", "description": "Data science and analytics tools"},
            {"name": "AI/ML", "description": "Artificial Intelligence and Machine Learning"},
            {"name": "Project Management", "description": "Project management methodologies"}
        ]
        
        for category_data in skill_categories:
            existing_category = db.query(SkillCategory).filter(
                SkillCategory.name == category_data["name"]
            ).first()
            if not existing_category:
                category = SkillCategory(**category_data)
                db.add(category)
        
        db.commit()
        
        # Create some initial skills
        programming_category = db.query(SkillCategory).filter(
            SkillCategory.name == "Programming Languages"
        ).first()
        
        if programming_category:
            skills = [
                {"name": "Python", "category_id": programming_category.id},
                {"name": "JavaScript", "category_id": programming_category.id},
                {"name": "Java", "category_id": programming_category.id},
                {"name": "C++", "category_id": programming_category.id},
                {"name": "C#", "category_id": programming_category.id},
                {"name": "Ruby", "category_id": programming_category.id},
                {"name": "Go", "category_id": programming_category.id},
                {"name": "Rust", "category_id": programming_category.id},
                {"name": "TypeScript", "category_id": programming_category.id},
                {"name": "PHP", "category_id": programming_category.id}
            ]
            
            for skill_data in skills:
                existing_skill = db.query(Skill).filter(Skill.name == skill_data["name"]).first()
                if not existing_skill:
                    skill = Skill(**skill_data)
                    db.add(skill)
        
        # Create a default super admin user
        admin_email = "admin@intervieworchestrator.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            admin_user = User(
                email=admin_email,
                first_name="Super",
                last_name="Admin",
                username="superadmin",
                hashed_password=get_password_hash("admin123!"),
                is_superuser=True,
                is_verified=True
            )
            db.add(admin_user)
        
        db.commit()
        db.close()
        
        logger.info("Initial data seeded successfully!")
        
    except Exception as e:
        logger.error(f"Error seeding data: {str(e)}")
        raise

if __name__ == "__main__":
    create_database()
    seed_initial_data()
    logger.info("Database initialization completed!")
