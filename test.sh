#!/bin/bash
export FLASK_ENVIRONMENT=test
PYTHONPATH=. alembic upgrade head && nosetests tests/ --nocapture
