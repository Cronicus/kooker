from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

import database as db

app = Flask(__name__)
api = Api(app)

def error():
    abort(404, message="Invalid command!")

parser = reqparse.RequestParser()
parser.add_argument('task')


class KookerPing(Resource):
    def get(self):
        return {"PING": "Welcome to Kooker DB"}

class KookerUser(Resource):
    def _parse_cmd(self, action, pieces):
        table = pieces[0]
        
        if action == "get":
            cmd, args = self._parse_cmd_get(table, pieces[1:])
            cmd = "get_" + cmd
   
        elif action == "search":
            cmd, args = self._parse_cmd_search(table, pieces[1:])
            cmd = "search_" + cmd
        
        else:
            error()
        
        return (cmd, args)

    def _parse_cmd_get(self, table, pieces):
        if table in ["recipe", "ingredient", "quisine", "unit"]:
            (cmd, args) = (table, self._parse_cmd_generic(pieces))
        
        else:
            error()
        
        return (cmd, args)
    
    def _parse_cmd_search(self, table, pieces):
        if table == "recipe":
            if (len(pieces) < 2):
                error()
            
            filter_type = pieces[0]
            (cmd, args) = self._parse_cmd_search_recipe(filter_type, pieces[1:])
        
        elif table in ["ingredient", "quisine", "unit"]:
            (cmd, args) = (table, self._parse_cmd_generic(pieces))
        
        else:
            error()
        
        return (cmd, args)
    
    def _parse_cmd_search_recipe(self, filter_type, args):
        if (len(args) < 3):
            error()
        
        if (filter_type == "name"):
            cmd = "recipe_by_name"
            key_filter = args[0]
        
        elif (filter_type == "ingredient"):
            cmd = "recipe_by_ingredient"
            
            if (args[0] == ''):
                key_filter = []
            else:
                key_filter = args[0].split("+")
        
        else:
            error()
        
        quisine_filter = args[1]
        if (args[1] == ''):
            quisine_filter = None
        
        try:
            veg_only = bool(int(args[2]))
        except:
            veg_only = False
        
        return cmd, (key_filter, quisine_filter, veg_only)
    
    def _parse_cmd_generic(self, args):
        if (len(args) > 2):
            error()
        
        return (args)
    
    def _parse_and_execute(self, msg):
        pieces = msg.split("-")
        if (len(pieces) < 3):
            error()
        
        cmd, args = self._parse_cmd(pieces[0], pieces[1:])
        
        self._user = db.DB_Connector()
        
        func = getattr(self._user, cmd)
        print "CMD : ", func
        print "ARGS : ", args
        
        res = jsonify(func(*args))
        print "RES : ", res
        
        if (res):
            return res
        
        return jsonify([])
    
    def get(self, msg):
        return self._parse_and_execute(msg)

api.add_resource(KookerUser, '/kooker/<msg>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
