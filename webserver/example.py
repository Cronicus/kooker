import database as db
import pprint

admin = db.DB_AdminConnector("topchef", "cookin")

#admin._clear_db()

#admin.create_new_unit ("kg")
#admin.create_new_unit ("gm")
#admin.create_new_unit ("pcs")
#admin.create_new_unit ("mL")

#admin.create_new_ingredient ("Potato", "kg", True)
#admin.create_new_ingredient ("Egg", "pcs", False)
#admin.create_new_ingredient ("Butter", "gm", True)
#admin.create_new_ingredient ("Cheese", "gm", True)
#admin.create_new_ingredient ("Chicken", "kg", False)
#admin.create_new_ingredient ("Mustard Oil", "mL", True)
#admin.create_new_ingredient ("Olive Oil", "mL", True)

#admin.create_new_cuisine ("Indian")
#admin.create_new_cuisine ("Italian")
#admin.create_new_cuisine ("American")
#admin.create_new_cuisine ("British")
#admin.create_new_cuisine ("Mexican")

#admin.create_new_recipe ("Omlette", "British", 
                         #[["Egg", 2], ["Butter", 10]], 5, 1, "To be added")

#admin.create_new_recipe ("Scrambled Eggs", "British", 
                         #[["Egg", 2], ["Butter", 10]], 10, 1, "To be added")

#admin.create_new_recipe ("French Fries", "Indian", 
                         #[["Potato", 2], ["Olive Oil", 50]], 10, 1, "To be added")

#admin.create_new_recipe ("Chicken Cheese Potato", "Indian", 
                         #[["Potato", 2], ["Chicken", 1], ["Cheese", 50]], 10, 1, "To be added")

#admin.create_new_recipe ("Cheesey Potato", "Indian", 
                         #[["Potato", 2], ["Cheese", 50]], 10, 1, "To be added")

print "Units : "
for res in admin.search_unit(""):
    #pprint.pprint (res)
    pprint.pprint (admin.get_unit(res["name"]))

print "Ingredients : "
for res in admin.search_ingredient(""):
    #pprint.pprint(res)
    pprint.pprint (admin.get_ingredient(res["name"]))

print "Cuisines : "
for res in admin.search_cuisine(""):
    #pprint.pprint (res)
    pprint.pprint (admin.get_cuisine(res["name"]))

print "Recipes : "
for res in admin.search_recipe_by_name("C"):
    #pprint.pprint (res)
    pprint.pprint (admin.get_recipe(res["name"]))
