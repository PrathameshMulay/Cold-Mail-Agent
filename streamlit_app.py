
import base64
import io

import pypdf
import streamlit as st

from app.workflow.pipeline import ColdMailPipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Find Recruiters",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state["page"] = 1

if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None

if "email_result" not in st.session_state:
    st.session_state["email_result"] = None


# ============================================================
# BACKGROUND ILLUSTRATION
# ============================================================

def create_background_uri():
    """Create a lightweight abstract SVG background."""

    svg = """
    <svg xmlns="http://www.w3.org/2000/svg"
         width="1600" height="1100" viewBox="0 0 1600 1100">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#f8f7ff"/>
          <stop offset="52%" stop-color="#f2f5ff"/>
          <stop offset="100%" stop-color="#fdf5ff"/>
        </linearGradient>
        <radialGradient id="glow">
          <stop offset="0%" stop-color="#c9bbff" stop-opacity=".52"/>
          <stop offset="100%" stop-color="#c9bbff" stop-opacity="0"/>
        </radialGradient>
      </defs>

      <rect width="1600" height="1100" fill="url(#bg)"/>
      <ellipse cx="1330" cy="100" rx="520" ry="440" fill="url(#glow)"/>
      <ellipse cx="80" cy="900" rx="520" ry="440" fill="url(#glow)"/>

      <g fill="none" stroke="#8f83ee" stroke-opacity=".13"
         stroke-width="2" stroke-dasharray="5 12">
        <path d="M 950 90 C 1170 150, 1050 330, 1320 350
                 S 1470 560, 1250 630"/>
        <path d="M 80 500 C 300 420, 430 580, 550 450"/>
      </g>

      <g fill="#8e7cf0" fill-opacity=".18">
        <circle cx="1120" cy="140" r="7"/>
        <circle cx="1180" cy="158" r="4"/>
        <circle cx="1240" cy="175" r="6"/>
        <circle cx="1300" cy="202" r="4"/>
        <circle cx="1370" cy="240" r="7"/>
        <circle cx="1420" cy="285" r="4"/>
        <circle cx="260" cy="760" r="5"/>
        <circle cx="310" cy="730" r="8"/>
        <circle cx="360" cy="775" r="4"/>
      </g>

      <g transform="translate(1320 350) rotate(-12)"
         fill="#7c68e9" fill-opacity=".12">
        <path d="M 0 0 L 140 -52 L 88 83 L 66 25 Z"/>
        <path d="M 66 25 L 140 -52 L 88 83 L 77 43 Z"
              fill-opacity=".2"/>
      </g>
    </svg>
    """

    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


background_uri = create_background_uri()


# ============================================================
# CUSTOM THEME AND BUTTON STYLING
# ============================================================

st.markdown(
    f"""
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {{
        --primary: #6548ed;
        --primary-dark: #5035d3;
        --text: #18223b;
        --muted: #667085;
        --border: #e6e7f0;
        --card: rgba(255, 255, 255, 0.93);
    }}

    /* Main background */
    .stApp {{
        background-color: #f6f7ff;
        background-image: url("{background_uri}");
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
    }}

    [data-testid="stAppViewContainer"] {{
        background: transparent;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1160px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    h1, h2, h3 {{
        color: var(--text);
        letter-spacing: -0.5px;
    }}

    p, label, .stCaption {{
        color: #475467;
    }}

    /* Brand header */
    .brand-row {{
        display: flex;
        align-items: center;
        gap: 13px;
        margin-bottom: 10px;
    }}

    .brand-mark {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 14px;
        color: white;
        background: linear-gradient(135deg, #8068f6, #5035d3);
        font-size: 25px;
        font-weight: 800;
        box-shadow: 0 7px 20px rgba(101, 72, 237, .24);
    }}

    .brand-name {{
        font-size: 23px;
        font-weight: 800;
        color: #252447;
        line-height: 1.2;
    }}

    .brand-tagline {{
        font-size: 13px;
        color: #737894;
        margin-top: 4px;
    }}

    /* Hero section */
    .hero {{
        position: relative;
        overflow: hidden;
        padding: 32px 34px;
        margin: 18px 0 22px 0;
        border: 1px solid rgba(220, 218, 248, .95);
        border-radius: 24px;
        background: linear-gradient(
            120deg,
            rgba(255, 255, 255, .96),
            rgba(246, 244, 255, .89)
        );
        box-shadow: 0 14px 40px rgba(61, 49, 121, .07);
    }}

    .hero-eyebrow {{
        color: #6548ed;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }}

    .hero-title {{
        color: #202044;
        font-size: clamp(30px, 4vw, 43px);
        line-height: 1.16;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin: 0 0 12px 0;
    }}

    .hero-title span {{
        color: #6548ed;
    }}

    .hero-description {{
        font-size: 15px;
        line-height: 1.7;
        color: #667085;
        max-width: 670px;
        margin: 0;
    }}

    /* Progress step cards */
    .step-card {{
        min-height: 84px;
        padding: 14px 15px;
        border: 1px solid #e4e5f0;
        border-radius: 15px;
        background: rgba(255, 255, 255, .78);
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
    }}

    .step-card.active {{
        background: rgba(245, 242, 255, .98);
        border-color: #9b8bf5;
        box-shadow: 0 4px 15px rgba(101, 72, 237, .08);
    }}

    .step-card.complete {{
        border-color: #b5e4ce;
        background: rgba(245, 255, 249, .93);
    }}

    .step-circle {{
        display: flex;
        flex: 0 0 34px;
        height: 34px;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: #efedf8;
        color: #6e698b;
        font-size: 14px;
        font-weight: 700;
    }}

    .step-card.active .step-circle {{
        background: #6548ed;
        color: white;
    }}

    .step-card.complete .step-circle {{
        background: #169b62;
        color: white;
    }}

    .step-title {{
        font-weight: 700;
        font-size: 13px;
        color: #272642;
    }}

    .step-description {{
        margin-top: 4px;
        font-size: 11px;
        color: #777c91;
        line-height: 1.4;
    }}

    .section-heading {{
        color: #292747;
        font-size: 21px;
        font-weight: 750;
        margin: 3px 0 5px 0;
    }}

    .section-description {{
        color: #72778b;
        font-size: 13px;
        line-height: 1.6;
        margin-bottom: 17px;
    }}

    /* Feature cards */
    .feature-card {{
        min-height: 112px;
        padding: 17px 18px;
        border-radius: 17px;
        border: 1px solid rgba(227, 226, 243, .95);
        background: rgba(255, 255, 255, .86);
        margin-bottom: 18px;
    }}

    .feature-icon {{
        font-size: 23px;
        margin-bottom: 8px;
    }}

    .feature-title {{
        font-weight: 700;
        font-size: 13px;
        color: #302b52;
        margin-bottom: 4px;
    }}

    .feature-description {{
        color: #787b90;
        font-size: 12px;
        line-height: 1.5;
    }}

    /* Cards and containers */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: var(--card);
        border-radius: 18px;
        border-color: var(--border);
        box-shadow: 0 6px 24px rgba(48, 42, 96, .045);
    }}

    /* =====================================================
       PRIMARY CTA BUTTONS
       Covers Find Recruiters, Generate Email, Download Email.
       The broad form-submit selector handles Streamlit's
       separate form-submit button kind.
       ===================================================== */

    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid*="primary"],
    div.stFormSubmitButton > button,
    div.stDownloadButton > button,
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-primaryFormSubmit"] {{
        background: linear-gradient(110deg, #765cf4, #593ce0) !important;
        background-color: #6548ed !important;
        color: #ffffff !important;
        border: 1px solid #6548ed !important;
        border-radius: 12px !important;
        min-height: 48px;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        box-shadow: 0 7px 18px rgba(101, 72, 237, 0.20) !important;
        transition: background 0.2s ease, transform 0.2s ease;
    }}

    /* Force primary button labels/icons to white and bold */
    div.stButton > button[kind="primary"] *,
    div.stButton > button[data-testid*="primary"] *,
    div.stFormSubmitButton > button *,
    div.stDownloadButton > button *,
    button[data-testid="stBaseButton-primary"] *,
    button[data-testid="stBaseButton-primaryFormSubmit"] * {{
        color: #ffffff !important;
        font-weight: 700 !important;
    }}

    /* Primary button hover */
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid*="primary"]:hover,
    div.stFormSubmitButton > button:hover,
    div.stDownloadButton > button:hover,
    button[data-testid="stBaseButton-primary"]:hover,
    button[data-testid="stBaseButton-primaryFormSubmit"]:hover {{
        background: linear-gradient(110deg, #6548ed, #4b2dc7) !important;
        background-color: #5035d3 !important;
        color: #ffffff !important;
        border-color: #5035d3 !important;
        transform: translateY(-1px);
    }}

    /* =====================================================
       SECONDARY BUTTONS
       Back buttons stay white with dark text.
       ===================================================== */

    div.stButton > button[kind="secondary"],
    div.stButton > button[data-testid*="secondary"],
    button[data-testid="stBaseButton-secondary"] {{
        background: rgba(255, 255, 255, 0.96) !important;
        background-color: #ffffff !important;
        color: #4c3bb5 !important;
        border: 1px solid #dedcf2 !important;
        border-radius: 12px !important;
        min-height: 44px;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        box-shadow: none !important;
    }}

    /* Keep secondary button labels/icons dark */
    div.stButton > button[kind="secondary"] *,
    div.stButton > button[data-testid*="secondary"] *,
    button[data-testid="stBaseButton-secondary"] * {{
        color: #4c3bb5 !important;
        font-weight: 500 !important;
    }}

    div.stButton > button[kind="secondary"]:hover,
    div.stButton > button[data-testid*="secondary"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover {{
        background: #f7f5ff !important;
        background-color: #f7f5ff !important;
        border-color: #c7bdf8 !important;
        color: #4c3bb5 !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: rgba(250, 249, 255, .96);
        border-right: 1px solid #e9e6f4;
    }}

    [data-testid="stSidebar"] h2 {{
        font-size: 19px;
    }}

    /* Upload and radio widgets */
    [data-testid="stFileUploader"] {{
        border-radius: 14px;
    }}

    [data-testid="stRadio"] > div {{
        gap: 10px;
    }}

    /* Evidence accordions */
    div[data-testid="stExpander"] {{
        border: 1px solid #e5e4f2;
        border-radius: 13px;
        background: rgba(255, 255, 255, .78);
    }}

    /* Footer */
    .footer-note {{
        text-align: center;
        color: #83869a;
        font-size: 11px;
        margin-top: 32px;
        padding: 15px;
    }}

    @media (max-width: 700px) {{
        .hero {{
            padding: 24px 20px;
        }}

        .brand-name {{
            font-size: 20px;
        }}

        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR — USER API KEYS
# ============================================================

with st.sidebar:
    st.markdown("## 🔑 API Configuration")

    st.caption(
        "Enter your own API keys. They are used by this app "
        "to call the respective services."
    )

    gemini_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        key="gemini_api_key_input",
        placeholder="Enter your Gemini API key",
    )

    hunter_api_key = st.text_input(
        "Hunter API Key",
        type="password",
        key="hunter_api_key_input",
        placeholder="Enter your Hunter API key",
    )

    st.markdown(
        "[Get a Gemini key ↗](https://aistudio.google.com/apikey)"
    )

    st.markdown(
        "[Get a Hunter key ↗](https://hunter.io/api-keys)"
    )

    st.divider()

    st.caption(
        "Keys are not written to a permanent database by this app. "
        "They remain in the active Streamlit session while you use it. "
        "The app server uses them to make API calls."
    )


# ============================================================
# HEADER AND PROGRESS INDICATOR
# ============================================================

st.markdown(
    """
    <div class="brand-row">
        <div class="brand-mark">✦</div>
        <div>
            <div class="brand-name">Find Recruiters</div>
            <div class="brand-tagline">
                Find the right people. Make a meaningful first connection.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


def render_steps(active_step):
    steps = [
        ("1", "Job & Resume", "Add your details"),
        ("2", "Recruiters", "Review your matches"),
        ("3", "Generate Email", "Create your outreach"),
    ]

    columns = st.columns(3)

    for index, (number, title, description) in enumerate(steps, start=1):
        if index < active_step:
            state = "complete"
            shown_number = "✓"
        elif index == active_step:
            state = "active"
            shown_number = number
        else:
            state = ""
            shown_number = number

        with columns[index - 1]:
            st.markdown(
                f"""
                <div class="step-card {state}">
                    <div class="step-circle">{shown_number}</div>
                    <div>
                        <div class="step-title">{title}</div>
                        <div class="step-description">{description}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


render_steps(st.session_state["page"])


# ============================================================
# PAGE 1 — JOB DESCRIPTION AND RESUME
# ============================================================

if st.session_state["page"] == 1:

    st.markdown(
        """
        <div class="hero">
            <div class="hero-eyebrow">Your next opportunity starts here</div>
            <div class="hero-title">
                Turn opportunities<br>
                into <span>conversations.</span>
            </div>
            <p class="hero-description">
                Find recruiters at your target company and create
                personalized, evidence-backed outreach using your
                job description and resume.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    
    with st.container(border=True):
        st.markdown(
            '<div class="section-heading">Job description & resume</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Paste the complete job posting and upload a text-readable
                PDF of your resume. Your API keys are available in the
                sidebar.
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("find_recruiters_form"):
            job_description = st.text_area(
                "Job Description",
                value=st.session_state.get("saved_job_description", ""),
                height=220,
                placeholder=(
                    "Paste the complete job description here, including "
                    "the role, responsibilities, and qualifications..."
                ),
                key="job_description_input",
            )

            uploaded_resume = st.file_uploader(
                "Upload your resume (PDF)",
                type=["pdf"],
                help="Use a text-based PDF rather than a scanned image.",
                key="resume_uploader",
            )

            st.caption(
                "Your resume should contain selectable text so the "
                "application can extract your experience and skills."
            )

            submitted = st.form_submit_button(
                "Find Recruiters  →",
                type="primary",
                use_container_width=True,
            )

    if submitted:
        if not job_description.strip():
            st.error("Please paste a job description.")

        elif not gemini_api_key.strip():
            st.error(
                "Enter your Gemini API key in the sidebar "
                "before finding recruiters."
            )

        else:
            resume_bytes = (
                uploaded_resume.getvalue()
                if uploaded_resume is not None
                else st.session_state.get("saved_resume_bytes")
            )

            if not resume_bytes:
                st.error("Please upload your resume as a PDF.")

            else:
                try:
                    with st.spinner(
                        "Analyzing your job description and resume, "
                        "then finding recruiters..."
                    ):
                        pdf_reader = pypdf.PdfReader(
                            io.BytesIO(resume_bytes)
                        )

                        resume_text = ""

                        for pdf_page in pdf_reader.pages:
                            page_text = pdf_page.extract_text()
                            if page_text:
                                resume_text += page_text + "\n"

                        if not resume_text.strip():
                            st.error(
                                "Could not extract text from this PDF. "
                                "Please upload a text-readable PDF."
                            )
                            st.stop()

                        pipeline = ColdMailPipeline(
                            gemini_api_key=gemini_api_key.strip(),
                            hunter_api_key=hunter_api_key.strip() or None,
                        )

                        result = pipeline.find_recruiters(
                            job_description=job_description,
                            resume_text=resume_text,
                        )

                    if not result or not result.get("recruiters"):
                        st.session_state["pipeline_result"] = None
                        st.session_state["email_result"] = None

                        st.warning(
                            "No recruiters could be found at the moment. "
                            "Please try again later."
                        )

                    else:
                        st.session_state["saved_job_description"] = (
                            job_description
                        )
                        st.session_state["saved_resume_bytes"] = resume_bytes
                        st.session_state["pipeline_result"] = result
                        st.session_state["email_result"] = None

                        st.session_state.pop(
                            "selected_recruiter_index_saved",
                            None,
                        )

                        st.session_state["page"] = 2
                        st.rerun()

                except Exception as error:
                    st.error(
                        "Something went wrong while finding recruiters."
                    )

                    st.caption(
                        "If the error mentions 503 or UNAVAILABLE, "
                        "Gemini may be temporarily overloaded. "
                        "Wait briefly and retry."
                    )

                    with st.expander("Technical details"):
                        st.exception(error)


# ============================================================
# PAGE 2 — RECRUITER SELECTION
# ============================================================

elif st.session_state["page"] == 2:

    result = st.session_state.get("pipeline_result")

    if not result or not result.get("recruiters"):
        st.warning("There are no recruiter results to display.")

        if st.button("Back to Job & Resume", type="primary"):
            st.session_state["page"] = 1
            st.rerun()

    else:
        recruiters = result["recruiters"]

        st.markdown(
            """
            <div class="hero">
                <div class="hero-eyebrow">Step 2 · Your matches</div>
                <div class="hero-title">
                    Meet your <span>recruiters.</span>
                </div>
                <p class="hero-description">
                    Choose a recruiter at your target company.
                    Recruiters are ranked primarily by location match,
                    with recruiter relevance as a secondary factor.
                    Contact information is retrieved only after you
                    make your selection.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(f"{len(recruiters)} recruiter(s) found")

        with st.container(border=True):
            st.markdown(
                '<div class="section-heading">Matched recruiters</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="section-description">
                    Select one person to continue. Contact email addresses
                    are not retrieved or displayed in this list.
                </div>
                """,
                unsafe_allow_html=True,
            )

            def recruiter_label(index):
                recruiter = recruiters[index]
                title = recruiter.title or "Recruiter"
                company = recruiter.company or "Company not listed"
                location = recruiter.location or "Location not listed"

                return (
                    f"{recruiter.name}  ·  {title}  ·  "
                    f"{company}  ·  {location}"
                )

            saved_index = st.session_state.get(
                "selected_recruiter_index_saved",
                0,
            )
            saved_index = min(max(saved_index, 0), len(recruiters) - 1)

            selected_index = st.radio(
                "Select a recruiter",
                options=list(range(len(recruiters))),
                index=saved_index,
                format_func=recruiter_label,
                key="selected_recruiter_index",
                label_visibility="collapsed",
            )

        selected_recruiter = recruiters[selected_index]

        with st.container(border=True):
            st.markdown(
                '<div class="section-heading">Selected recruiter</div>',
                unsafe_allow_html=True,
            )

            st.subheader(selected_recruiter.name)
            st.write(selected_recruiter.title or "Title not available")

            st.write(
                f"**Company:** "
                f"{selected_recruiter.company or 'Not available'}"
            )

            st.write(
                f"**Location:** "
                f"{selected_recruiter.location or 'Not available'}"
            )

            if selected_recruiter.linkedin_url:
                st.markdown(
                    f"[View LinkedIn Profile ↗]"
                    f"({selected_recruiter.linkedin_url})"
                )

        back_col, next_col = st.columns([1, 2])

        with back_col:
            if st.button("← Back", use_container_width=True):
                st.session_state["page"] = 1
                st.rerun()

        with next_col:
            if st.button(
                "Generate Email  →",
                type="primary",
                use_container_width=True,
            ):
                if not gemini_api_key.strip():
                    st.error(
                        "Enter your Gemini API key in the sidebar."
                    )

                elif not hunter_api_key.strip():
                    st.error(
                        "Enter your Hunter API key in the sidebar "
                        "to retrieve recruiter contact information."
                    )

                else:
                    try:
                        with st.spinner(
                            "Finding contact information and generating "
                            "your personalized email..."
                        ):
                            pipeline = ColdMailPipeline(
                                gemini_api_key=gemini_api_key.strip(),
                                hunter_api_key=hunter_api_key.strip(),
                            )

                            email_result = pipeline.generate_email(
                                job=result["job"],
                                candidate=result["candidate"],
                                recruiter=selected_recruiter,
                            )

                        st.session_state["email_result"] = email_result

                        st.session_state[
                            "selected_recruiter_index_saved"
                        ] = selected_index

                        st.session_state["page"] = 3
                        st.rerun()

                    except Exception as error:
                        st.error(
                            "Something went wrong while generating "
                            "the email."
                        )

                        with st.expander("Technical details"):
                            st.exception(error)


# ============================================================
# PAGE 3 — CONTACT DETAILS AND EMAIL
# ============================================================

elif st.session_state["page"] == 3:

    result = st.session_state.get("pipeline_result")
    email_result = st.session_state.get("email_result")

    if not result or not email_result:
        st.warning("Your email results are unavailable.")

        if st.button("Back to Recruiters", type="primary"):
            st.session_state["page"] = 2
            st.rerun()

    else:
        recruiters = result["recruiters"]

        selected_index = st.session_state.get(
            "selected_recruiter_index_saved",
            0,
        )

        selected_index = min(
            max(selected_index, 0),
            len(recruiters) - 1,
        )

        selected_recruiter = recruiters[selected_index]

        st.markdown(
            """
            <div class="hero">
                <div class="hero-eyebrow">Step 3 · Ready for outreach</div>
                <div class="hero-title">
                    Make your first <span>connection.</span>
                </div>
                <p class="hero-description">
                    Review the retrieved contact information, check the
                    resume evidence behind your personalization, and
                    edit your email before downloading it.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        contact = email_result.get("contact")
        email = email_result.get("email")
        evidence = email_result.get("evidence")

        def field_value(obj, field_name, default="Not available"):
            if obj is None:
                return default

            if isinstance(obj, dict):
                value = obj.get(field_name)
            else:
                value = getattr(obj, field_name, None)

            if value is None or value == "":
                return default

            return value

        # ----------------------------------------------------
        # CONTACT CARD
        # ----------------------------------------------------

        with st.container(border=True):
            st.markdown(
                '<div class="section-heading">Recruiter contact</div>',
                unsafe_allow_html=True,
            )

            st.subheader(selected_recruiter.name)

            contact_col1, contact_col2 = st.columns(2)

            with contact_col1:
                st.write(
                    f"**Company:** "
                    f"{selected_recruiter.company or 'Not available'}"
                )

                st.write(
                    f"**Email:** {field_value(contact, 'email')}"
                )

            with contact_col2:
                st.write(
                    f"**Hunter score:** "
                    f"{field_value(contact, 'hunter_score')}"
                )

                st.write(
                    f"**Verification:** "
                    f"{field_value(contact, 'verification_status')}"
                )

            if selected_recruiter.linkedin_url:
                st.markdown(
                    f"[View LinkedIn Profile ↗]"
                    f"({selected_recruiter.linkedin_url})"
                )

        # ----------------------------------------------------
        # RESUME EVIDENCE
        # ----------------------------------------------------

        with st.container(border=True):
            st.markdown(
                '<div class="section-heading">Evidence used</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="section-description">
                    Review how your resume supports the requirements
                    identified in the job description.
                </div>
                """,
                unsafe_allow_html=True,
            )

            matches = field_value(evidence, "matches", default=[])

            if matches:
                for index, match in enumerate(matches, start=1):
                    capability = field_value(
                        match,
                        "capability",
                        "Relevant capability",
                    )

                    with st.expander(
                        f"{index}. {capability}",
                        expanded=(index == 1),
                    ):
                        st.write(
                            "**Evidence:** "
                            f"{field_value(match, 'evidence')}"
                        )

                        st.write(
                            "**Why relevant:** "
                            f"{field_value(match, 'relevance_reason')}"
                        )

                        st.write(
                            "**Score:** "
                            f"{field_value(match, 'score')}"
                        )

            else:
                st.caption("No evidence matches were returned.")

        # ----------------------------------------------------
        # EDITABLE EMAIL
        # ----------------------------------------------------

        with st.container(border=True):
            st.markdown(
                '<div class="section-heading">Your personalized email</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="section-description">
                    Review and edit the email before downloading it.
                </div>
                """,
                unsafe_allow_html=True,
            )

            email_subject = field_value(
                email,
                "subject",
                default="",
            )

            email_body = field_value(
                email,
                "body",
                default="",
            )

            edited_subject = st.text_input(
                "Subject",
                value=email_subject,
                key="edited_email_subject",
            )

            edited_body = st.text_area(
                "Email body",
                value=email_body,
                height=330,
                key="edited_email_body",
            )

            download_text = (
                f"Subject: {edited_subject}\n\n{edited_body}"
            )

            st.download_button(
                label="Download Email  ↓",
                data=download_text,
                file_name="recruiter_outreach_email.txt",
                mime="text/plain",
                type="primary",
                use_container_width=True,
            )

        back_col, restart_col = st.columns(2)

        with back_col:
            if st.button(
                "← Back to Recruiters",
                use_container_width=True,
            ):
                st.session_state["page"] = 2
                st.rerun()

        with restart_col:
            if st.button(
                "Start a New Search",
                type="primary",
                use_container_width=True,
            ):
                st.session_state["page"] = 1
                st.session_state["pipeline_result"] = None
                st.session_state["email_result"] = None

                st.session_state.pop(
                    "selected_recruiter_index_saved",
                    None,
                )

                st.session_state.pop(
                    "saved_job_description",
                    None,
                )

                st.session_state.pop(
                    "saved_resume_bytes",
                    None,
                )

                st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">
        Find Recruiters · Targeted discovery · Evidence-backed outreach
    </div>
    """,
    unsafe_allow_html=True,
)
