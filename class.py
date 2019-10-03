    class PDF(FPDF):
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)

            # Arial italic 8
            self.set_font('Arial', 'I', 8)

            # Text color in gray
            self.set_text_color(128)

            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

        def create_header(self, label, num=0):
            # Arial 12
            self.set_font('Arial', '', 14)

            # Calculate width of header and position
            w = self.get_string_width(label) + 6
            self.set_x(10)

            # Background color
            # self.set_fill_color(200, 220, 255)

            # Title
            if num == 0:
                self.cell(
                    w, 6, label, border='B', ln=1
                )
            else:
                self.cell(
                    w, 6, '%d. %s' % (num, label), border='B', ln=1
                )

            # Line break
            self.ln(4)

        def create_paragraph(self, p_text, d=''):
            # Read text file
            txt = p_text

            # Times 12
            self.set_font('Times', d, 12)

            # Output justified text
            self.multi_cell(0, 5, txt)

            # Line break
            self.ln()

            # Mention in italics
            self.set_font('', 'I')
            self.cell(0, 5, '(end of excerpt)')

        def print_chapter(self, num, title, name):
            self.add_page()
            self.chapter_title(num, title)
            self.chapter_body(name)
