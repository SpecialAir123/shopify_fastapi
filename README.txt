1. Clone the Repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name


2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate (For macOS/Linux)
venv\Scripts\activate (For windows)


3. Install Dependencies
pip install -r requirements.txt

4. Running the Application
uvicorn app:app --reload


5. API Documentation
FastAPI provides interactive API documentation out of the box.
Swagger UI: http://localhost:8000/docs

6. Run Tests
pytest tests/test_main.py