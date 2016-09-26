from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger

from db import base
from routes import cities, empty

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='1.0')

# SQLAlchemy session teardown
@app.teardown_appcontext
def shutdownSession(exception=None):
    base.dbSession.remove()

api.add_resource(empty.Noop, '/')
api.add_resource(cities.NeighborQuery, '/city/<int:cityId>/neighbor/')
api.add_resource(cities.CityQuery, '/city/')

if __name__ == '__main__':
    app.run(debug=True)
