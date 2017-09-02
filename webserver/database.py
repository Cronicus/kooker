import pymongo
import re

from configs import HOSTNAME, PORT, GENERIC_USER, GENERIC_PASS

class DB_Exception(Exception):
    def __init__ (self, value):
        self.value = value
    def __str__ (self):
        return repr(self.value)
#----------------------------------------------------------------------------------------

class DB_Connector:
    # Class provides a connector object for read-only access to Kooker DB

    def __init__ (self):
        # Connect to database
        
        _db_client = pymongo.MongoClient(
                        'mongodb://%s:%s@%s:%s/kooker'%(
                        GENERIC_USER, GENERIC_PASS, HOSTNAME, PORT))
        
        self._db = _db_client["kooker"]

    def __exit__ (self):
        # Cleanup
        
        _db_client.close()
    
    # Get Methods ---------------------------------------------------------

    def get_recipe (self, name):
        # Get recipe by name
        
        units       = self._db.units
        recipes     = self._db.recipes
        quisines    = self._db.quisines
        ingredients = self._db.ingredients
        
        item_qty = []
        recipe = recipes.find_one({"name": name}, {"_id": 0})
        
        if not recipe:
            return {}
        
        matching_items = ingredients.find(
            {"_id": {"$in": recipe["items"]}}, 
            {"name": 1, "unit": 1})
        
        for item in matching_items:
            item_qty.append ({"name"     : item["name"], 
                              "quantity" : recipe["quantities"][
                                                recipe["items"].index(item["_id"])],
                              "unit"     : units.find_one({"_id": item["unit"]})["name"]})
        
        recipe["items"]   = item_qty
        recipe["quisine"] = quisines.find_one(
                                {"_id": recipe["quisine"]}, 
                                {"_id": 0, "name": 1})["name"]
        
        del recipe["quantities"]
        
        return recipe

    def get_ingredient (self, name):
        # Get ingredient by name
        
        ingredients = self._db.ingredients
        units = self._db.units
        
        ingredient = ingredients.find_one({"name": name}, {"_id": 0})
        
        if not ingredient:
            return {}
        
        ingredient["unit"] = units.find_one(
                                {"_id": ingredient["unit"]}, 
                                {"_id": 0, "name": 1})["name"]
        
        return ingredient

    def _get_ingredient_primary (self, name):
        # Get primary ingredient by name
        
        ingredients = self._db.ingredients
        ingredient = ingredients.find_one({"name": name})
        
        if not ingredient:
            return None
        
        aliases = self._db.aliases
        primary_item = aliases.find_one({"alias": ingredient["_id"]}, {"primary": 1})
        
        if not primary_item:
            return ingredient
        
        return ingredients.find_one({"_id": primary_item["_id"]})
    
    def get_unit (self, name):
        # Get unit by name
        
        units = self._db.units
        unit = units.find_one({"name": name}, {"_id": 0})
        
        return unit
    
    def get_quisine (self, name):
        # Get quisine by name
        
        quisines = self._db.quisines
        quisine = quisines.find_one({"name": name}, {"_id": 0})
        
        return quisine
    
    def _get_quisine (self, name):
        # Get quisine by name
        
        quisines = self._db.quisines
        return quisines.find_one({"name": name})
    
    # Search Methods ---------------------------------------------------------

    def search_recipe_by_name (self, string, quisine=None, only_veg=False):
        # Search recipe by name, quisine_type
        
        recipes = self._db.recipes
        
        # Regex for names starting with provided string
        search_params = {"name": re.compile("^"+string, re.IGNORECASE)}
        
        if (only_veg):
            search_params["veg"] = True
        
        if quisine:
            quisine_query_result = self._get_quisine(quisine)
            
            if not quisine_query_result:
                return []
            
            search_params["quisine"] = quisine_query_result["_id"]
        
        result = recipes.find(search_params, {"name": 1, "veg": 1, "time": 1, "_id": 0})
        
        return list(result)
    
    def search_recipe_by_ingredient (self, items=None, quisine=None, only_veg=False):
        # Search recipe by ingredients, quisine_type
        
        recipes = self._db.recipes
        item_ids = []
        search_params = dict({})
        
        # Verify item names and get item ids
        for item in items:
            primary_item = self._get_ingredient_primary(item)
            
            if not primary_item:
                return []
            
            item_ids.append (primary_item["_id"])
        
        if len(items) != 0:
            search_params["items"] = {"$all": item_ids}
        
        if only_veg:
            search_params["veg"] = True
        
        if quisine:
            quisine_query_result = self._get_quisine(quisine)
            
            if not quisine_query_result:
                return []
            
            search_params["quisine"] = quisine_query_result["_id"]
        
        result = recipes.find(search_params, {"name": 1, "veg": 1, "time": 1, "_id": 0})
        
        return list(result)

    def search_ingredient (self, string, only_veg=False):
        # Search ingredients by name
        
        ingredients = self._db.ingredients
        
        # Regex for names starting with provided string
        search_params = {"name": re.compile("^"+string, re.IGNORECASE)}
        
        if (only_veg):
            search_params["veg"] = True
        
        result = ingredients.find(search_params, {"name": 1, "_id": 0})
        
        return list(result)
    
    def search_unit (self, string):
        # Search units by name
        
        units = self._db.units
        
        # Regex for names starting with provided string
        regx = re.compile("^"+string, re.IGNORECASE)
        result = units.find({"name": regx}, {"name": 1, "_id": 0})
        
        return list(result)
        #return json.dumps(result)
    
    def search_quisine (self, string):
        # Search quisines by name
        
        quisines = self._db.quisines
        
        # Regex for names starting with provided string
        regx = re.compile("^"+string, re.IGNORECASE)
        result = quisines.find({"name": regx}, {"name": 1, "_id": 0})
        
        return list(result)

#----------------------------------------------------------------------------------------

class DB_AdminConnector(DB_Connector):
    # Class provides connector object for administrative read/write access to Kooker DB
    
    def __init__ (self, username, password):
        # Connect to database
        
        _db_client = pymongo.MongoClient(
                        'mongodb://%s:%s@%s:%s/kooker'%(
                        username, password, HOSTNAME, PORT))
        
        self._db = _db_client["kooker"]
    
    def __exit__ (self):
        # Cleanup
        
        _db_client.close()
    
    def _run_updgrade_script (self):
        pass
        #self._db.quisines.update({}, {"$rename":{"label": "name"}}, False, True);
        #self._db.units.update({}, {"$rename":{"label": "name"}}, False, True);
        
    def _init_db (self):
        # Initialize Database
        # This maynot be necessary as pymongo does it on the go 
        
        self._db.quisines
        self._db.recipes
        self._db.units
        self._db.ingredients
        self._db.aliases

    def _clear_db (self):
        # Clear Database
        
        self._db.quisines.drop()
        self._db.recipes.drop()
        self._db.units.drop()
        self._db.ingredients.drop()
        self._db.aliases.drop()

    def _sync_db (self):
        # Sync Database
        
        recipes = self._db.recipes
        aliases = self._db.aliases
        
        # Find recipes which have old primary item ids 
        # which now have become aliases andupdate them
        # using the alias table
        for alias in aliases.find():
            matching_recipes = recipes.find({"items": {"$all": [alias["_id"]]}}, {"items"})
            for recipe in matching_recipes:
                items = recipe["items"]
                items[items.index(alias["alias"])] = alias["primary"]
                recipes.update_one({"_id": recipe["_id"], "items": items})
        # Find a cleaner method
    
    # Recipe Methods --------------------------------------------------------

    def create_new_recipe (self, name, quisine, items, time, serves, steps):
        # Creates a new recipe

        recipes = self._db.recipes
        
        # Raise exception if recipe exists
        if recipes.find_one({"name": name}):
            raise DB_Exception ("Recipe " + str(name) + " exists!")
        
        ingredients = self._db.ingredients
        item_ids = []
        item_qts = []
        veg = True
        
        # Verify item names and get item ids
        for item, qty in items:
            primary_item =  self._get_ingredient_primary(item)
            if not primary_item:
                raise DB_Exception ("Ingredient " + str(item) + " not found!")
            
            item_ids.append (primary_item["_id"])
            item_qts.append (qty)
            
            if veg and not primary_item["veg"]:
                veg = False
        
        quisines = self._db.quisines
        
        # Verify quisine types and get quisine ids
        quisine_query_result =  quisines.find_one({"name": quisine})
        if not quisine_query_result:
            raise DB_Exception ("Quisine type " + str(quisine) + " not found!")
            quisine_ids.append (quisine_query_result["_id"])
        
        new_recipe = {
            "name"       : name,
            "quisine"    : quisine_query_result["_id"],
            "items"      : item_ids,
            "quantities" : item_qts,
            "time"       : time,
            "steps"      : steps,
            "veg"        : veg
        }
        
        recipes.insert_one(new_recipe)

    def modify_recipe (self, name, new_name, quisine, items, time, serves, steps):
        # Modifies a recipe
        
        recipes = self._db.recipes
        
        # Raise exception if recipe does not exists
        if not recipes.find_one({"name": name}):
            raise DB_Exception ("Recipe " + str(name) + " not found!")
        
        # Raise exception if recipe with same name already  exist
        if (new_name != name) and recipes.find_one({"name": new_name}):
            raise DB_Exception ("Recipe " + str(new_name) + " already exists!")
        
        ingredients = self._db.ingredients
        item_ids = []
        item_qts = []
        veg = True
        
        # Verify item names and get item ids
        for item, qty in items:
            primary_item =  self._get_ingredient_primary(item)
            if not primary_item:
                raise DB_Exception ("Ingredient " + str(item) + " not found!")
            
            item_ids.append (primary_item["_id"])
            item_qts.append (qty)
            
            if veg and not primary_item["veg"]:
                veg = False
        
        quisines = self._db.quisines
        
        # Verify quisine types and get quisine ids
        quisine_query_result =  quisines.find_one({"name": quisine})
        if not quisine_query_result:
            raise DB_Exception ("Quisine type " + str(quisine) + " not found!")
            quisine_ids.append (quisine_query_result["_id"])
        
        updated_recipe = {
            "name"       : new_name,
            "quisine"    : quisine_query_result["_id"],
            "items"      : item_ids,
            "quantities" : item_qts, 
            "time"       : time,
            "steps"      : steps,
            "veg"        : veg
        }
        
        recipes.update_one({"name": name}, updated_recipe)

    def delete_recipe (self, name):
        # Deletes a recipe
        
        recipes = self._db.recipes
        recipes.delete_one ({"name": name})

    # Ingredient Methods --------------------------------------------------------

    def create_new_ingredient (self, name, unit, veg):
        # Creates a new ingredient
        
        ingredients = self._db.ingredients
        
        # Raise exception if ingredient exists
        if ingredients.find_one({"name": name}):
            raise DB_Exception ("Ingredient " + str(name) + " exists!")
        
        units = self._db.units
        unit_query_result =  units.find_one({"name": unit})
        
        # Raise exception if unit type does not exist
        if not unit_query_result:
            raise DB_Exception ("Unit type " + str(unit) + " does not exist!")
        
        new_ingredient = {
            "name": name,
            "unit": unit_query_result["_id"],
            "veg" : veg
        }
        
        ingredients.insert_one(new_ingredient)

    def modify_ingredient (self, name, new_name, unit, veg):
        # Modifies an existing ingredient
        
        ingredients = self._db.ingredients
        
        # Raise exception if ingredient does not exist
        if not recipes.find_one({"name": name}):
            raise DB_Exception ("Ingredient " + str(name) + " exists!")
        
        # Raise exception if ingredient with same name already  exist
        if (new_name != name) and ingredients.find_one({"name": new_name}):
            raise DB_Exception ("Ingredient " + str(new_name) + " already exists!")
        
        units = self._db.units
        unit_query_result =  units.find_one({"name": unit})
        
        # Raise exception if unit type does not exist
        if unit_query_result:
            raise DB_Exception ("Unit type " + str(name) + " does not exist!")
        
        updated_ingredient = {
            "name": new_name,
            "unit": unit_query_result["_id"],
            "veg" : veg
        }
        
        ingredients.update_one({"name": name}, updated_ingredient)

    def delete_ingredient (self, name):
        # Deletes an ingredient and all recipe links
        
        ingredients = self._db.ingredients
        
        # Find ingredient with given name
        ingredient = ingredients.find_one({"name": name})
        
        if not ingredient:
            return
        
        aliases = self._db.aliases
        
        # If ingredient is an alias, delete alias only
        if aliases.find_one({"alias": ingredient["_id"]}):
            aliases.delete_one({"alias": ingredient["_id"]})
            return
        
        # Since ingredient is primary, delete all aliases
        aliases.delete_many({"primary": ingredient["_id"]})
        
        recipes = self._db.recipes
        
        # Modify recipes with primary ingredient
        modify_recipes = recipes.find_many({"items": {"$all": [ingredient["_id"]]}},{"items": 1})
        
        for recipe in modify_recipes:
            items = recipe["items"]
            items.remove(ingredient["_id"])
            recipes.update_one ({"_id": recipe["_id"]}, {"items": items})
        
        # Delete ingredient
        ingredients.delete_one ({"_id": ingredient["_id"]})

    def ingredient_alias (self, primary_name, alias_name, force=False):
        # Make an ingredient an alias to another
        
        if primary_name == alias_name:
            return
        
        ingredients = self._db.ingredients
        primary_query = ingredients.find_one({"name": primary_name})
        alias_query = ingredients.find_one({"name": alias_name})
        
        # Raise exception if either of the ingredients do not exist
        if not primary_query:
            raise DB_Exception ("Ingredient " + str(primary_name) + " does not exist!")
        if not alias_query:
            raise DB_Exception ("Ingredient " + str(alias_name) + " does not exist!")
        
        # Raise exception (in no force mode) when the unit types don't match
        if primary_query["unit"] != alias_query["unit"]:
            if not force:
                raise DB_Exception ("Units don't match for " + str(alias_name) + " and " + str(primary_name))
            # else raise a WARNING *TODO
        
        primary_id = primary_query["_id"]
        aliases = self._db.ingredient_aliases
        
        # If provided primary_name is an alias, get it's primary
        alias_check_query = aliases.find_one({"primary": primary_id})
        if alias_check_query:
            primary_id = alias_check_query["primary"]
        
        # Update alias if exists, else make new
        aliases.update_one({"alias": alias_query["_id"]}, {"alias": alias_query["_id"], "primary": primary_id}, upsert=True)    
        
        # Syncronize database alias links
        self._sync_db()

    def set_ingredient_primary (self, name):
        # Set ingredient as primary amongst aliases
        
        ingredients = self._db.ingredients
        item_query = ingredients.find_one({"name": name})
        
        # Raise exception if either of the ingredients do not exist
        if not item_query:
            raise DB_Exception ("Ingredient " + str(primary_name) + " does not exist!")
        
        item_id = item_query["_id"]
        aliases = self._db.ingredient_aliases
        
        # If provided primary_name is an alias, make it primary
        alias = aliases.find_one({"alias": item_id})
        
        if not alias:
            # Nothing to do
            return
            
        old_primary_id = alias["primary"]
        new_primary_id = alias["alias"]
        
        # Change old primary to an alias
        aliases.update_one({"primary": old_primary_id}, {"alias": old_primary_id, "primary": new_primary_id}, upsert=True)
        
        # Update all other aliases
        aliases.update_many({"primary": old_primary_id}, {"primary": new_primary_id})
        
        # Syncronize database alias links
        self._sync_db()

    # Unit Methods --------------------------------------------------------

    def create_new_unit (self, name):
        # Creates a new unit
        
        units = self._db.units
        
        # Raise exception if unit exists
        if units.find_one({"name": name}):
            raise DB_Exception ("Unit type " + str(name) + " exists!")
        
        units.insert_one({"name": name})

    def modify_units (self, name, new_name):
        # Modifies an existing unit
        
        units = self._db.units
        
        # Raise exception if unit does not exist
        if not units.find_one({"name": name}):
            raise DB_Exception ("Unit type " + str(name) + " does not exist!")
        
        # Raise exception if unit with same name already  exist
        if units.find_one({"name": new_name}):
            raise DB_Exception ("Unit type " + str(name) + " already exists!")
        
        units.update_one({"name": name}, {"name": new_name})

    def delete_unit (self, name):
        # Deletes a unit and all associated ingredients
        
        units = self._db.units
        ingredients = self._db.ingredients
        
        # Find unit with given name
        unit = units.find_one({"name": name},{})
        if (unit):
            # Find ingredient with given unit
            damned_ingredients = ingredients.find_many({"unit": unit["_id"]},{})
            for ingredient in damned_ingredients:
                ingredients.delete_one ({"_id": ingredient["_id"]})
        
        units.delete_one ({"unit": unit["_id"]})

    # Quisine Methods --------------------------------------------------------

    def create_new_quisine (self, name):
        # Creates a new quisine
        
        quisines = self._db.quisines
        
        # Raise exception if quisine exists
        if quisines.find_one({"name": name}):
            raise DB_Exception ("Quisine type " + str(name) + " exists!")
        
        quisines.insert_one({"name": name})

    def modify_quisines (self, name, new_name):
        # Modifies an existing quisine
        
        quisines = self._db.quisines
        
        # Raise exception if quisine does not exist
        if not quisines.find_one({"name": name}):
            raise DB_Exception ("Quisine type " + str(name) + " does not exist!")
        
        # Raise exception if quisine with same name already  exist
        if quisines.find_one({"name": new_name}):
            raise DB_Exception ("Quisine type " + str(name) + " already exists!")
        
        quisines.update_one({"name": name}, {"name": new_name})

    def delete_quisine (self, name):
        # Deletes a quisine and all associated recipes
        
        quisines = self._db.quisines
        recipes = self._db.recipes
        
        # Find quisine with given name
        quisine = quisines.find_one({"name": name},{})
        if (quisine):
            # Find recipe with given quisine
            damned_recipes = recipes.find_many({"quisine": quisine["_id"]},{})
            for recipe in damned_recipes:
                recipes.delete_one ({"_id": recipe["_id"]})
        
        quisines.delete_one ({"quisine": quisine["_id"]})

