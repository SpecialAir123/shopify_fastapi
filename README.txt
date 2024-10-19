1. Clone the Repository
git clone https://github.com/SpecialAir123/shopify_fastapi.git
cd your-repo-name


2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate (For macOS/Linux)
venv\Scripts\activate (For windows)


3. Install Dependencies
pip install -r requirements.txt

4. Copy the variables to the .env
SHOPIFY_ACCESS_TOKEN=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
SHOPIFY_SHOP_NAME=kangs-international

5. Running the Application
uvicorn app:app --reload


6. API Documentation
FastAPI provides interactive API documentation out of the box.
Swagger UI: http://localhost:8000/docs

7. Run Tests
pytest tests/test_main.py
