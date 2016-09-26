from flask_restful import Resource
from flask_restful_swagger import swagger

class Noop(Resource):
    "This endpoint does nothing =D"
    @swagger.operation(
        notes='Not much to say',
        nickname='get',
        responseMessages=[
            {
                'code': '200',
                'description': 'The given city was found and the resulting matches were returned'
            }
        ]
    )
    def get(self):
        return {}
