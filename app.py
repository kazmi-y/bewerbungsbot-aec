# app.py
from cv_extractor import extract_cv_text
import streamlit as st
import tempfile
import os
from models import UserProfile
from generator import generate_cv, generate_cover_letter
from document_builder import create_cv_document, create_cover_letter_document



st.set_page_config(
    page_title="BewerbungsBot AEC",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ BewerbungsBot AEC")
st.caption("Professional German application documents for the AEC industry — powered by Gemini AI")


# ─────────────────────────────────────────────
# SIDEBAR — Input fields
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Personal Information")

    full_name       = st.text_input("Full Name", value="Yasir Kazmi")
    date_of_birth   = st.text_input("Date of Birth", value="15.09.1988", placeholder="DD.MM.YYYY")
    nationality     = st.text_input("Nationality", value="Deutsch")
    city            = st.text_input("City of Residence", value="Chemnitz")
    email           = st.text_input("Email Address", value="yasir.h.kazmi@gmail.com")
    phone           = st.text_input("Phone Number", value="+49-176-735-69-963")

    st.divider()
    st.header("🎓 Education")

    university      = st.text_input("University", value="Bauhaus-Universität Weimar")
    degree          = st.text_input("Degree", value="M.Sc. Bauingenieurwesen")
    thesis_title    = st.text_input("Thesis Title (optional)", value="")
    grade           = st.text_input("Final Grade (optional)", value="")

    st.divider()
    st.header("💼 Professional Experience")

    years_experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=12)

    bim_roles = st.multiselect(
        "BIM Roles",
        options=["BIM Manager", "BIM Koordinator", "BIM Modeler", "BIM Berater", "VDC Manager"],
        default=["BIM Manager", "BIM Koordinator", "BIM Modeler"]
    )

    software_skills = st.multiselect(
        "Software Skills",
        options=["Revit", "IfcOpenShell", "Python", "Solibri", "Navisworks",
                 "AutoCAD", "Dynamo", "Power BI", "Dalux", "BIM 360"],
        default=["Revit", "IfcOpenShell", "Python", "Solibri"]
    )

    st.divider()
    st.header("🎯 Target Position")

    target_job_title = st.text_input("Job Title", value="BIM Manager")
    target_company   = st.text_input("Company Name", value="Ed. Züblin AG")

    st.divider()
    st.header("📄 Upload Documents")

    uploaded_cv    = st.file_uploader("Existing CV (PDF/DOCX)", type=["pdf", "docx", "doc"])
    uploaded_photo = st.file_uploader("Profile Photo (JPG/PNG)", type=["jpg", "jpeg", "png"])
    uploaded_cl    = st.file_uploader("Previous Cover Letter (optional)", type=["pdf", "docx"])

    st.divider()
    st.header("📢 Job Advertisement")

    job_ad_text = st.text_area(
        "Paste the full job advertisement here",
        height=200,
        placeholder="Copy and paste the complete job posting text..."
    )


# ─────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 CV (Lebenslauf)")
    generate_cv_btn = st.button("🚀 Generate CV", use_container_width=True, type="primary")

with col2:
    st.subheader("✉️ Cover Letter (Anschreiben)")
    generate_cl_btn = st.button("🚀 Generate Cover Letter", use_container_width=True, type="primary")


# --- PHOTO HANDLING ---
photo_path = None
if uploaded_photo is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_photo.read())
        photo_path = tmp.name

# --- UPLOADED FILE TEXT PLACEHOLDERS ---
cv_extracted_text = None
if uploaded_cv is not None:
    with st.spinner("📖 Reading your CV..."):
        cv_extracted_text = extract_cv_text(uploaded_cv)
    if cv_extracted_text and not cv_extracted_text.startswith("⚠️"):
        st.sidebar.success(f"✅ CV read: {len(cv_extracted_text)} characters extracted")
    else:
        st.sidebar.warning(cv_extracted_text)

cl_extracted_text = None
if uploaded_cl is not None:
    cl_extracted_text = extract_cv_text(uploaded_cl)


# --- BUILD PROFILE ---
profile = UserProfile(
    full_name=full_name,
    date_of_birth=date_of_birth,
    nationality=nationality,
    city=city,
    email=email,
    phone=phone,
    university=university,
    degree=degree,
    thesis_title=thesis_title or None,
    grade=grade or None,
    bim_roles=bim_roles,
    software_skills=software_skills,
    years_experience=years_experience,
    target_job_title=target_job_title,
    target_company=target_company,
    job_ad_text=job_ad_text,
    cv_extracted_text=cv_extracted_text,
    cover_letter_extracted_text=cl_extracted_text
)


# ─────────────────────────────────────────────
# CV GENERATION
# ─────────────────────────────────────────────
if generate_cv_btn:
    if not job_ad_text.strip():
        st.error("❌ Please paste a job advertisement before generating.")
    else:
        with st.spinner("⏳ Gemini is generating your CV..."):
            cv_text = generate_cv(profile)

        if cv_text.startswith("❌"):
            st.error(cv_text)
        else:
            st.session_state["cv_text"] = cv_text
            st.success("✅ CV generated successfully!")

if "cv_text" in st.session_state:
    with col1:
        with st.expander("👁️ Preview (raw text)", expanded=False):
            st.text(st.session_state["cv_text"][:1000] + "...")

        cv_buffer = create_cv_document(
            st.session_state["cv_text"],
            profile.full_name,
            photo_path=photo_path
        )

        st.download_button(
            label="⬇️ Download CV as .docx",
            data=cv_buffer,
            file_name=f"Lebenslauf_{profile.full_name.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )


# ─────────────────────────────────────────────
# COVER LETTER GENERATION
# ─────────────────────────────────────────────
if generate_cl_btn:
    if not job_ad_text.strip():
        st.error("❌ Please paste a job advertisement before generating.")
    else:
        with st.spinner("⏳ Gemini is writing your cover letter..."):
            cl_text = generate_cover_letter(profile)

        if cl_text.startswith("❌"):
            st.error(cl_text)
        else:
            st.session_state["cl_text"] = cl_text
            st.success("✅ Cover letter generated successfully!")

if "cl_text" in st.session_state:
    with col2:
        with st.expander("👁️ Preview (raw text)", expanded=False):
            st.text(st.session_state["cl_text"][:1000] + "...")

        cl_buffer = create_cover_letter_document(
            st.session_state["cl_text"],
            profile.full_name
        )

        st.download_button(
            label="⬇️ Download Cover Letter as .docx",
            data=cl_buffer,
            file_name=f"Anschreiben_{profile.full_name.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
st.caption("BewerbungsBot AEC • Powered by Google Gemini • Built with Python + Streamlit")
