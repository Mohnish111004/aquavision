"""
PDF Report Generation for Water Availability Predictions
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io

def generate_prediction_report(prediction_data, user_info=None):
    """
    Generate PDF report for a water availability prediction
    
    Args:
        prediction_data: Dictionary containing prediction details
        user_info: Optional user information
    
    Returns:
        BytesIO buffer containing PDF data
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#374151'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    
    # ── Header ────────────────────────────────────────────────────────────────
    elements.append(Paragraph("AquaVision AI", title_style))
    elements.append(Paragraph("Water Availability Prediction Report", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    elements.append(Paragraph(f"<b>Report Generated:</b> {report_date}", normal_style))
    
    if user_info:
        elements.append(Paragraph(f"<b>Generated for:</b> {user_info.get('full_name', user_info.get('username', 'User'))}", normal_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # ── Prediction Summary ────────────────────────────────────────────────────
    elements.append(Paragraph("Prediction Summary", heading_style))
    
    prediction = prediction_data.get('prediction', 'N/A')
    confidence = prediction_data.get('confidence', 0)
    
    # Color-coded prediction result
    pred_color = {
        'High': colors.green,
        'Medium': colors.orange,
        'Low': colors.red
    }.get(prediction, colors.grey)
    
    prediction_table = Table([
        ['Water Availability Level', Paragraph(f"<b>{prediction}</b>", normal_style)],
        ['Confidence Score', f"{confidence:.2f}%"],
        ['Current Status', prediction_data.get('current_status', 'N/A')],
        ['Risk Level', prediction_data.get('risk_level', 'N/A')]
    ], colWidths=[2.5*inch, 3.5*inch])
    
    prediction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (1, 0), (1, 0), pred_color),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.white),
    ]))
    
    elements.append(prediction_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ── Input Parameters ──────────────────────────────────────────────────────
    elements.append(Paragraph("Input Parameters", heading_style))
    
    input_data = [
        ['Parameter', 'Value'],
        ['Latitude', f"{prediction_data.get('latitude', 'N/A')}"],
        ['Longitude', f"{prediction_data.get('longitude', 'N/A')}"],
        ['Current Water Level', f"{prediction_data.get('currentlevel', 'N/A')} m"],
        ['Level Difference', f"{prediction_data.get('level_diff', 'N/A')} m"],
        ['Date', prediction_data.get('date', 'N/A')],
        ['State', prediction_data.get('state_name', 'N/A')],
        ['District', prediction_data.get('district_name', 'N/A')],
        ['Basin', prediction_data.get('basin', 'N/A')],
        ['Sub-Basin', prediction_data.get('sub_basin', 'N/A')],
        ['Station', prediction_data.get('station_name', 'N/A')]
    ]
    
    input_table = Table(input_data, colWidths=[2.5*inch, 3.5*inch])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    
    elements.append(input_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ── Weather Information (if available) ────────────────────────────────────
    if prediction_data.get('temperature') or prediction_data.get('humidity'):
        elements.append(Paragraph("Weather Conditions", heading_style))
        
        weather_data = [
            ['Metric', 'Value'],
            ['Temperature', f"{prediction_data.get('temperature', 'N/A')}°C"],
            ['Humidity', f"{prediction_data.get('humidity', 'N/A')}%"],
            ['Rainfall', f"{prediction_data.get('rainfall', 'N/A')} mm"],
            ['Condition', prediction_data.get('weather_condition', 'N/A')]
        ]
        
        weather_table = Table(weather_data, colWidths=[2.5*inch, 3.5*inch])
        weather_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0ea5e9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f9ff')])
        ]))
        
        elements.append(weather_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # ── Recommendations ───────────────────────────────────────────────────────
    if prediction_data.get('recommendations'):
        elements.append(Paragraph("AI Recommendations", heading_style))
        
        for i, rec in enumerate(prediction_data['recommendations'][:5], 1):
            elements.append(Paragraph(f"<b>{i}. {rec.get('title', 'Recommendation')}</b>", subheading_style))
            elements.append(Paragraph(rec.get('detail', ''), normal_style))
            elements.append(Paragraph(f"<i>Category: {rec.get('category', 'N/A')} | Priority: {rec.get('priority', 'N/A')}</i>", normal_style))
            elements.append(Spacer(1, 0.15*inch))
    
    # ── Footer ────────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("This report was generated by AquaVision AI - Water Availability Prediction System", footer_style))
    elements.append(Paragraph("For more information, visit your dashboard or contact support.", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data
