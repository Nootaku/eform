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


def contract(company, form):
    """Creates a dictionary of strings containing the values of the given form.

    Attributes:
            - form: LIST[with form values]

    Output:
            - contract_dict: DICT(key: value) where keys are headers and values
                        are paragraphs.
    """
    # FORM's checkbox management -- variables
    exclusivity = "non-exclusive"
    if form[6] == "on":
        exclusivity = str(
            "exclusive (on the territories mentioned in article 2) to the " +
            "Intermediary and the player understands that during the " +
            "Contract Period, he cannot make the same request to any other " +
            "intermediary."
        )
    lump = "The payment method will be a lump sum payment."
    by_club = str(
        "The Player authorizes the club to pay the Intermediary on his behalf."
    )

    # Initiate dictionary
    contract_dict = {
        "1. Contract Period": [
            str(
                "This contract shall enter into force on the {0}, " +
                "and be valid until the {1}."
            ).format(form[3], form[4])
        ],
        "2. Request and scope": [
            str(
                "The Player requests the Intermediary to handle " +
                "negotiations related to his transfer and his labour " +
                "contract with professional clubs in {0}."
            ).format(form[5])
        ],
        "3. Exclusivity": [
            str(
                "The Player's request to the Intermediary is {0}"
            ).format(exclusivity)
        ],
        "4. Remuneration": [
            str(
                "The Player will pay to the Intermediary remuneration in " +
                "the amount equivalent to {0}% of the total " +
                "gross income that the Player will receive from his club as " +
                "a result of the player contract negotiated by the " +
                "Intermediary for the Player."
            ).format(form[7])
        ],
        "5. Compulsory provision": [str(
            "The parties agree that they will comply with the statutes, " +
            "regulations, directives, and decisions of FIFA, " +
            "confederations, and associations, and the laws and ordinances " +
            "of any other countries where the player signs a labour contract."
        )],
        "signatures": [
            str(
                "Signed in 3 originals in {0} on {1},"
            ).format(form[10], form[11]),
            str("Intermediary: {0}").format(company.agent_name),
            str("Signature"),
            str("Player: {0}").format(form[0]),
            str("Signature")
        ]
    }

    if form[8] == "on":
        contract_dict["4. Remuneration"].append(lump)
    if form[9] == "on":
        contract_dict["4. Remuneration"].append(by_club)

    return contract_dict
