# KOOKER WEBSERVER

database.py : Library for accessing the mongoDB server
configs.py  : mongoDB server location and authentication
app.py      : Runs the webserver accepting http requests

# 1) Database Commands

# a) DB_Connector
    
    get_recipe     (name)   returns ---> {
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
    
    get_ingredient (name)   returns ---> {
                                "name"    : <ingredient-name>, 
                                "unit"    : <unit-name>, 
                                "veg"     : <is-veg => true(1) or false(0)>
                                }
    
    get_cuisine    (name)   returns ---> {
                                "name"    : <cuisine-name>
                                }
    
    get_unit       (name)   returns ---> {
                                "name"    : <unit-name>
                                }

    search_recipe_by_name (string, cuisine=None, only_veg=False)
        returns --->    {
                            "name"    : <recipe-name>, 
                            "veg"     : <is-veg => true(1) or false(0)>,
                            "time"    : <minutes>
                        }
    
    search_recipe_by_ingredient (items=None, cuisine=None, only_veg=False)
        returns --->    {
                            "name"    : <recipe-name>, 
                            "veg"     : <is-veg => true(1) or false(0)>,
                            "time"    : <minutes>
                        }
    
    search_ingredient (string, only_veg=False)
        returns --->    {
                            "name"    : <recipe-name>
                        }
    
    search_unit (string)
        returns --->    {
                            "name"    : <recipe-name>
                        }
