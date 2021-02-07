from flask import Flask
from flask_restx import Resource, Api, reqparse
from circlek_crawler.circlek_crawler import CirclekCrawler

app = Flask(__name__)
api = Api(app, version='1.0', title="CircleK Gas API", doc="/swagger")
ns = api.namespace("circlek")

circlek_gas = CirclekCrawler("https://www.circlek.se/drivmedelspriser")


@ns.route('/price/<string:product_num>')
class Price(Resource):
    @ns.doc("test")
    def get(self, product_num):
        circlek_gas.crawler_prices()
        parser = reqparse.RequestParser()
        args = parser.parse_args()
        try:
            price = list(filter(lambda x: x["product"] == product_num, circlek_gas.prices))[0]
            return price
        except IndexError:
            return None


@ns.route('/prices')
class Prices(Resource):
    def get(self):
        circlek_gas.crawler_prices()
        return circlek_gas.prices


# @api.route()
class Test(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        args = parser.parse_args()
        return 'hello world'


ns.add_resource(Test, "/test")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
