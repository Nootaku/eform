import datetime

# PDF Creation module
from fpdf import FPDF, HTMLMixin

# PROJECT FUNCTIONS
from functions.models.replace import replaceInString as ris
from functions.models.contract import intermediary, player, contract


# First, let's connect to the database:
def generatePdf(
    database, company, user, form_values, destination
):
    """Generates a PDF document. Uses the Logged in user name in order to get
    the company data.

    Arguments:
            - user: User name of the logged in user.
            - form_values: Array of values organized in the following way
                    0. request.form['name'],
                    1. request.form['dateOfBirth'],
                    2. request.form['passport'],
                    3. request.form['startDate'],
                    4. request.form['endDate'], ok
                    5. request.form['country'],
                    6. request.form['exclusive'],
                    7. request.form['remunaration'],
                    8. request.form['lump'],
                    9. request.form['byClub'],
                    10. request.form['signCity'],
                    11. request.form['date']

    Output:
            - success: Boolean determining if the PDF has been generated.

    Extra information:
        fpdf.cell(
            w, --> Cell width. If 0, the cell extends up to the right margin.
            h = 0, --> Cell height
            txt = '', --> String to print
            border = 0, --> 0 / 1: (no) border | L / R / T / B: left, right...
            ln = 0, -->  where to go after the call: 1 = next line, 2 = Below
            align = '', --> L || C || R
            fill = False, --> background must be painted or transparent
            link = '' --> URL or identifier returned by add_link()
        )

        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
    """
    # Define variables:
    # ----------------------
    intermediary_paragraph = intermediary(company)
    player_paragraph = player(form_values)
    exclusivity = "non-exclusive."
    lump = None
    byClub = None
    if form_values[6] == "on":
        exclusivity = str(
            "exclusive (on the territories mentioned in article 2) to the " +
            "Intermediary and the player understands that during the " +
            "Contract Period, he cannot make the same request to any other " +
            "intermediary."
        )
    if form_values[8] == "on":
        lump = "The payment method will be a lump sum payment."
    if form_values[9] == "on":
        byClub = str(
            "The Player authorizes the club to pay the Intermediary on his " +
            "behalf."
        )

    dates = [form_values[1], form_values[3], form_values[4], form_values[11]]
    for i in range(len(dates)):
        try:
            d = datetime.datetime.strptime(dates[i], "%Y-%m-%d")
            day = d.day
            month = d.month
            year = d.year
            dates[i] = str(day) + "/" + str(month) + "/" + str(year)
            print(dates[i])
        except Exception as ex:
            print(str(ex))

    replacements = [
        ["${player_name}$", form_values[0]],
        ["${date_of_birth}$", dates[0]],
        ["${passport}$", form_values[2]],  # 10
        ["${start_date}$", dates[1]],
        ["${end_date}$", dates[2]],
        ["${contract_country}$", form_values[5]],
        ["${exclusivity}$", exclusivity],
        ["${remuneration}$", form_values[7]],  # 15
        ["${lump}$", lump],  # 16
        ["${by_club}$", byClub],  # 17
        ["${sign_city}$", form_values[10]],  # 18
        ["${sign_date}$", dates[3]],
        ["\u2018", "'"],
        ["\u2019", "'"]
    ]

    class MyFPDF(FPDF, HTMLMixin):
        def header(self):
            # Line break
            self.ln(10)

        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Text color in gray
            self.set_text_color(128)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

        def create_title(self, text):
            self.set_font('Arial', 'B', 20)
            self.cell(
                0, h=15, txt=text, border=1, ln=2, align='C'
            )
            self.ln(15)

        def create_header(self, text):
            self.set_font('Arial', size=16)
            self.cell(10)  # move next cell 10mm to the right
            w = self.get_string_width(text) + 2
            self.cell(w, h=5, txt=text, border='B', ln=1)
            self.ln(5)

        def user_paragraph(self, paragraph, aka=""):
            self.set_font('Arial', size=11)

            self.write_html(paragraph)
            self.ln(8)

            if aka != "":
                self.set_font('Arial', 'I', size=11)
                self.cell(10)  # move next cell 10mm to the right
                hia = "(hereinafter « The " + aka + " »)"
                self.cell(0, txt=hia, ln=1)
                self.ln(8)

        def write_contract(self):
            for i in contract:
                text = contract[i]
                for j in replacements:
                    if text is not None:
                        text = ris(text, j[0], j[1])

                if text is not None:
                    if i.startswith("h"):
                        self.set_font('Arial', 'B', size=14)
                        self.cell(0, h=5, txt=text, ln=1)
                        self.ln(5)
                    elif i.startswith("m"):
                        self.set_font('Arial', size=11)
                        self.multi_cell(0, h=5, txt=text, align='L')
                        self.ln(5)
                    elif i.startswith("s"):
                        self.ln(5)
                        self.set_font('Arial', size=11)
                        self.multi_cell(0, h=5, txt=text, align='L')
                        self.ln(5)
                    elif i.startswith("n"):
                        self.set_font('Arial', size=12)
                        self.multi_cell(0, h=5, txt=text, align='L')
                        self.ln(5)
                    elif i.startswith("sig"):
                        self.set_font('Arial', size=11)
                        self.multi_cell(0, h=5, txt=text, align='L')
                        self.cell(0, h=30, ln=2)
                    else:
                        self.set_font('Arial', size=11)
                        self.multi_cell(0, h=5, txt=text, align='L')
                        self.ln(10)

    pdf = MyFPDF()

    # Generate PDF:
    # ----------------------
    pdf.add_page()

    # Title
    pdf.create_title('Intermediary Agreement')

    # Header 1
    pdf.create_header('INTERMEDIARY')

    # Intermediary
    pdf.user_paragraph(intermediary_paragraph, "Indermediary")

    # And
    pdf.set_font('Arial', 'B', size=12)
    pdf.cell(0, txt="And", ln=1)
    pdf.ln(8)

    pdf.create_header('PLAYER')

    # Player
    pdf.user_paragraph(player_paragraph, "Player")
    pdf.set_font('Arial', size=11)
    pdf.cell(
        0, h=5,
        txt="have agreed to inter into an intermediary agreement as follow :",
        ln=1
    )
    pdf.ln(15)

    # Contract
    pdf.write_contract()

    pdf.output(destination, 'F')
