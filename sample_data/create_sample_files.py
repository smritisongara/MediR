from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DATA_DIR = Path(__file__).resolve().parent

def create_sample_prescription_image():
    # Create a realistic prescription graphic
    img = Image.new('RGB', (800, 1000), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Header banner
    draw.rectangle([(0, 0), (800, 100)], fill='#0284c7')
    draw.text((30, 25), "CITY HEALTH CLINIC - DR. A. SHARMA, MD", fill='#ffffff')
    draw.text((30, 60), "Reg No: MCI-48291 | Phone: +91-9876543210", fill='#e0f2fe')
    
    # Patient Info
    draw.rectangle([(20, 120), (780, 180)], outline='#cbd5e1', width=1)
    draw.text((40, 135), "Patient: John Doe (Demo Patient)    Age: 34 Y / M", fill='#1e293b')
    draw.text((40, 155), "Date: 12-Nov-2025                   Diagnosis: Pharyngitis", fill='#475569')
    
    # Prescription Symbol
    draw.text((40, 200), "Rx", fill='#0284c7')
    
    # Medicines
    meds = [
        "1. Tab. Amoxicillin 500mg - 1 tab three times daily (after food) x 5 days",
        "   [Antibiotic for respiratory infection - complete full 5-day course]",
        "",
        "2. Tab. Paracetamol 650mg - 1 tab SOS for fever/pain (max 3/day)",
        "   [Pain and fever relief - take with water]",
        "",
        "3. Tab. Cetirizine 10mg - 1 tab at bedtime x 3 days",
        "   [Relief from cold and allergy symptoms]",
        "",
        "Clinical Advice:",
        "- Drink plenty of warm water and rest well.",
        "- Avoid cold foods and drinks.",
        "- Review with doctor if fever persists beyond 3 days."
    ]
    
    y = 250
    for line in meds:
        color = '#0f172a' if not line.startswith('   [') else '#0284c7'
        draw.text((40, y), line, fill=color)
        y += 35
        
    # Signature line
    draw.line([(550, 880), (750, 880)], fill='#64748b', width=2)
    draw.text((580, 890), "Dr. A. Sharma (MD)", fill='#1e293b')
    draw.text((560, 910), "Senior Medical Officer", fill='#64748b')
    
    img.save(DATA_DIR / "sample_prescription.png")
    print(f"Generated {DATA_DIR / 'sample_prescription.png'}")

def create_sample_pdf():
    # Simple valid single-page text PDF
    content = (
        "METROPOLIS CLINICAL DIAGNOSTICS LABORATORY\n"
        "Patient: John Doe (34 Y / Male) | Date: 10-Nov-2025\n"
        "COMPLETE BLOOD COUNT (CBC) LABORATORY REPORT\n\n"
        "Hemoglobin (Hb): 10.2 g/dL [LOW] (Normal: 13.0 - 17.0 g/dL)\n"
        "Total Leucocyte Count (WBC): 14,800 /mcL [HIGH] (Normal: 4,000 - 11,000 /mcL)\n"
        "Red Blood Cells (RBC): 3.9 million/mcL [LOW] (Normal: 4.5 - 5.5 million/mcL)\n"
        "Platelet Count: 220,000 /mcL [NORMAL] (Normal: 150,000 - 450,000 /mcL)\n"
        "Neutrophils: 78 % [HIGH] (Normal: 40 - 70 %)\n"
        "Lymphocytes: 18 % [LOW] (Normal: 20 - 40 %)\n"
        "ESR: 32 mm/hr [HIGH] (Normal: 0 - 15 mm/hr)\n\n"
        "Clinical Interpretation: Elevated WBC with mild anemia. Consult physician."
    )
    
    # We can write a minimal PDF 1.4 document
    text_escaped = content.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    pdf_lines = [
        "%PDF-1.4",
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj",
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj",
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj",
        "5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj",
    ]
    
    # Construct stream with text positions
    stream_ops = ["BT", "/F1 12 Tf", "50 720 Td", "18 TL"]
    for l in content.split("\n"):
        clean_l = l.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        stream_ops.append(f"({clean_l}) '")
    stream_ops.append("ET")
    stream_str = "\n".join(stream_ops)
    
    stream_obj = f"4 0 obj << /Length {len(stream_str.encode('utf-8'))} >> stream\n{stream_str}\nendstream\nendobj"
    pdf_lines.append(stream_obj)
    
    # xref table
    xref_pos = 0
    full_doc = "\n".join(pdf_lines) + "\nxref\n0 6\n0000000000 65535 f \n"
    # Write to file
    with open(DATA_DIR / "sample_blood_test.pdf", "wb") as f:
        # Generate with pypdf or writer
        f.write((full_doc + "trailer << /Size 6 /Root 1 0 R >>\nstartxref\n999\n%%EOF").encode('latin1'))
    print(f"Generated {DATA_DIR / 'sample_blood_test.pdf'}")

if __name__ == '__main__':
    create_sample_prescription_image()
    create_sample_pdf()
