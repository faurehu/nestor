#!/bin/bash
export FLASK_ENVIRONMENT=dev
PYTHONPATH=. alembic upgrade head && python run.py
