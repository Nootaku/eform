def intermediary(company):
    """Creates an HTML string with info related to the given company.

    Attributes:
            - company: SQLAlchemy Query Response object

    Output:
            - string: STR() containing html tags to be used with
                    the fpdf.write_html() function.
    """
    string = str(
        "<p><B><I>{0}</B></I>, registered in {1} under the VAT number {2} " +
        "and having its registered office located [<I>{3} - {4}, {1}$</I>] " +
        "and registered intermediary at the {5} Football Federation under " +
        "n° {6}, represented by <B>{7}</B>, Director,</p>"
    ).format(
        company.name, company.country, company.vat_nr, company.street,
        company.city, company.agent_country, company.agent_nr,
        company.agent_name
    )
    return string


def player(form):
    """Creates an HTML string with info related to the given form values.

    Attributes:
            - form: LIST[with form values]

    Output:
            - string: STR() containing html tags to be used with
                    the fpdf.write_html() function.
    """
    string = str(
        "<p><B><I>{0}</B></I>, born on {1}, in possession of passport " +
        "number {2},</p>"
    ).format(form[0], form[1], form[2])
    return string


contract = {
    "1. Contract Period":
    "h1": "1. Contract Period",
    "p1": str(
        "This contract shall enter into force on the ${start_date}$, and be " +
        "valid until the ${end_date}$."
    ),
    "h2": "2. Request and scope",
    "p2": str(
        "The Player requests the Intermediary to handle negotiations " +
        "related to his transfer and his labour contract with professional " +
        "clubs in ${contract_country}$."
    ),
    "h3": "3. Exclusivity",
    "p3": str(
        "The Player's request to the Intermediary is ${exclusivity}$"
    ),
    "h4": "4. Remuneration",
    "m4": str(
        "The Player will pay to the Intermediary remuneration in the amount " +
        "equivalent to ${remuneration}$% of the total gross income that the " +
        "Player will receive from his club as a result of the player " +
        "contract negotiated by the Intermediary for the Player."
    ),
    "m5": "${lump}$",
    "p6": "${by_club}$",
    "h5": "5. Compulsory provision",
    "p7": str(
        "The parties agree that they will comply with the statutes, " +
        "regulations, directives, and decisions of FIFA, confederations, " +
        "and associations, and the laws and ordinances of any other " +
        "countries where the player signs a labour contract."
    ),
    "s8": "Signed in 3 originals in ${sign_city}$ on ${sign_date}$,",
    "n9": "Intermediary: ${agent_name}$",
    "sig1": "Signature",
    "n10": "Player: ${player_name}$",
    "sig2": "Signature",
}
