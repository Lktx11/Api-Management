from flask import Flask
from flasgger import Swagger
from routes.routes import routes_bp
app = Flask(__name__)
app.register_blueprint(routes_bp)
swagger_template = {
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Digite seu token JWT"
        },
        "ApiKey": {
            "type": "apiKey",
            "name": "X-API-Key",
            "in": "header",
            "description": "Digite sua chave de API"
        }
    }
}
Swagger(app, template=swagger_template)
app.run(debug=True)


