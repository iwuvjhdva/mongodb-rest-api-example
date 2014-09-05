import colander
from pymongo import MongoClient

from flask import Flask, request
from flask.json import jsonify
from flask.views import MethodView

from schemas import Item

db = MongoClient()['mongodb-eat-n-learn']


class InventoryView(MethodView):
    def get(self):
        data = db.inventory.find(fields={'_id': 0}).sort('item', 1)
        status = 200 if data else 204
        return jsonify(data=list(data)), status

    def post(self):
        response_params = {}
        data = request.get_json()
        try:
            clean_data = Item().deserialize(data)
        except colander.Invalid as e:
            reason, status = "Data validation error", 400
            response_params['errors'] = e.asdict()
        else:
            db.inventory.insert(clean_data)
            reason = "Inventory Item registered successfully"
            status = 201
        return jsonify(reason=reason, **response_params), status


app = Flask(__name__)
app.add_url_rule('/inventory/', view_func=InventoryView.as_view('inventory'))

if __name__ == "__main__":
    app.run(debug=True)
