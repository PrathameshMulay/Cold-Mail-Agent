import streamlit as st
import io
import pypdf

from app.workflow.pipeline import ColdMailPipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Find Recruiters",
    page_icon="✉️",
    layout="wide",
)


# ============================================================
# PIPELINE
# ============================================================

@st.cache_resource
def get_pipeline():

    return ColdMailPipeline()


pipeline = get_pipeline()


# ============================================================
# HEADER
# ============================================================

st.title("Cold Mail Agent")

st.write(
    "Find relevant recruiters and generate a personalized "
    "cold email."
)

st.divider()


# ============================================================
# INPUTS
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Job Description")

    job_description = st.text_area(
        "Paste the job description",
        height=500,
        placeholder="Paste the complete job description here...",
        label_visibility="collapsed",
    )


with col2:

    st.subheader("Resume")

    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Upload your resume as a PDF.",
        label_visibility="collapsed",
    )


st.divider()


# ============================================================
# FIND RECRUITERS
# ============================================================

if st.button(
    "Find Recruiters",
    type="primary",
    use_container_width=True,
):

    # --------------------------------------------------------
    # Validate job description
    # --------------------------------------------------------

    if not job_description.strip():

        st.error(
            "Please paste a job description."
        )

    # --------------------------------------------------------
    # Validate resume
    # --------------------------------------------------------

    elif uploaded_resume is None:

        st.error(
            "Please upload your resume."
        )

    else:

        try:

            with st.spinner(
                "Analyzing job, resume, and finding recruiters..."
            ):

                # ==================================================
                # EXTRACT TEXT FROM PDF
                # ==================================================

                pdf_reader = pypdf.PdfReader(
                    io.BytesIO(
                        uploaded_resume.getvalue()
                    )
                )

                resume_text = ""

                for page in pdf_reader.pages:

                    text = page.extract_text()

                    if text:

                        resume_text += (
                            text + "\n"
                        )

                # --------------------------------------------------
                # Make sure text was actually extracted
                # --------------------------------------------------

                if not resume_text.strip():

                    st.error(
                        "Could not extract text from the uploaded "
                        "PDF. Please upload a text-based PDF."
                    )

                    st.stop()

                # ==================================================
                # RUN RECRUITER DISCOVERY
                # ==================================================

                result = pipeline.find_recruiters(
                    job_description=job_description,
                    resume_text=resume_text,
                )

            # ==================================================
            # HANDLE NO RECRUITERS
            # ==================================================

            if not result or not result.get("recruiters"):

                st.session_state.pop(
                    "pipeline_result",
                    None,
                )

                st.session_state.pop(
                    "email_result",
                    None,
                )

                st.warning(
                    "No recruiters could be found at the moment. "
                    "Please try again later."
                )

            else:

                # ------------------------------------------------
                # Store results in session state
                # ------------------------------------------------

                st.session_state["pipeline_result"] = result

                # ------------------------------------------------
                # Clear previously generated email
                # ------------------------------------------------

                st.session_state.pop(
                    "email_result",
                    None,
                )

                st.success(
                    f"Found {len(result['recruiters'])} recruiters."
                )

        except Exception as e:

            st.error(
                "Something went wrong while finding recruiters."
            )

            st.exception(e)


# ============================================================
# DISPLAY RECRUITERS
# ============================================================

if "pipeline_result" in st.session_state:

    result = st.session_state["pipeline_result"]

    recruiters = result["recruiters"]

    st.divider()

    st.header("Recruiters")

    st.write(
        "Recruiters are ranked primarily by job-location match, "
        "with recruiter relevance as a secondary factor."
    )

    # --------------------------------------------------------
    # Radio options
    # --------------------------------------------------------

    recruiter_options = []

    for recruiter in recruiters:

        recruiter_options.append(
            (
                recruiter.name,
                recruiter,
            )
        )

    selected_name = st.radio(
        "Select a recruiter",
        options=[
            name
            for name, recruiter in recruiter_options
        ],
        index=0,
    )

    # --------------------------------------------------------
    # Find selected recruiter
    # --------------------------------------------------------

    selected_recruiter = next(
        recruiter
        for name, recruiter in recruiter_options
        if name == selected_name
    )

    # ========================================================
    # DISPLAY SELECTED RECRUITER
    # ========================================================

    st.subheader("Selected Recruiter")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.write(
            f"**Name:** {selected_recruiter.name}"
        )

        st.write(
            f"**Title:** "
            f"{selected_recruiter.title or 'Not available'}"
        )

        st.write(
            f"**Company:** "
            f"{selected_recruiter.company or 'Not available'}"
        )

    with info_col2:

        st.write(
            f"**Location:** "
            f"{selected_recruiter.location or 'Not available'}"
        )

        if selected_recruiter.linkedin_url:

            st.markdown(
                f"[View LinkedIn Profile]"
                f"({selected_recruiter.linkedin_url})"
            )


    # ========================================================
    # GENERATE EMAIL
    # ========================================================

    st.divider()

    if st.button(
        "Generate Email",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Finding email and generating personalized message..."
            ):

                email_result = pipeline.generate_email(
                    job=result["job"],
                    candidate=result["candidate"],
                    recruiter=selected_recruiter,
                )

            st.session_state["email_result"] = email_result

        except Exception as e:

            st.error(
                "Something went wrong while generating the email."
            )

            st.exception(e)


# ============================================================
# EMAIL RESULT
# ============================================================

if "email_result" in st.session_state:

    email_result = st.session_state["email_result"]

    contact = email_result["contact"]
    email = email_result["email"]
    evidence = email_result["evidence"]

    st.divider()

    st.header("Recruiter Contact")

    contact_col1, contact_col2, contact_col3 = st.columns(3)

    with contact_col1:

        st.write(
            f"**Email:** {contact.email}"
        )

    with contact_col2:

        st.write(
            f"**Hunter Score:** {contact.hunter_score}"
        )

    with contact_col3:

        st.write(
            f"**Verification:** "
            f"{contact.verification_status}"
        )


    # ========================================================
    # EVIDENCE
    # ========================================================

    st.divider()

    st.header("Evidence Used")

    for i, match in enumerate(
        evidence.matches,
        start=1,
    ):

        with st.expander(
            f"{i}. {match.capability}",
            expanded=True,
        ):

            st.write(
                f"**Evidence:** {match.evidence}"
            )

            st.write(
                f"**Why relevant:** "
                f"{match.relevance_reason}"
            )

            st.write(
                f"**Score:** {match.score}"
            )


    # ========================================================
    # EMAIL
    # ========================================================

    st.divider()

    st.header("Generated Email")

    st.subheader("Subject")

    st.text_input(
        "Email subject",
        value=email.subject,
        label_visibility="collapsed",
    )

    st.subheader("Body")

    st.text_area(
        "Email body",
        value=email.body,
        height=500,
        label_visibility="collapsed",
    )

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    st.download_button(
        label="Download Email",
        data=(
            f"Subject: {email.subject}\n\n"
            f"{email.body}"
        ),
        file_name="cold_email.txt",
        mime="text/plain",
        use_container_width=True,
    )