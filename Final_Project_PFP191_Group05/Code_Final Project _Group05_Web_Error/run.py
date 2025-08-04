"""
Main runner for Campus Event Management System
"""

import os
import sys

# Get the absolute path of the project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if __name__ == '__main__':
    try:
        from frontend.app import app
        
        print("🎉 Campus Event Management System")
        print("=" * 50)
        print("🌐 Server starting at: http://localhost:5000")
        print("📚 Documentation: Check README.md")
        print("👤 Demo accounts:")
        print("   Admin: admin / admin123")
        print("   Organizer: organizer1 / org123") 
        print("   Student: student1 / student123")
        print("=" * 50)
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        os.makedirs('data/reports', exist_ok=True)
        
        # Run the Flask app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            threaded=True
        )
    except ImportError as e:
        print(f"Import Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're running from the project root directory")
        print("2. Install required packages: pip install -r requirements.txt")
        print("3. Check that all files are in the correct locations")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)