# String Analyzer Service

A lightweight RESTful API for analyzing string properties using in-memory storage.

## Features

-  FastAPI with automatic docs
-  In-memory array storage 
-  Complete string analysis
-  Natural language query processing
-  Docker support
-  Zero dependencies except FastAPI

### Local Development

1. **Clone and run:**
```bash
git clone https://github.com/nadduli/string-analyzer.git
cd string-analyzer

python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000