#!/bin/bash
PYTHONPATH=. alembic upgrade head && python run.py
