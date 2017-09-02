# Setting up the users
#
# Open MongoDb shell on the terminal
# > mongo
#
# Switch to the kooker database
# >> use kooker
#
# Create the admin user
# >> db.createUser(
# >> {
# >>   user: "topchef",
# >>   pwd:  "cookin",
# >>   roles: [ { role: "readWrite", db: "kooker" }]
# >> }
# >> )
#
# Create the generic user
# >> db.createUser(
# >> {
# >>   user: "generic",
# >>   pwd:  "generic",
# >>   roles: [ { role: "read", db: "kooker" }]
# >> }
# >> )
# >> exit
#
# Now edit the mongodb configuration file as root
# > sudo nano /etc/mongod.conf
#
# Add these lines at the bottom to enable authentication
# > security:
# > 	authorization: enabled
#
# Now start the mongodb service
# You are done!

# Configuration options for kooker database

HOSTNAME = '127.0.0.1'
PORT     = '27017'

GENERIC_USER = "generic"
GENERIC_PASS = "generic"
