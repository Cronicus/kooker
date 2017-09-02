import database as db
import pprint

#admin = db.DB_Connector()
admin = db.DB_AdminConnector("topchef", "cookin")
#admin._run_updgrade_script()

#admin.create_new_recipe ("Mutta", "Indian", [["Butter", 4], ["Fish", 2]], 120, 2, "Mutte me jaa")
#admin.create_new_recipe ("Muth", "Indian", [["Butter", 0.3], ["Salt", 1]], 10, 1, "Pondy laga")

#for res in admin.search_recipe_by_name(''):
    #pprint.pprint (admin.get_recipe(res["name"]))

#for res in admin.search_recipe_by_name('M', quisine="Indian", only_veg=False):
    #pprint.pprint(res)

#for res in admin.search_recipe_by_ingredient("Fishery", quisine=None, only_veg=False):
    #pprint.pprint (admin.get_recipe(res["name"]))

#pprint.pprint(admin.get_ingredient('Salt'))
