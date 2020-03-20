from flask_restful import Resource
from flask_restful_swagger import swagger

class Noop(Resource):
    """This endpoint does nothing =D"""
    @swagger.operation(
        notes='Basic uptime endpoint.  Only used to validate the application',
        nickname='get',
        parameters=[],
        responseMessages=[
            {
                'code': '200',
                'description': ''
            }
        ]
    )
    def get(self):
        return {"status": "OK"}
