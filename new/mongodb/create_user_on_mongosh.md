ENter command to create a user

enter mongosh

and enter

``use admin``

``db.createUser({ user: "username", pwd: "password", roles: [{ role: "root", db: "admin" } ] })``

this gives right to the created user all right to every database
