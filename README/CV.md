# 💼 CV module

## ⚙️ Setup

### 1. Install requirements

```pip install -r requirements.txt```

```ollama pull llama3:8b``` - or any other model you want to use

```ollama pull phi3:mini``` - or any other model you want to use for classification

### 2. Start docker

```docker compose up -d```

### 3. Create database and import migrations

```python alembic/setup_db.py```
