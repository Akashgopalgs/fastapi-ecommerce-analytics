# FastAPI Ecommerce Analytics

A simple ecommerce analytics project built with **FastAPI** (backend, PostgreSQL database) and **Streamlit** (frontend dashboard).

## Features
- Upload product & customer data into PostgreSQL
- Browse products with filters (price, category, etc.)
- Customer analytics (most orders, top locations)
- Interactive dashboard with charts and graphs

## Tech Stack
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Streamlit
- Pandas

## Setup
```bash
git clone https://github.com/Akashgopalgs/fastapi-ecommerce-analytics.git
cd fastapi-ecommerce-analytics
pip install -r requirements.txt
uvicorn main:app --reload
streamlit run dashboard.py
