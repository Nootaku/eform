# PDF Creation module
from fpdf import FPDF, HTMLMixin

# PROJECT FUNCTIONS
from functions.contract import intermediary, player, contract


# First, let's connect to the database:
def generatePdf(company, form_values, destination):
    """Generates a PDF document. Uses the Logged in user name in order to get
    the company data.

    Arguments:
            - company: The company linked to the ID of the logged in user.
            - form_values: Array of form values organized in the following way
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
            - destination: path to the Downloads folder of the user

    Output:
            - success: Boolean determining if the PDF has been generated.

    Extra information:
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
    """
    # Define variables:
    # ----------------------
    intermediary_paragraph = intermediary(company)
    player_paragraph = player(form_values)
    contract_text = contract(company, form_values)

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
            for key in contract_text:
                if key == "signatures":
                    for p in contract_text[key]:
                        if p == contract_text[key][0]:
                            self.ln(5)
                            self.set_font('Arial', size=11)
                            self.multi_cell(0, h=5, txt=p, align='L')
                            self.ln(5)
                        elif (
                            p == contract_text[key][1] or
                            p == contract_text[key][3]
                        ):
                            self.set_font('Arial', size=12)
                            self.multi_cell(0, h=5, txt=p, align='L')
                            self.ln(5)
                        else:
                            self.set_font('Arial', size=11)
                            self.multi_cell(0, h=5, txt=p, align='L')
                            self.cell(0, h=30, ln=2)
                else:
                    self.set_font('Arial', 'B', size=14)
                    self.cell(0, h=5, txt=key, ln=1)
                    self.ln(5)
                    for p in contract_text[key]:
                        p_index = contract_text[key].index(p) + 1
                        if p_index == len(contract_text[key]):
                            self.set_font('Arial', size=11)
                            self.multi_cell(0, h=5, txt=p, align='L')
                            self.ln(10)
                        else:
                            self.set_font('Arial', size=11)
                            self.multi_cell(0, h=5, txt=p, align='L')
                            self.ln(5)

    pdf = MyFPDF()

    # Generate PDF
    pdf.add_page()
    pdf.create_title('Intermediary Agreement')
    pdf.create_header('INTERMEDIARY')
    pdf.user_paragraph(intermediary_paragraph, "Indermediary")
    pdf.set_font('Arial', 'B', size=12)
    pdf.cell(0, txt="And", ln=1)
    pdf.ln(8)
    pdf.create_header('PLAYER')
    pdf.user_paragraph(player_paragraph, "Player")
    pdf.set_font('Arial', size=11)
    pdf.cell(
        0, h=5,
        txt="have agreed to inter into an intermediary agreement as follow :",
        ln=1
    )
    pdf.ln(15)
    pdf.write_contract()

    # SAVE FILE
    pdf.output(destination, 'F')
