from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from tables import Characters, Worlds, Base

app = Eve(validator=ValidatorSQL, data=SQL)

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()

# Insert some example data in the db
if not db.session.query(Characters).count():
    import nintendo_data
    for item in nintendo_data.character_data:
        db.session.add(Characters.from_tuple(item))
    db.session.commit()
if not db.session.query(Worlds).count():
    import nintendo_data
    for item in nintendo_data.world_data:
        db.session.add(Worlds.from_tuple(item))
    db.session.commit()

app.run(debug=True, use_reloader=False)