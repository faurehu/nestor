#!/usr/bin/env python
from nestor import create_app
from nestor.config import ENVIRONMENT

app = create_app()
debug = ENVIRONMENT == 'development'
app.run(host='0.0.0.0', debug=debug)
