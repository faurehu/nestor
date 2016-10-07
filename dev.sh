#!/bin/bash
FLASK_ENVIRONMENT=dev
PYTHONPATH=. alembic upgrade head && python run.py
