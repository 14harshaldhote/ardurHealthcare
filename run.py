# ardurHealthcare/run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Ensure debug is False in production environments
    app.run(debug=True)