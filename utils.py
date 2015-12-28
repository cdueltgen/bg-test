import os
from datetime import datetime

import boto3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica

S3_BUCKET = os.environ.get('S3_BUCKET')

def make_pdf():
    """Generate a pdf report."""
    d = datetime.utcnow()
    report_date = d.strftime("%Y%m%d%H%M%S")
    report_name = "report-" + report_date + ".pdf"
    pdf = canvas.Canvas(report_name, pagesize=letter)
    pdf.setFont("Courier", 50)
    pdf.setStrokeColorRGB(1, 0, 0)
    pdf.setFillColorRGB(1, 0, 0)
    pdf.drawCentredString(letter[0] / 2, inch * 7, 'FANCY REPORT')
    pdf.drawCentredString(letter[0] / 2, inch * 6, 'CLASSIFIED')
    pdf.drawCentredString(letter[0] / 2, inch * 5, 'For Your Eyes Only')
    pdf.setFont("Courier", 20)
    pdf.drawCentredString(letter[0] / 2, inch * 4, 'Created: ' + d.strftime("%B %d, %Y %H:%M:%S"))

    pdf.showPage()
    pdf.save()
    return report_name

def upload_queue(filename, file_contents):
    """Upload to s3 function for use with the worker queue."""
    # file_contents = f.read()

    s3 = boto3.resource('s3')
    s3.Bucket(S3_BUCKET).put_object(Key=filename, Body=file_contents)
    return
