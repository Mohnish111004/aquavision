"""
Create admin user for AquaVision AI
Run this script to create the default admin account
"""
from database import db
from database.models import User
from app import app

def create_admin():
    """Create admin user if it doesn't exist"""
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("⚠️  Admin user already exists")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Role: {admin.role}")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@aquavision.ai',
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        
        try:
            db.session.add(admin)
            db.session.commit()
            
            print("=" * 60)
            print("✅ Admin user created successfully!")
            print("=" * 60)
            print("\nLogin Credentials:")
            print(f"  Username: admin")
            print(f"  Email: admin@aquavision.ai")
            print(f"  Password: admin123")
            print("\n⚠️  IMPORTANT: Change the password after first login!")
            print("=" * 60)
        
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin user: {str(e)}")

if __name__ == "__main__":
    create_admin()
