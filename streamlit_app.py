
import base64
import html
import io
from urllib.parse import urlsplit

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

for key, default in {
    "page": 1,
    "pipeline_result": None,
    "email_result": None,
    "selected_recruiter_index_saved": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ============================================================
# BACKGROUND
# ============================================================

def create_background_uri():
    svg = """
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1100" viewBox="0 0 1600 1100">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#f8f7ff"/>
          <stop offset="52%" stop-color="#f2f5ff"/>
          <stop offset="100%" stop-color="#fdf5ff"/>
        </linearGradient>
        <radialGradient id="glow">
          <stop offset="0%" stop-color="#c9bbff" stop-opacity=".48"/>
          <stop offset="100%" stop-color="#c9bbff" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="1600" height="1100" fill="url(#bg)"/>
      <ellipse cx="1330" cy="100" rx="520" ry="440" fill="url(#glow)"/>
      <ellipse cx="80" cy="900" rx="520" ry="440" fill="url(#glow)"/>
      <g fill="none" stroke="#8f83ee" stroke-opacity=".13" stroke-width="2" stroke-dasharray="5 12">
        <path d="M950 90 C1170 150 1050 330 1320 350 S1470 560 1250 630"/>
        <path d="M80 500 C300 420 430 580 550 450"/>
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
      <g transform="translate(1320 350) rotate(-12)" fill="#7c68e9" fill-opacity=".12">
        <path d="M0 0 L140 -52 L88 83 L66 25 Z"/>
        <path d="M66 25 L140 -52 L88 83 L77 43 Z" fill-opacity=".2"/>
      </g>
    </svg>
    """
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


background_uri = create_background_uri()


# ============================================================
# CSS
# ============================================================

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html {
    color-scheme: light !important;
}

.stApp {
    background-color: #f6f7ff !important;
    background-image: url("__BG__");
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    color: #18223b !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 1160px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4 {
    color: #202044 !important;
}

[data-testid="stMarkdownContainer"] p {
    color: #475467;
}


/* BRAND */

.brand-row {
    display: flex;
    align-items: center;
    gap: 13px;
    margin-bottom: 10px;
}

.brand-mark {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 14px;
    color: #ffffff !important;
    background: linear-gradient(135deg, #8068f6, #5035d3);
    font-size: 25px;
    font-weight: 800;
    box-shadow: 0 7px 20px rgba(101,72,237,.24);
}

.brand-name {
    font-size: 23px;
    font-weight: 800;
    color: #252447 !important;
    line-height: 1.2;
}

.brand-tagline {
    font-size: 13px;
    color: #737894 !important;
    margin-top: 4px;
}


/* HERO */

.hero {
    padding: 32px 34px;
    margin: 18px 0 22px;
    border: 1px solid #dcdaf8;
    border-radius: 24px;
    background: linear-gradient(120deg, #ffffff, #f8f6ff) !important;
    box-shadow: 0 14px 40px rgba(61,49,121,.07);
}

.hero-eyebrow {
    color: #6548ed !important;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero-title {
    color: #202044 !important;
    font-size: clamp(30px, 4vw, 43px);
    line-height: 1.16;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 0 0 12px;
}

.hero-title span {
    color: #6548ed !important;
}

.hero-description {
    font-size: 15px;
    line-height: 1.7;
    color: #667085 !important;
    max-width: 720px;
    margin: 0;
}


/* PROGRESS INDICATOR */

.step-card {
    min-height: 84px;
    padding: 14px 15px;
    border: 1px solid #e4e5f0;
    border-radius: 15px;
    background: #ffffff !important;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}

.step-card.active {
    background: #f5f2ff !important;
    border-color: #9b8bf5;
}

.step-card.complete {
    background: #f5fff9 !important;
    border-color: #b5e4ce;
}

.step-circle {
    display: flex;
    flex: 0 0 34px;
    height: 34px;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #efedf8;
    color: #6e698b !important;
    font-size: 14px;
    font-weight: 700;
}

.step-card.active .step-circle {
    background: #6548ed;
    color: #ffffff !important;
}

.step-card.complete .step-circle {
    background: #169b62;
    color: #ffffff !important;
}

.step-title {
    font-weight: 700;
    font-size: 13px;
    color: #272642 !important;
}

.step-description {
    margin-top: 4px;
    font-size: 11px;
    color: #777c91 !important;
    line-height: 1.4;
}


/* FEATURES */

.feature-card {
    min-height: 112px;
    padding: 17px 18px;
    border-radius: 17px;
    border: 1px solid #e3e2f3;
    background: #ffffff !important;
    margin-bottom: 18px;
}

.feature-icon {
    font-size: 23px;
    margin-bottom: 8px;
}

.feature-title {
    font-weight: 700;
    font-size: 13px;
    color: #302b52 !important;
    margin-bottom: 4px;
}

.feature-description {
    color: #787b90 !important;
    font-size: 12px;
    line-height: 1.5;
}


/* SECTION HEADINGS */

.section-heading {
    color: #292747 !important;
    font-size: 21px;
    font-weight: 750;
    margin: 3px 0 5px;
}

.section-description {
    color: #72778b !important;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 17px;
}


/* WHITE CONTAINERS */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    border: 1px solid #e3e5ef !important;
    border-radius: 18px !important;
    box-shadow: 0 6px 24px rgba(48,42,96,.055) !important;
}


/* WHITE INPUTS */

.stTextInput input,
.stTextArea textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
input[type="text"],
input[type="password"],
input[type="email"],
textarea {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #18223b !important;
    -webkit-text-fill-color: #18223b !important;
    caret-color: #6548ed !important;
    color-scheme: light !important;
    border-color: #dedcf2 !important;
}

[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div {
    background: #ffffff !important;
    border-color: #dedcf2 !important;
}

input::placeholder,
textarea::placeholder {
    color: #98a2b3 !important;
    -webkit-text-fill-color: #98a2b3 !important;
    opacity: 1 !important;
}

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p {
    color: #344054 !important;
    -webkit-text-fill-color: #344054 !important;
}


/* RECRUITER CARD TEXT */

.recruiter-name {
    color: #6548ed !important;
    font-size: 17px;
    font-weight: 800;
    line-height: 1.4;
    margin: 0 0 5px 0;
}

.recruiter-title {
    color: #344054 !important;
    font-size: 14px;
    line-height: 1.5;
    margin-bottom: 5px;
}

.recruiter-meta {
    color: #667085 !important;
    font-size: 12px;
    line-height: 1.7;
}

.selected-label {
    color: #6548ed !important;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .7px;
    margin-bottom: 5px;
}

.recruiter-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 13px;
    background: linear-gradient(135deg, #8068f6, #593ce0);
    color: #ffffff !important;
    font-size: 14px;
    font-weight: 800;
}

.linkedin-link {
    color: #6548ed !important;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none !important;
}


/* FILE UPLOADER */

[data-testid="stFileUploader"] section {
    background: #ffffff !important;
    border-color: #dcd8f0 !important;
}

[data-testid="stFileUploader"] section *,
[data-testid="stFileUploader"] button {
    color: #344054 !important;
}


/* PRIMARY BUTTONS */

div.stButton > button[kind="primary"],
div.stFormSubmitButton > button,
div.stDownloadButton > button,
div.stLinkButton > a,
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: linear-gradient(110deg, #765cf4, #593ce0) !important;
    background-color: #6548ed !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #6548ed !important;
    border-radius: 12px !important;
    min-height: 44px;
    font-weight: 700 !important;
    box-shadow: 0 7px 18px rgba(101,72,237,.13) !important;
}

div.stButton > button[kind="primary"] *,
div.stFormSubmitButton > button *,
div.stDownloadButton > button *,
button[data-testid="stBaseButton-primary"] *,
button[data-testid="stBaseButton-primaryFormSubmit"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 700 !important;
}


/* SECONDARY BUTTONS */

div.stButton > button[kind="secondary"],
button[data-testid="stBaseButton-secondary"] {
    background: #ffffff !important;
    color: #4c3bb5 !important;
    -webkit-text-fill-color: #4c3bb5 !important;
    border: 1px solid #dedcf2 !important;
    border-radius: 12px !important;
    min-height: 44px;
    font-weight: 500 !important;
    box-shadow: none !important;
}

div.stButton > button[kind="secondary"] *,
button[data-testid="stBaseButton-secondary"] * {
    color: #4c3bb5 !important;
    -webkit-text-fill-color: #4c3bb5 !important;
    font-weight: 500 !important;
}


/* SIDEBAR */

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #faf9ff !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #344054 !important;
}

[data-testid="stSidebar"] a {
    color: #593ce0 !important;
}


/* FOOTER */

.footer-note {
    text-align: center;
    color: #83869a !important;
    font-size: 11px;
    margin-top: 32px;
    padding: 15px;
}

@media (max-width: 700px) {
    .hero {
        padding: 24px 20px;
    }

    .brand-name {
        font-size: 20px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
"""

st.markdown(
    f"<style>\n{CSS.replace('__BG__', background_uri)}\n</style>",
    unsafe_allow_html=True,
)


# ============================================================
# API KEY SIDEBAR
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
# APP HEADER
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

    for index, (number, title, description) in enumerate(
        steps, start=1
    ):
        if index < active_step:
            state, shown_number = "complete", "✓"
        elif index == active_step:
            state, shown_number = "active", number
        else:
            state, shown_number = "", number

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
            Find recruiters at your target company and create personalized,
            evidence-backed outreach using your job description and resume.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    features = [
        ("⌕", "Relevant recruiters",
         "Discover recruiters at the company you are targeting."),
        ("▤", "Evidence-backed emails",
         "Connect job requirements to experience on your resume."),
        ("↗", "Less manual work",
         "Research recruiters and prepare outreach in one workflow."),
    ]

    feature_columns = st.columns(3)

    for column, (icon, title, description) in zip(
        feature_columns, features
    ):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.container(border=True):
        st.markdown(
            '<div class="section-heading">Job description &amp; resume</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Paste the complete job posting and upload a text-readable PDF
                of your resume. Your API keys are available in the sidebar.
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
                "Find Recruiters →",
                type="primary",
                use_container_width=True,
            )

    if submitted:
        if not job_description.strip():
            st.error("Please paste a job description.")
        elif not gemini_api_key.strip():
            st.error("Enter your Gemini API key in the sidebar.")
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
                        reader = pypdf.PdfReader(
                            io.BytesIO(resume_bytes)
                        )
                        resume_parts = []

                        for pdf_page in reader.pages:
                            page_text = pdf_page.extract_text()
                            if page_text:
                                resume_parts.append(page_text)

                        resume_text = "\n".join(resume_parts)

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
                        st.session_state["saved_job_description"] = job_description
                        st.session_state["saved_resume_bytes"] = resume_bytes
                        st.session_state["pipeline_result"] = result
                        st.session_state["email_result"] = None
                        st.session_state["selected_recruiter_index_saved"] = 0
                        st.session_state.pop("edited_email_subject", None)
                        st.session_state.pop("edited_email_body", None)
                        st.session_state["page"] = 2
                        st.rerun()

                except Exception as error:
                    st.error(
                        "Something went wrong while finding recruiters."
                    )
                    with st.expander("Technical details"):
                        st.exception(error)


# ============================================================
# PAGE 2 — NATIVE STREAMLIT RECRUITER CARDS
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
                Select a recruiter to continue. Results are ranked primarily
                by location match, with recruiter relevance as a secondary
                factor. Contact information is retrieved after selection.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(f"{len(recruiters)} recruiter(s) found")
        st.markdown(
            '<div class="section-heading">Choose a recruiter</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-description">'
            'Use the circle to select a recruiter. Click the LinkedIn button '
            'to open their profile separately.'
            '</div>',
            unsafe_allow_html=True,
        )

        selected_index = int(
            st.session_state.get("selected_recruiter_index_saved", 0)
        )
        selected_index = max(
            0,
            min(selected_index, len(recruiters) - 1),
        )

        def valid_linkedin_url(value):
            if not value:
                return None
            try:
                parsed = urlsplit(str(value).strip())
            except ValueError:
                return None

            host = (parsed.hostname or "").lower()

            if (
                parsed.scheme in ("https", "http")
                and (
                    host == "linkedin.com"
                    or host.endswith(".linkedin.com")
                )
            ):
                return parsed.geturl()

            return None

        # Each card uses native Streamlit controls, not a multiline
        # HTML block. The LinkedIn control is a separate link button.

        for index, recruiter in enumerate(recruiters):
            is_selected = index == selected_index

            with st.container(border=True):
                selector_col, details_col, link_col = st.columns(
                    [0.45, 5.2, 1.7]
                )

                with selector_col:
                    selector_label = "◉" if is_selected else "○"
                    selector_type = (
                        "primary" if is_selected else "secondary"
                    )

                    if st.button(
                        selector_label,
                        key=f"select_recruiter_{index}",
                        type=selector_type,
                        help="Select this recruiter",
                    ):
                        st.session_state[
                            "selected_recruiter_index_saved"
                        ] = index
                        st.rerun()

                with details_col:
                    if is_selected:
                        st.markdown(
                            '<div class="selected-label">✓ Selected</div>',
                            unsafe_allow_html=True,
                        )

                    name = str(recruiter.name or "Recruiter")
                    safe_name = html.escape(name)

                    st.markdown(
                        f'<p class="recruiter-name">{safe_name}</p>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f'<div class="recruiter-title">'
                        f'{html.escape(str(recruiter.title or "Recruiter"))}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    company = html.escape(
                        str(recruiter.company or "Company not listed")
                    )
                    location = html.escape(
                        str(recruiter.location or "Location not listed")
                    )

                    st.markdown(
                        f'<div class="recruiter-meta">'
                        f'<strong>Company:</strong> {company}'
                        f' &nbsp; · &nbsp; '
                        f'<strong>Location:</strong> {location}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                with link_col:
                    linkedin_url = valid_linkedin_url(
                        getattr(recruiter, "linkedin_url", None)
                    )

                    if linkedin_url:
                        st.link_button(
                            "View LinkedIn ↗",
                            linkedin_url,
                            use_container_width=True,
                        )
                    else:
                        st.caption("LinkedIn unavailable")

        selected_recruiter = recruiters[selected_index]

        st.session_state[
            "selected_recruiter_index_saved"
        ] = selected_index

        back_col, next_col = st.columns([1, 2])

        with back_col:
            if st.button(
                "← Back",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state["page"] = 1
                st.rerun()

        with next_col:
            if st.button(
                "Generate Email →",
                type="primary",
                use_container_width=True,
            ):
                if not gemini_api_key.strip():
                    st.error("Enter your Gemini API key in the sidebar.")
                elif not hunter_api_key.strip():
                    st.error(
                        "Enter your Hunter API key in the sidebar "
                        "to retrieve contact information."
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
                            "Something went wrong while generating the email."
                        )
                        with st.expander("Technical details"):
                            st.exception(error)


# ============================================================
# PAGE 3 — CONTACT, EVIDENCE AND EMAIL
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
        selected_index = int(
            st.session_state.get("selected_recruiter_index_saved", 0)
        )
        selected_index = max(
            0,
            min(selected_index, len(recruiters) - 1),
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
                Review the contact information and resume evidence, then
                edit your personalized email before downloading.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        def field_value(obj, field_name, default="Not available"):
            if obj is None:
                return default
            if isinstance(obj, dict):
                value = obj.get(field_name)
            else:
                value = getattr(obj, field_name, None)
            return default if value is None or value == "" else value

        contact = field_value(email_result, "contact", default=None)
        email = field_value(email_result, "email", default=None)
        evidence = field_value(email_result, "evidence", default=None)

        with st.container(border=True):
            st.markdown(
                '<div class="section-heading">Recruiter contact</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p class="recruiter-name">'
                f'{html.escape(str(selected_recruiter.name))}</p>',
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"**Company:** "
                    f"{selected_recruiter.company or 'Not available'}"
                )
                st.write(f"**Email:** {field_value(contact, 'email')}")

            with col2:
                st.write(
                    f"**Hunter score:** {field_value(contact, 'hunter_score')}"
                )
                st.write(
                    f"**Verification:** "
                    f"{field_value(contact, 'verification_status')}"
                )

            linkedin_url = valid_linkedin_url(
                getattr(selected_recruiter, "linkedin_url", None)
            )
            if linkedin_url:
                st.link_button(
                    "View LinkedIn Profile ↗",
                    linkedin_url,
                )

        with st.container(border=True):
            st.markdown(
                '<div class="section-heading">Evidence used</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="section-description">'
                'Review how your resume supports the job requirements.'
                '</div>',
                unsafe_allow_html=True,
            )

            matches = field_value(evidence, "matches", default=[])

            if matches:
                for index, match in enumerate(matches, start=1):
                    capability = field_value(
                        match, "capability", "Relevant capability"
                    )
                    with st.expander(
                        f"{index}. {capability}",
                        expanded=(index == 1),
                    ):
                        st.write(
                            f"**Evidence:** {field_value(match, 'evidence')}"
                        )
                        st.write(
                            f"**Why relevant:** "
                            f"{field_value(match, 'relevance_reason')}"
                        )
                        st.write(
                            f"**Score:** {field_value(match, 'score')}"
                        )
            else:
                st.caption("No evidence matches were returned.")

        with st.container(border=True):
            st.markdown(
                '<div class="section-heading">Your personalized email</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="section-description">'
                'Review and edit the email before downloading it.'
                '</div>',
                unsafe_allow_html=True,
            )

            email_subject = field_value(email, "subject", default="")
            email_body = field_value(email, "body", default="")

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

            st.download_button(
                label="Download Email ↓",
                data=f"Subject: {edited_subject}\n\n{edited_body}",
                file_name="recruiter_outreach_email.txt",
                mime="text/plain",
                type="primary",
                use_container_width=True,
            )

        back_col, restart_col = st.columns(2)

        with back_col:
            if st.button(
                "← Back to Recruiters",
                type="secondary",
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

                for key in (
                    "selected_recruiter_index_saved",
                    "saved_job_description",
                    "saved_resume_bytes",
                    "edited_email_subject",
                    "edited_email_body",
                ):
                    st.session_state.pop(key, None)

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
