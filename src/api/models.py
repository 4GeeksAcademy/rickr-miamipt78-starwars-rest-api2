from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


User_Person_Favorites = Table(
    'user_person_favorites',
    db.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('person_id', ForeignKey('person.id'), primary_key=True),
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    #relationships
    favorite_people: Mapped[list['Person']] = relationship(secondary=User_Person_Favorites, back_populates='favorited_by_user')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }


class Person(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=True)

    #relationships
    favorited_by_user: Mapped[list['User']] = relationship(secondary=User_Person_Favorites, back_populates='favorite_people')

    def __repr__(self):
        return '<Person {}>'.format(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
        }
    

