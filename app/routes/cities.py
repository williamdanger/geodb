"""City-based routes"""
from datetime import datetime
from flask_restful import Resource, abort, reqparse
from flask_restful_swagger import swagger
from geoalchemy2.shape import to_shape
from shapely import wkb
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from db.city import City

neighborParser = reqparse.RequestParser()
neighborParser.add_argument('sameCountry', default=False, help='Limit results to the same country')
neighborParser.add_argument('limit', type=int, default=10, help='Number of results to return')
neighborParser.add_argument('offset', type=int, default=0, help='Number of results skip before returning data')

cityParser = reqparse.RequestParser()
cityParser.add_argument('query', default="", help='Query string for finding matching cities')

def asJson(city):
    return {
        'id': city.id,
        'name': city.name,
        'asciiName': city.asciiName,
        'alternateNames': city.alternateNames,
        'location': bytes(to_shape(city.location)),
        'featureClass': city.featureClass,
        'featureCode': city.featureCode,
        'countryCode': city.countryCode,
        'cc2': city.cc2,
        'admin1Code': city.admin1Code,
        'admin2Code': city.admin2Code,
        'admin3Code': city.admin3Code,
        'admin4Code': city.admin4Code,
        'population': city.population,
        'elevation': city.elevation,
        'dem': city.dem,
        'timezone': city.timezone,
        'modificationDate': city.modificationDate.isoformat(),
    }

class NeighborQuery(Resource):
    """Returns the nearest neighbors to a city, given the city's ID"""
    @swagger.operation(
        notes='Some notes',
        nickname='get',
        parameters=[
            {
                'name': 'cityId',
                'description': 'The ID of the city',
                'required': True,
                'paramType': 'path'
            }, {
                'name': 'sameCountry',
                'description': 'Limit the cities returned to be in the same country as the origin',
                'required': False,
                'dataType': 'boolean'
            }, {
                'name': 'limit',
                'description': 'Limit the cities to the given number.  Defaults to 10',
                'required': False,
                'dataType': 'integer'
            }, {
                'name': 'offset',
                'description': 'Skips the given number of cities to return.  Defaults to 0',
                'required': False,
                'dataType': 'integer'
            }
        ],
        responseMessages=[
            {
                'code': '200',
                'description': 'The given city was found and the resulting matches were returned'
            },
            {
                'code': '404',
                'description': 'The city ID was not found or invalid'
            }
        ]
    )
    def get(self, cityId):
        args = neighborParser.parse_args()
        origin = City.query.filter(City.id == cityId).first()
        if not origin:
            abort(404, message='City {} does not exist'.format(cityId))
        neighbors = City.query.filter(
                City.id != origin.id
            ).order_by(
                func.ST_Distance(City.location, origin.location)
            )
        if args['sameCountry']:
            neighbors = neighbors.filter(City.countryCode == origin.countryCode)
        neighbors = neighbors.limit(args['limit']).offset(args['offset'])
        return [asJson(n) for n in neighbors.all()]


class CityQuery(Resource):
    def get(self):
        args = cityParser.parse_args()
        origin = City.query.filter(City.id == cityId).first()
