from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.db_tables import User
from db.db_tables import Company
from db.encryption import encryptPsw


def createUser(name, psw):
    """Inserts a new user in the users table of the users database.

    Arguments:
            - name: STR(username)
            - psw: STR(password)

    Output:
            - None
    """
    engine = create_engine('sqlite:///db/users.db', echo=True)

    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    user = User(name, encryptPsw(psw))
    session.add(user)

    # commit the record the database
    session.commit()


def createCompany(
    user_id, name, vat_nr, address, agent_name, agent_nr, agent_country
):
    """Inserts a new company in the company table of the users database.

    Arguments:
            - user_id: INT(foreign key => user.id)
            - name: STR(company name)
            - vat_nr: STR(companies.vat_nr)
            - address: LIST =>
                    [companies.street, companies.city, companies.country]
            - agent_name: STR(companies.agent)
            - agent_nr: STR(companies.agent_nr)
            - agent_country: STR(companies.agent_country)

    Output:
            - None
    """
    engine = create_engine('sqlite:///db/users.db', echo=True)

    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    comp = Company(
        user_id, name, vat_nr, address, agent_name, agent_nr, agent_country
    )
    session.add(comp)

    # commit the record the database
    session.commit()
