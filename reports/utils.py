from django.template.loader import render_to_string
from django.conf import settings
import os
from datetime import datetime
import weasyprint
from io import BytesIO
from django.core.files.base import ContentFile

def generate_pdf_report(report):
    """Generate a PDF report from a Report instance."""
    
    # Get the test order and patient
    test_order = report.test_order
    patient = test_order.patient
    
    # Get test results
    results = test_order.results.all()
    
    # Prepare context for template
    context = {
        'report': report,
        'patient': patient,
        'results': results,
        'notes': report.notes,
    }
    
    # Render HTML template
    html_string = render_to_string('report_template.html', context)
    
    # Generate PDF
    pdf_file = BytesIO()
    weasyprint.HTML(string=html_string).write_pdf(pdf_file)
    
    # Save PDF to report model
    if report.pdf_report:
        # Delete old file if it exists
        if os.path.isfile(report.pdf_report.path):
            os.remove(report.pdf_report.path)
    
    # Create filename
    filename = f"report_{report.report_number}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Save the PDF to the model
    report.pdf_report.save(filename, ContentFile(pdf_file.getvalue()), save=True)
    
    return report.pdf_report.url