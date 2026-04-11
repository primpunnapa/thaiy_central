# ThaiY

# project description
The platform centralizes Thai Boys' Love (BL) series. The system focuses on delivering up-to-date streaming links, official media, and series metadata, ensuring fans can access information instantly during peak traffic hours (e.g., during series premieres).

# set up with Docker (recommended)
# 1. Navigate to project
cd thai-bl-central

# 2. Build and start everything
docker-compose up -d

# 3. Seed the database (wait 5 seconds for postgres to be ready)
docker-compose exec backend python seed.py

# 4. Check logs to make sure everything is running
docker-compose logs

# to stop everything
docker-compose down -v

## without Docker
# set up the backend
1. Create a virtual environment and activate it:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`
```
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Run the FastAPI server:
```bash
fastapi dev main.py
```
Documentation for FastAPI can be found at http://127.0.0.1:8000/docs

# set up the frontend
1. Navigate to the frontend directory:
```bash
cd frontend
```
2. Install the required packages:
```bash
npm install
```
3. Start the development server:
```bash
npm run dev
```