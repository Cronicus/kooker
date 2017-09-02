# KOOKER WEBSERVER

    app.py      ---> Runs the webserver accepting http requests
    configs.py  ---> mongoDB server location and user authentication
    database.py ---> Library for accessing the mongoDB server

# Database Commands

# a) DB_Connector
    
    get_recipe (name)
        URI     --->    http://192.168.0.110:5000/kooker/get-recipe-<string>
        returns --->    {
                            "name"    : <recipe-name>, 
                            "cuisine" : <cuisine-name>, 
                            "veg"     : <is-veg => true(1) or false(0)>,
                            "items"   : [{"name": <item1>, "quantity": <qty1>, "unit": <unit1>},
                                         {"name": <item2>, "quantity": <qty2>, "unit": <unit2>},
                                         {"name": <item3>, "quantity": <qty3>, "unit": <unit3>},
                                        ...]
                            "time"    : <minutes>,
                            "serves"  : <number-of-people>,
                            "steps"   : <text>
                        }
    
    get_ingredient (name)
        URI     --->    http://192.168.0.110:5000/kooker/get-ingredient-<string>
        returns --->    {
                            "name"    : <ingredient-name>, 
                            "unit"    : <unit-name>, 
                            "veg"     : <is-veg => true(1) or false(0)>
                        }
    
    get_cuisine (name)
        URI     --->    http://192.168.0.110:5000/kooker/get-cuisine-<string>
        returns --->    {
                            "name"    : <cuisine-name>
                        }
    
    get_unit (name)
        URI     --->    http://192.168.0.110:5000/kooker/get-unit-<string>
        returns --->    {
                            "name"    : <unit-name>
                        }

    search_recipe_by_name (string, cuisine=None, only_veg=False)
        URI     --->    http://192.168.0.110:5000/kooker/search-recipe-name-<string>-<cuisine=None>-<only_veg=False(0)>
        returns --->    {
                            "name"    : <recipe-name>, 
                            "veg"     : <is-veg => true(1) or false(0)>,
                            "time"    : <minutes>
                        }
    
    search_recipe_by_ingredient (items=None, cuisine=None, only_veg=False)
        URI     --->    http://192.168.0.110:5000/kooker/search-recipe-name-<item1>+<item2>+<item3>+...-<cuisine=None>-<only_veg=False(0)>
        returns --->    {
                            "name"    : <recipe-name>, 
                            "veg"     : <is-veg => true(1) or false(0)>,
                            "time"    : <minutes>
                        }
    
    search_ingredient (string, only_veg=False)
        URI     --->    http://192.168.0.110:5000/kooker/search-ingredient-<string>
        returns --->    {
                            "name"    : <recipe-name>
                        }
    
    search_unit (string)
        URI     --->    http://192.168.0.110:5000/kooker/search-unit-<string>
        returns --->    {
                            "name"    : <recipe-name>
                        }

# a) DB_AdminConnector
    
    create_new_recipe (name, cuisine, items, time, serves, steps)
    modify_recipe     (name, new_name, cuisine, items, time, serves, steps)
    delete_recipe     (name)
    
    create_new_ingredient (name, unit, veg)
    modify_ingredient     (name, new_name, unit, veg)
    delete_ingredient     (name)
    
    create_new_cuisine (name)
    modify_cuisines    (name, new_name)
    delete_cuisine     (name)
    
    create_new_unit (name)
    modify_units    (name, new_name)
    delete_unit     (name)
    
    ingredient_alias       (primary_name, alias_name, force=False)
    set_ingredient_primary (name)
    
    
