# generator.py
import os
from google import genai
from dotenv import load_dotenv
from models import UserProfile

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"


def build_cv_prompt(profile: UserProfile) -> str:
    """
    Highly prescriptive prompt that forces Gemini to output
    structured text matching German AEC two-column CV format.
    """

    # Extract software with proficiency levels
    software_with_levels = []
    if profile.software_skills:
        for sw in profile.software_skills:
            # You can extend this to accept dict like {"Revit": "Expert"}
            software_with_levels.append(f"{sw} – Fortgeschritten")

    # Add AEC keywords if job ad mentions them
    aec_keywords = []
    if profile.job_ad_text:
        job_ad_lower = profile.job_ad_text.lower()
        if "iso 19650" in job_ad_lower or "bim" in job_ad_lower:
            aec_keywords.append("ISO 19650")
        if "hoai" in job_ad_lower:
            aec_keywords.append("HOAI")
        if "vob" in job_ad_lower:
            aec_keywords.append("VOB")

    return f"""
Du bist ein Experte für deutsche Bewerbungen im Bauwesen (AEC-Branche).
Erstelle einen **tabellarischen Lebenslauf** nach deutschem Standard für die Position **{profile.target_job_title}** bei **{profile.target_company}**.

WICHTIGE FORMATIERUNGS-REGELN:
1. **Zwei-Spalten-Layout**: Linke Spalte = Zeitraum (MM/YYYY – MM/YYYY), rechte Spalte = Details
2. **Maximal 2 Seiten**
3. **Umgekehrt chronologisch** (neuste Erfahrung zuerst)
4. **Keine Lücken** im Lebenslauf — jeder Zeitraum muss lückenlos an den nächsten anschließen
5. **Abschnitte in dieser Reihenfolge**:
   - Persönliche Daten
   - Berufserfahrung
   - Ausbildung
   - Weiterbildung (BIM-Zertifikate ZUERST, dann andere)
   - Kenntnisse (Software, Methoden, Standards)
   - Sprachen

PERSÖNLICHE DATEN:
- Name: {profile.full_name}
- Geburtsdatum: {profile.date_of_birth}
- Nationalität: {profile.nationality}
- Wohnort: {profile.city}
- Telefon: {profile.phone}
- E-Mail: {profile.email}

BERUFSERFAHRUNG — KRITISCH: NUR die folgenden Daten verwenden, NICHTS erfinden:
{profile.cv_extracted_text or "⚠️ KEIN LEBENSLAUF HOCHGELADEN — Bitte nur die oben angegebenen Daten verwenden, KEINE Erfahrung erfinden."}

STRIKTE REGEL: Du darfst KEINE Unternehmen, Positionen, Projekte oder Daten erfinden, 
die nicht explizit in den obigen Daten stehen. Wenn keine Berufserfahrung vorhanden ist, 
schreibe "Berufserfahrung folgt" und lasse den Abschnitt leer.

AUSBILDUNG:
- Universität: {profile.university}
- Abschluss: {profile.degree}
- Abschlussarbeit: {profile.thesis_title or "nicht angegeben"}
- Note: {profile.grade or "nicht angegeben"}

BIM-ROLLEN: {", ".join(profile.bim_roles) if profile.bim_roles else "keine"}
SOFTWARE-KENNTNISSE: {", ".join(software_with_levels) if software_with_levels else "keine"}
BERUFSERFAHRUNG: {profile.years_experience} Jahre

ZIELPOSITION: {profile.target_job_title}
ZIELUNTERNEHMEN: {profile.target_company}

STELLENAUSSCHREIBUNG (Keywords beachten):
{profile.job_ad_text}

WICHTIGE AEC-KEYWORDS (wenn relevant, einbauen):
{", ".join(aec_keywords) if aec_keywords else "keine spezifischen Standards erwähnt"}

OUTPUT-FORMAT:
Gib den Lebenslauf im folgenden strukturierten Format zurück:

**PERSÖNLICHE DATEN**
Geburtsdatum: [Datum]
Nationalität: [Land]
Wohnort: [Stadt]
Telefon: [Nummer]
E-Mail: [Adresse]

**BERUFSERFAHRUNG**
[MM/YYYY – MM/YYYY] | **[Jobtitel]**, [Unternehmen], [Stadt]
• [Aufgabe 1 mit konkreten Erfolgen und Keywords aus der Stellenausschreibung]
• [Aufgabe 2]
• [Aufgabe 3]

[Für jede weitere Position wiederholen]

**AUSBILDUNG**
[MM/YYYY – MM/YYYY] | **[Abschluss]**, [Universität], [Stadt]
Abschlussarbeit: [Titel]
Note: [Note]

**WEITERBILDUNG**
[MM/YYYY] | **[BIM-Zertifikat 1]**, [Institution]
[MM/YYYY] | **[BIM-Zertifikat 2]**, [Institution]
[MM/YYYY] | **[Andere Zertifikate]**, [Institution]

**KENNTNISSE**
**BIM-Management & Methoden:**
{", ".join(profile.bim_roles) if profile.bim_roles else "—"}

**Software:**
{", ".join(software_with_levels) if software_with_levels else "—"}

**Standards & Normen:**
{", ".join(aec_keywords) if aec_keywords else "—"}

**SPRACHEN**
Deutsch – Muttersprache
Englisch – Verhandlungssicher
[Weitere Sprachen falls vorhanden]

KRITISCHE REGEL: Gib NUR den fertigen Lebenslauf zurück, KEINE Erklärungen davor oder danach.
"""


def generate_cv(profile: UserProfile) -> str:
    prompt = build_cv_prompt(profile)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Fehler bei der CV-Generierung: {str(e)}"


def build_cover_letter_prompt(profile: UserProfile) -> str:
    """DIN 5008 compliant cover letter with named contact preference."""

    return f"""
Du bist ein Experte für deutsche Bewerbungsschreiben im Bauwesen (AEC-Branche).
Erstelle ein **professionelles Anschreiben nach DIN 5008** für die Position **{profile.target_job_title}** bei **{profile.target_company}**.

FORMATIERUNGS-REGELN:
1. **Streng 1 Seite**
2. **DIN 5008-Layout**:
   - Absenderadresse oben links (Name, Straße, PLZ Stadt)
   - Empfängeradresse darunter
   - Datum rechtsbündig
   - Betreffzeile (fett, ohne "Betreff:")
3. **Anrede**: Wenn Ansprechpartner bekannt → "Sehr geehrter Herr [Name]" / "Sehr geehrte Frau [Name]"
   Falls nicht bekannt → "Sehr geehrte Damen und Herren"
4. **3-Absatz-Struktur**:
   - Absatz 1: Aktueller Kontext + warum ich mich bewerbe
   - Absatz 2: Meine Qualifikationen passend zur Stellenausschreibung (Keywords einbauen!)
   - Absatz 3: Interviewanfrage, keine Gehaltsvorstellungen, keine Verfügbarkeit
5. **Schluss**: "Mit freundlichen Grüßen" + Unterschriftsblock

BEWERBER-DATEN:
- Name: {profile.full_name}
- Wohnort: {profile.city}
- Telefon: {profile.phone}
- E-Mail: {profile.email}

POSITION: {profile.target_job_title}
UNTERNEHMEN: {profile.target_company}

STELLENAUSSCHREIBUNG (Keywords daraus verwenden):
{profile.job_ad_text}

VORHERIGES ANSCHREIBEN DES BEWERBERS (falls vorhanden, verbessern):
{profile.cover_letter_extracted_text or "Kein vorheriges Anschreiben vorhanden"}

QUALIFIKATIONEN:
- BIM-Rollen: {", ".join(profile.bim_roles) if profile.bim_roles else "keine"}
- Software: {", ".join(profile.software_skills) if profile.software_skills else "keine"}
- Erfahrung: {profile.years_experience} Jahre
- Universität: {profile.university}
- Abschluss: {profile.degree}

OUTPUT-FORMAT-BEISPIEL:

{profile.full_name}
[Straße + Hausnummer]
[PLZ] {profile.city}
Telefon: {profile.phone}
E-Mail: {profile.email}

{profile.target_company}
[Abteilung / Personalabteilung]
[Straße]
[PLZ] [Stadt]

[Ort], [Datum heute]

**Bewerbung als {profile.target_job_title}**

Sehr geehrter Herr [falls bekannt] / Sehr geehrte Damen und Herren,

[Absatz 1: Einstieg - warum bewerbe ich mich, aktueller Kontext]

[Absatz 2: Qualifikationen - passend zu den Keywords aus der Stellenausschreibung, konkrete Beispiele aus Berufserfahrung]

[Absatz 3: Abschluss - Freude auf Gespräch, Motivation für das Unternehmen]

Mit freundlichen Grüßen

{profile.full_name}

KRITISCHE REGEL: Gib NUR das fertige Anschreiben zurück, KEINE Erklärungen.
"""


def generate_cover_letter(profile: UserProfile) -> str:
    prompt = build_cover_letter_prompt(profile)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Fehler beim Anschreiben: {str(e)}"
