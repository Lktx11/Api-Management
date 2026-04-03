from flask import Flask

app = Flask(__name__)

import routes.routes

app.run()