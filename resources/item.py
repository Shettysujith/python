from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
from models.item import ItemModel

class Item (Resource):
    parser= reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be empty"
        )
    parser.add_argument('store_id',
            type=int,
            required=True,
            help="Every item needs a store id"
        )
    @jwt_required()
    def get(self, name):
        item= ItemModel.find_by_name(name) 
        if item:
            return item.json()
        return {'message': "Item not found"},404
        
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An Item with name '{}' already exists.".format(name)}, 400
        
        data=Item.parser.parse_args()
    
        # data=request.get_json(silent=True)#force=True
        
        item=ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {'message': "An Error Occurred inserting the item."}, 500 #internal server error
        
        return item.json(), 201
    
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return{'message':'Item deleted'}

    def put(self,name):
        data=Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item= ItemModel(name,data['price'])
        if item is None:
            item=ItemModel(name, **data)
        else:
            item.price= data['price']
            # try:
            #     updated_item.update()
            # except:
            #     return {'message':"An error occured updating the item."},500
        return item.json()


class Itemlist(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
            # [item.json() for item in ItemModel.query.all()]