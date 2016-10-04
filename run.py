#!/usr/bin/env python
from nestor import create_app
from nestor.config import ENVIRONMENT, PORT

app = create_app()
debug = ENVIRONMENT == 'dev'
app.run(host='0.0.0.0', port=PORT, debug=debug)
