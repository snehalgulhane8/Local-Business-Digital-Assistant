# Local Business Digital Assistant

A FastAPI + HTML/CSS/JavaScript business analytics application built with the Olist Brazilian E-Commerce Public Dataset.

## Features

- Business KPI dashboard
- Monthly sales analysis
- Product/category analysis
- Top customer analysis
- Order status analysis
- Review analysis
- Delivery analysis
- Rule-based business recommendations
- Natural-language business questions
- Vercel deployment configuration

## Stack

- Python
- FastAPI
- Uvicorn
- Pandas
- NumPy
- HTML/CSS/JavaScript
- Chart.js
- Vercel

## Run locally on Windows PowerShell

From the project root:

```powershell
python -m venv venv
venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd backend
..\venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## Vercel

Push the project to GitHub and import the repository into Vercel. The included `vercel.json` configures the FastAPI entry point.

## Dataset

Olist Brazilian E-Commerce Public Dataset:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
