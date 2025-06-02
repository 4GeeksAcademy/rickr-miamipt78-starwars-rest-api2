
import click
from api.models import db, User, Person, User_Person_Favorites

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
with youy database, for example: Import the price of bitcoin every night as 12am
"""
def setup_commands(app):
    
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("insert-users") # name of our command
    def insert_test_users():
        print("Creating users...")

        user_list = ['johndoe123', 'sammysmith456', 'mustangsally789']

        for x in range(0, len(user_list)):
            user = User()
            user.username = user_list[x]
            db.session.add(user)
            db.session.commit()
            print("User: ", user.username, " created.")

        print("All test users created")


    @app.cli.command("create-people")
    def insert_test_persons():
        person_name_list = ['Luke Skywalker', 'Darth Vader', 'C-3PO', 'Leah Organa', 'Obiwan Kenobi']
        person_hair_color = ['blonde', 'none', 'none', 'black', 'white']

        for x in range(0, len(person_name_list)):
            person = Person()
            person.name = person_name_list[x]
            person.hair_color = person_hair_color[x]
            db.session.add(person)
            db.session.commit()
            print("Person: ", person.name, " created.")

        print('All test people created')


    @app.cli.command("check-users")
    def check_users():
        all_users = db.session.scalars(db.select(User).order_by(User.id)).all()
        processed_users = [each_user.serialize() for each_user in all_users]
        print(processed_users)
    
    @app.cli.command("check-people")
    def check_people():
        all_people = db.session.scalars(db.select(Person).order_by(Person.id)).all()
        processed_people = [each_person.serialize() for each_person in all_people]
        print(processed_people)
    
    @app.cli.command("create-favorites")
    @click.argument('user_id')
    @click.argument('person_id')
    def create_favorites(user_id, person_id):
        user = db.session.get(User, user_id)
        person = db.session.get(Person, person_id)
        user.favorite_people.append(person)
        db.session.commit()

        print(f"User {user.username} has added {person.name} to their favorites.")
    
    @app.cli.command("check-user-faves")
    @click.argument('user_id')
    def get_user_favorites(user_id):
        user = db.session.get(User, user_id)
        all_people = [each_person.serialize() for each_person in user.favorite_people]
        print(all_people)
    

    @app.cli.command("check-fave-users")
    @click.argument('person_id')
    def get_favorited_by_user(person_id):
        person = db.session.get(Person, person_id)
        all_users = [each_user.serialize() for each_user in person.favorited_by_user]
        print(all_users)


