#! /usr/bin/env python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "pypdf==5.4.0",
# ]
# ///

import marimo

__generated_with = "0.11.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    input_file_widget = mo.ui.file_browser(filetypes=[".pdf",], initial_path=".", multiple=False)
    rotation_widget = mo.ui.slider(start=-360, stop=360, step=90, value=0, show_value=True)
    doit_button = mo.ui.run_button()
    mo.md(f"Set rotation angle: {rotation_widget}\nFile to rotate: {input_file_widget}\n{doit_button}")
    return doit_button, input_file_widget, rotation_widget


@app.cell(hide_code=True)
def _(Path, doit_button, mo, parse_args, rotate_pdf):
    # Define input and output file paths
    if mo.running_in_notebook():
        # wait for user to click button
        mo.stop(not doit_button.value)
    file_no = 0
    input_pdf, rotation_angle = parse_args()
    if input_pdf:
        input_pdf = Path(input_pdf)
        file_no += 1
        output_pdf = input_pdf.parent.joinpath(f"{input_pdf.stem}-rot_{rotation_angle}.pdf")
    
        assert rotation_angle % 90 == 0
    
        # Call the function to rotate the PDF
        rotate_pdf(input_pdf, output_pdf, rotation_angle)
        print(f"{file_no}: Rotated PDF saved as {output_pdf}")
    return file_no, input_pdf, output_pdf, rotation_angle


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from pathlib import Path
    return Path, mo


@app.cell(hide_code=True)
def _():
    from pypdf import PdfReader, PdfWriter

    def rotate_pdf(input_pdf_path, output_pdf_path, rotation_angle):

        # Create a PdfReader object to read the input PDF
        reader = PdfReader(input_pdf_path)

        # Create a PdfWriter object to write the rotated PDF
        writer = PdfWriter()

        # Loop through each page in the PDF
        for page in reader.pages:
            # Rotate the page by the specified angle
            page.rotate(rotation_angle)
            # Add the rotated page to the writer object
            writer.add_page(page)

        # Write the rotated pages to the output PDF file
        with open(output_pdf_path, 'wb') as output_pdf:
            writer.write(output_pdf)
    return PdfReader, PdfWriter, rotate_pdf


@app.cell(hide_code=True)
def _():
    import argparse
    parser = argparse.ArgumentParser(description="rotate all pages by supplied degrees")
    parser.add_argument("-r", "--rotation", type=int, default=90, help="Degrees to rotate")
    parser.add_argument("filename", help="Input file name")
    None
    return argparse, parser


@app.cell(hide_code=True)
def _(input_file_widget, mo, parser, rotation_widget):
    def parse_args():
        if mo.running_in_notebook():
            input_pdf = input_file_widget.value[0].path if len(input_file_widget.value) else None
            rotation = int(rotation_widget.value)
        else:
            args = parser.parse_args()
            input_pdf = args.filename
            rotation = args.rotation
        return input_pdf, rotation
    return (parse_args,)


if __name__ == "__main__":
    app.run()
