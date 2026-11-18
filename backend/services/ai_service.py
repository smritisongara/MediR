import os
import re
import json
import logging
from backend.config import Config

logger = logging.getLogger(__name__)

# Medical Term Glossary with patient-friendly educational definitions
MEDICAL_GLOSSARY = {
    "hemoglobin": "The protein inside your red blood cells that carries oxygen from your lungs to the rest of your body.",
    "wbc": "White Blood Cells are your body's immune defense soldiers that fight off infections, viruses, and bacteria.",
    "leucocyte": "Another medical name for White Blood Cells, essential for immunity and fighting infections.",
    "rbc": "Red Blood Cells are disc-shaped cells responsible for delivering fresh oxygen to all your tissues.",
    "platelet": "Tiny cell fragments in your blood that help form clots to stop bleeding when you have a cut or injury.",
    "neutrophil": "The most common type of white blood cell, specially mobilized to fight off sudden bacterial infections.",
    "lymphocyte": "A type of white blood cell that produces antibodies and remembers past infections to protect you.",
    "esr": "Erythrocyte Sedimentation Rate: a blood test measuring how quickly red cells settle, often elevated during inflammation or infection.",
    "pcv": "Packed Cell Volume (Hematocrit): the percentage of your blood volume made up of red blood cells.",
    "cholesterol": "A waxy fat-like substance found in all your cells. While your body needs it to build cells, excessive amounts can build up in arteries.",
    "triglycerides": "A type of fat (lipid) in your blood stored from unused calories. High levels may increase cardiovascular risk.",
    "hdl": "High-Density Lipoprotein, known as 'Good Cholesterol', helps remove extra cholesterol from your bloodstream back to your liver.",
    "ldl": "Low-Density Lipoprotein, known as 'Bad Cholesterol', can slowly build up plaque inside artery walls if levels remain high.",
    "vldl": "Very Low-Density Lipoprotein, carrying triglycerides in your bloodstream.",
    "creatinine": "A waste product from muscle breakdown that healthy kidneys filter out through urine. Used to monitor kidney filtration.",
    "uric acid": "A waste byproduct from digestion of purines. High levels can crystallize in joints causing gout pain.",
    "hba1c": "A blood test showing your average blood sugar level over the past 2 to 3 months.",
    "fasting glucose": "The concentration of sugar in your blood after fasting (no food or drink except water) for at least 8 hours.",
    "sgpt": "Serum Glutamic Pyruvic Transaminase (ALT): an enzyme found mainly in liver cells, checked to assess liver health.",
    "sgot": "Serum Glutamic Oxaloacetic Transaminase (AST): an enzyme present in the liver, heart, and muscles.",
    "bilirubin": "A yellowish pigment formed during normal breakdown of red blood cells, processed by the liver.",
    "tsh": "Thyroid Stimulating Hormone: produced by your pituitary gland to regulate thyroid activity and metabolism.",
    "amoxicillin": "A widely used penicillin-class antibiotic that treats bacterial infections of the ear, nose, throat, or chest.",
    "paracetamol": "A medication commonly used to relieve mild-to-moderate pain and reduce high body temperature (fever).",
    "cetirizine": "An antihistamine medicine that relieves allergy symptoms like sneezing, runny nose, watery eyes, or hives."
}

# Standard Clinical Reference Rules
REFERENCE_RULES = [
    {
        "test_name": "Hemoglobin (Hb)",
        "keywords": ["hemoglobin", "hb"],
        "unit": "g/dL",
        "normal_min": 13.0,
        "normal_max": 17.0,
        "simple_explanation": "Carries fresh oxygen from lungs to muscles and organs."
    },
    {
        "test_name": "Total Leucocyte Count (WBC)",
        "keywords": ["wbc", "total leucocyte", "leukocyte", "tlc"],
        "unit": "/mcL",
        "normal_min": 4000,
        "normal_max": 11000,
        "simple_explanation": "Immune defense cells that fight bacterial and viral infections."
    },
    {
        "test_name": "Red Blood Cells (RBC)",
        "keywords": ["rbc", "red blood cell"],
        "unit": "million/mcL",
        "normal_min": 4.5,
        "normal_max": 5.5,
        "simple_explanation": "Vital disc-shaped cells delivering oxygen throughout your body."
    },
    {
        "test_name": "Packed Cell Volume (PCV / Hematocrit)",
        "keywords": ["pcv", "packed cell volume", "hematocrit"],
        "unit": "%",
        "normal_min": 38.0,
        "normal_max": 50.0,
        "simple_explanation": "Proportion of whole blood composed of red blood cells."
    },
    {
        "test_name": "Platelet Count",
        "keywords": ["platelet", "thrombocyte"],
        "unit": "/mcL",
        "normal_min": 150000,
        "normal_max": 450000,
        "simple_explanation": "Blood-clotting cells essential to halt bleeding upon cuts or injury."
    },
    {
        "test_name": "Neutrophils",
        "keywords": ["neutrophil", "neutrophils"],
        "unit": "%",
        "normal_min": 40.0,
        "normal_max": 70.0,
        "simple_explanation": "Frontline infection fighters responding quickly to acute inflammation."
    },
    {
        "test_name": "Lymphocytes",
        "keywords": ["lymphocyte", "lymphocytes"],
        "unit": "%",
        "normal_min": 20.0,
        "normal_max": 40.0,
        "simple_explanation": "Immune cells that remember pathogens and produce antibodies."
    },
    {
        "test_name": "ESR (Erythrocyte Sed. Rate)",
        "keywords": ["esr", "erythrocyte sedimentation"],
        "unit": "mm/hr",
        "normal_min": 0,
        "normal_max": 15,
        "simple_explanation": "Non-specific inflammatory index indicating infection or body stress."
    },
    {
        "test_name": "Total Cholesterol",
        "keywords": ["total cholesterol", "cholesterol total"],
        "unit": "mg/dL",
        "normal_min": 0,
        "normal_max": 200,
        "simple_explanation": "Total lipid measurement in bloodstream. High levels warrant diet check."
    },
    {
        "test_name": "Triglycerides",
        "keywords": ["triglyceride", "triglycerides"],
        "unit": "mg/dL",
        "normal_min": 0,
        "normal_max": 150,
        "simple_explanation": "Circulating dietary fat stored in tissue. Best kept below 150 mg/dL."
    },
    {
        "test_name": "HDL Cholesterol ('Good')",
        "keywords": ["hdl", "hdl cholesterol"],
        "unit": "mg/dL",
        "normal_min": 40,
        "normal_max": 100,
        "simple_explanation": "Protective cholesterol that sweeps excess fats back to liver."
    },
    {
        "test_name": "LDL Cholesterol ('Bad')",
        "keywords": ["ldl", "ldl cholesterol"],
        "unit": "mg/dL",
        "normal_min": 0,
        "normal_max": 100,
        "simple_explanation": "Plaque-forming lipid. Keeping below 100 protects cardiovascular health."
    },
    {
        "test_name": "Fasting Blood Sugar",
        "keywords": ["fasting blood sugar", "fbs", "fasting glucose"],
        "unit": "mg/dL",
        "normal_min": 70,
        "normal_max": 100,
        "simple_explanation": "Morning glucose concentration after an 8-hour overnight fast."
    },
    {
        "test_name": "HbA1c",
        "keywords": ["hba1c", "glycated hemoglobin"],
        "unit": "%",
        "normal_min": 4.0,
        "normal_max": 5.7,
        "simple_explanation": "Average blood sugar control over previous 90-day period."
    }
]

def analyze_medical_values(text):
    """
    Extract laboratory parameters and return structured 5-column table items:
    Test Name | Measured Value | Unit | Reference Range | Simple Explanation
    """
    findings = []
    abnormal = []
    
    lines = text.split("\n")
    for rule in REFERENCE_RULES:
        for line in lines:
            line_clean = line.lower()
            if any(k in line_clean for k in rule["keywords"]):
                match = re.search(r'[:\s-]([0-9]+(?:\.[0-9]+)?)\b', line)
                if match:
                    try:
                        val = float(match.group(1))
                        status = "NORMAL"
                        status_color = "normal"
                        
                        if val < rule["normal_min"]:
                            status = "LOW"
                            status_color = "warning"
                        elif val > rule["normal_max"]:
                            status = "HIGH"
                            status_color = "danger"
                            
                        if "[high]" in line_clean or " high" in line_clean:
                            status = "HIGH"
                            status_color = "danger"
                        elif "[low]" in line_clean or " low" in line_clean:
                            status = "LOW"
                            status_color = "warning"
                            
                        item = {
                            "test_name": rule["test_name"],
                            "measured_value": str(val),
                            "unit": rule["unit"],
                            "reference_range": f"{rule['normal_min']} - {rule['normal_max']}",
                            "status": status,
                            "status_color": status_color,
                            "simple_explanation": rule["simple_explanation"],
                            # Legacy backward compatibility keys:
                            "parameter": rule["test_name"],
                            "value": f"{val} {rule['unit']}",
                            "meaning": rule["simple_explanation"]
                        }
                        findings.append(item)
                        if status in ("HIGH", "LOW"):
                            abnormal.append(item)
                        break
                    except Exception:
                        pass

    return findings, abnormal

def simplify_medical_report(extracted_text):
    """
    Comprehensive report simplification conforming to all clinical requirements:
    - Summary
    - Decoded terms & meanings
    - 5-Column Table data
    - Flagged abnormal values
    - Important clinical observations
    - Unreadable/missing information notice
    - Doctor questions
    """
    if not extracted_text or len(extracted_text.strip()) == 0:
        return {
            "summary": "No readable medical text was detected.",
            "results_table": [],
            "abnormal_values": [],
            "important_observations": ["Document appears empty or contains non-text content."],
            "unreadable_or_missing": "Unable to extract test names or laboratory parameters.",
            "recommended_doctor_questions": ["Please request a clear physical copy of this report from the diagnostic clinic."],
            "disclaimer": "⚠️ MediR is an educational medical communication assistant, not a doctor."
        }

    findings, abnormal = analyze_medical_values(extracted_text)

    # 1. Summary
    summary_parts = []
    if len(findings) > 0:
        summary_parts.append(f"We analyzed {len(findings)} key laboratory parameters from the submitted information.")
        if len(abnormal) > 0:
            summary_parts.append(
                f"⚠️ Attention: {len(abnormal)} parameter(s) were flagged outside biological reference ranges "
                f"({', '.join([a['test_name'] for a in abnormal])})."
            )
        else:
            summary_parts.append("✅ All identified parameters appear to lie within standard biological reference ranges.")
    else:
        summary_parts.append("Your medical text was reviewed. General health terminology and clinical instructions were extracted.")

    # 2. Important Observations
    observations = []
    for a in abnormal:
        if "wbc" in a["test_name"].lower():
            observations.append("Elevated White Blood Cell count (Leukocytosis): Commonly indicates an active immune response to infection, throat inflammation, or tissue stress.")
        elif "hemoglobin" in a["test_name"].lower():
            observations.append("Low Hemoglobin: Indicates reduced oxygen-carrying capacity (anemia), which can lead to fatigue, lightheadedness, or shortness of breath.")
        elif "cholesterol" in a["test_name"].lower() or "lipid" in a["test_name"].lower():
            observations.append("Elevated Lipid/Cholesterol markers: Indicates increased circulating blood fats, warranting lifestyle, dietary, and physician review.")
        elif "esr" in a["test_name"].lower():
            observations.append("Elevated ESR: Reflects systemic inflammatory activity in the body.")

    if not observations and len(findings) > 0:
        observations.append("Laboratory parameters appear stable and congruent with reference bounds.")
    elif not observations:
        observations.append("No specific abnormal markers detected from the readable text.")

    # 3. Unreadable or missing info check
    unreadable_notice = None
    if len(extracted_text.split()) < 15 and len(findings) == 0:
        unreadable_notice = "Certain sections of the medical document could not be completely parsed. Please verify handwritten notes or faint stamps directly with your clinic."

    # 4. Doctor questions
    doctor_questions = [
        "What do these test readings mean in the context of my symptoms and current lifestyle?",
        "Are any follow-up tests or repeat evaluations recommended in the coming weeks?",
        "Should I consider any dietary, hydration, or activity adjustments based on these results?"
    ]
    if any("wbc" in a["test_name"].lower() for a in abnormal):
        doctor_questions.append("My White Blood Cell count is elevated. Could this indicate an active infection or seasonal illness?")
    if any("hemoglobin" in a["test_name"].lower() for a in abnormal):
        doctor_questions.append("My Hemoglobin reading is below range. Do I need an iron profile evaluation or nutritional supplements?")
    if any("cholesterol" in a["test_name"].lower() for a in abnormal):
        doctor_questions.append("My lipid numbers are elevated. What heart-healthy meal and exercise plan is best for me?")

    # 5. Glossary terms
    glossary_terms = []
    text_lower = extracted_text.lower()
    for term, definition in MEDICAL_GLOSSARY.items():
        if term in text_lower:
            glossary_terms.append({
                "term": term.title(),
                "simple_explanation": definition
            })

    return {
        "summary": " ".join(summary_parts),
        "results_table": findings,
        "key_findings": findings,
        "abnormal_values": abnormal,
        "important_observations": observations,
        "unreadable_or_missing": unreadable_notice,
        "glossary": glossary_terms[:8],
        "recommended_doctor_questions": doctor_questions,
        "disclaimer": "⚠️ MediR provides educational medical communication assistance only. It does not diagnose diseases, prescribe medication, or substitute for a licensed healthcare professional."
    }

def get_chatbot_response(user_question, report_context=""):
    """
    Handle patient questions with contextual medical intelligence, simple language, and strict safety guardrails.
    """
    q_lower = user_question.lower()
    
    if any(k in q_lower for k in ["diagnose me", "do i have cancer", "am i dying", "prescribe", "should i take", "change my dose", "stop taking"]):
        return (
            "⚠️ **Important Safety Notice**: As an AI educational assistant, MediR cannot diagnose medical conditions, "
            "prescribe medications, or adjust drug dosages. \n\n"
            "Please share your symptoms and report directly with your qualified doctor or healthcare specialist. "
            "If you are experiencing severe pain, difficulty breathing, or acute symptoms, seek immediate emergency medical care."
        )
        
    for term, definition in MEDICAL_GLOSSARY.items():
        if term in q_lower:
            return (
                f"**{term.upper()} (Medical Explanation)**:\n\n"
                f"{definition}\n\n"
                f"💡 *In your report*: If your report shows this parameter with an arrow or tag like [HIGH] or [LOW], "
                f"it indicates a reading outside standard reference bounds. Ask your doctor how it relates to how you feel."
            )

    if "high" in q_lower or "abnormal" in q_lower or "low" in q_lower:
        if report_context:
            _, abnormal = analyze_medical_values(report_context)
            if abnormal:
                bullets = "\n".join([f"- **{a['test_name']}**: {a['measured_value']} {a['unit']} (Ref: {a['reference_range']}) - {a['simple_explanation']}" for a in abnormal])
                return (
                    f"Based on the report you uploaded, the following values were flagged outside standard bounds:\n\n"
                    f"{bullets}\n\n"
                    f"**Next Steps**:\n"
                    f"These numbers give your physician clues about what might be going on (e.g. infection, hydration, diet). "
                    f"We recommend asking: *'Doctor, what is the best approach to normalize these values?'*"
                )
        return (
            "In laboratory reports, a 'High' or 'Low' result means your value is outside the reference range established for healthy adults. "
            "Many temporary factors like dehydration, recent exercise, minor colds, or diet can cause slight shifts. Always confirm with your physician."
        )

    if "ask my doctor" in q_lower or "questions for doctor" in q_lower:
        return (
            "Here are great questions you can bring to your next doctor appointment:\n\n"
            "1. *What do these specific lab numbers indicate for my daily health?*\n"
            "2. *Are any of my values urgent, or are they mild fluctuations?*\n"
            "3. *What lifestyle, dietary, or hydration changes can help improve them?*\n"
            "4. *When should I schedule a follow-up or repeat test?*"
        )

    return (
        f"Thank you for your question. Here is a simplified explanation:\n\n"
        f"Medical reports reflect measurements taken at a specific moment in time. "
        f"Values are always interpreted in the context of your symptoms, age, and medical history.\n\n"
        f"If you'd like to understand a specific test or line from your document, type the name (e.g., 'Hemoglobin', 'WBC', 'Platelets', 'Triglycerides') "
        f"and MediR will explain what it does in simple terms!"
    )
