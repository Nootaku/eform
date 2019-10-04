from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///db/users.db', echo=True)
# Allows us to use a template over multiple tables & DBs
Base = declarative_base()


# Creating the User template:
class User(Base):
    # Define the table in which it should be placed
    __tablename__ = "users"

    # Define the columns of a user (and thus of the table)
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String, unique=True)
    password = Column("password", String)

    # Define an __init__ function to make the call to the User class easier
    def __init__(self, name, psw):
        self.username = name
        self.password = psw


# Creating a Company template
class Company(Base):
    # Define the tablename in which it should be placed
    __tablename__ = "companies"

    # Define the columns present in the Company class (and thus the table)
    id = Column("id", Integer, primary_key=True)
    user_id = Column("userid", String, ForeignKey("users.id"))
    name = Column("name", String)
    vat_nr = Column("vat_nr", String)
    street = Column("street", String)
    city = Column("city", String)
    country = Column("country", String)
    agent_name = Column("agent_name", String)
    agent_nr = Column("agent_nr", String)
    agent_country = Column("agent_country", String)

    # Define an __init__ function to make the call to the User class easier
    def __init__(
        self, user, name, vat, address, agent, agent_nr, agent_country
    ):
        """
        Arguments :
                - user:     INT(users.id)
                - name:     STR(companies.name)
                - vat:      STR(companies.vat_nr)
                - address:  LIST =>
                        [companies.street, companies.city, companies.country]
                - agent:    STR(companies.agent)
                - agent_nr: STR(companies.agent_nr)
                - agent_country: STR(companies.agent_country)
        """
        self.user_id = user
        self.name = name
        self.vat_nr = vat
        self.street = address[0]
        self.city = address[1]
        self.country = address[2]
        self.agent_name = agent
        self.agent_nr = agent_nr
        self.agent_country = agent_country


# create tables
Base.metadata.create_all(engine)
