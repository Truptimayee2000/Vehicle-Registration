# Vehicle Registration Data Dashboard

This project is a web-based dashboard application to analyze and visualize vehicle registration data. It uses a Flask backend API with a PostgreSQL database, and a Streamlit frontend for interactive data visualization.

---

## Features

- REST API built with Flask to serve vehicle registration data.
- Data storage and ORM managed with SQLAlchemy and PostgreSQL.
- Cross-Origin Resource Sharing (CORS) enabled for API.
- Data processing and manipulation with Pandas.
- Interactive charts and visualizations with Streamlit and Altair.
- HTTP requests handled with the `requests` library.

---

## Requirements

- Python 3.7 or higher
- PostgreSQL database

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Truptimayee2000/Vehicle-Registration.git
cd Vehicle-Registration
```

2. Install Miniconda (if not already installed):

Download and install Miniconda from https://docs.conda.io/en/latest/miniconda.html according to your operating system.

3. Create a new Conda environment:

```bash
    conda create -n vehicle_dashboard python=3.9 -y
    
```
4. Activate the Conda environment:
```bash
    conda activate vehicle_dashboard
```
5. Install required packages:

```bash
    pip install -r requirements.txt
```
6. split terminal or open 2 prompt at a time 

7. Backend (Flask API)
```bash
    cd backend
    flask run
```
8. Frontend (Streamlit)
```bash
    cd frontend
    streamlit run dashboard.py       
```
