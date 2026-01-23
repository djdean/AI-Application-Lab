"""
FastAPI Server Launcher
Starts the FastAPI server for any workshop task
"""

import sys
import subprocess
import os

def print_banner():
    print("=" * 60)
    print("FastAPI Workshop - Server Launcher")
    print("=" * 60)
    print()

def print_menu():
    print("Select which server to run:")
    print()
    print("  1. Task 1 - Basic FastAPI Setup")
    print("  2. Task 2 - Pydantic Models")
    print("  3. Task 3 - Lists and Global State")
    print("  4. Task 4 - Complex Data and Custom Responses")
    print("  5. Task 5 - CORS Middleware (Full Server)")
    print()
    print("  Q. Quit")
    print()

def start_server(task_number):
    """Start the FastAPI server for the specified task"""
    server_file = f"task_{task_number}_server:myapp"
    
    print(f"\nStarting Task {task_number} server...")
    print(f"Server will be available at: http://localhost:8000")
    print(f"API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 60)
    print()
    
    try:
        # Start uvicorn with reload enabled
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            server_file,
            "--reload",
            "--port", "8000",
            "--host", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except FileNotFoundError:
        print("\n❌ Error: uvicorn not found!")
        print("Please install it with: pip install uvicorn")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nMake sure you have uvicorn installed:")
        print("pip install uvicorn")

def main():
    print_banner()
    
    # Check if we're in the correct directory
    if not os.path.exists("task_1_server.py"):
        print("⚠️  Warning: Server files not found in current directory")
        print("Please run this script from the 'Build FastAPI Server' folder")
        print()
        input("Press Enter to exit...")
        return
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-5 or Q): ").strip().upper()
        
        if choice == 'Q':
            print("\nGoodbye!")
            break
        elif choice in ['1', '2', '3', '4', '5']:
            start_server(choice)
            print("\n")
        else:
            print("\n❌ Invalid choice. Please enter 1-5 or Q.")
            print()

if __name__ == "__main__":
    main()
