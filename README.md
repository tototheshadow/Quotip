# Quotip
 BANGKIT Capstone Project
 
 A safe place to share your days both good and bad. Quotip is where you can be yourself. Make notes about how your day in detail and see what recommendations are given to you! Quotip will give you a gift in the form of useful quotes and activities adjusting to the story that you tell about your day.

## Getting Started
Here are a few steps to get our system up and running in your local computer :
1. **Prequerities** :
    - Python `3.8.10 or above`
    - FastAPI `0.78.0`
    - Uvicorn
    - SQLModel `0.0.6`
    - Pymysql
    - SQLAlchemy `1.4.35`
    - passlib[bcrypt] 
    - xlrd `1.2.0`
    - numpy
    - Tensorflow

2. **Initial Setup** :
    - Clone our project [Github Repo](https://github.com/tototheshadow/Quotip)
    - Navigate to CC/backend_fix
    - Create Python virtual environment on the folder by using `python3 -m venv env`, and activate the environment running `activate.bat` file on the env file (for Windows)
    - Install the requirements `pip install -r requirements.txt`
    - Run the server with uvicorn `python3 -m uvicorn main:app --reload` (This is enough if you’re just running the API on your local machine)
    - Navigate to `127.0.0.1/docs` or `127.0.0.1/redoc` to see the documentation and test the endpoints.
