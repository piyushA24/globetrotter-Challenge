#!/bin/bash
echo "Seeding data into postgress..."
python -m app.services.data_loader
echo "Starting uvicorn..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
