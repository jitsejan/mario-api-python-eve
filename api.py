from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from tables import Character, Powerup, Base

app = Eve(validator=ValidatorSQL, data=SQL)

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()

    if not instance:
        instance = model(**kwargs)
        session.add(instance)

    return instance

star_power = get_or_create(db.session, Powerup, name='Star')
flower_power = get_or_create(db.session, Powerup, name="Fire Flower")
mushroom_power = get_or_create(db.session, Powerup, name='Mushroom')

mario = Character('Mario', 'This is Mario')
mario.powerups = [star_power, mushroom_power]
db.session.add(mario)

luigi = Character('Luigi', 'This is Luiigi')
luigi.powerups = [flower_power, mushroom_power]
db.session.add(luigi)

db.session.commit()


app.run(debug=True, use_reloader=False)

characters = db.session.query(Character).all()
print characters[0].powerups[0].name