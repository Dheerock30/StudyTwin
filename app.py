import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from analyzer import analyze_code
from database import (
    initialize_database,
    save_submission,
    get_history
)
from twin import (
    calculate_twin,
    get_skill_level
)
from recommender import generate_recommendations
from ai_mentor import get_ai_feedback


# ============================================================
# SETUP
# ============================================================

load_dotenv()
initialize_database()

st.set_page_config(
    page_title="StudyTwin",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "last_recommendations" not in st.session_state:
    st.session_state.last_recommendations = None

if "last_ai_feedback" not in st.session_state:
    st.session_state.last_ai_feedback = None


# ============================================================
# LIGHT CUSTOM CSS
# IMPORTANT: CSS ONLY — NO HTML
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background-color: #0e1117;
        }

        [data-testid="stSidebar"] {
            background-color: #11151c;
        }

        .main-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            color: #9aa4b2;
            font-size: 1.05rem;
            margin-bottom: 2rem;
        }

        .small-muted {
            color: #8b949e;
            font-size: 0.85rem;
        }

        .section-space {
            margin-top: 1.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("StudyTwin")

    st.caption("Developer Intelligence System")

    st.divider()

    st.subheader("Developer")

    user_id = st.text_input(
        "Your name",
        value="demo_user"
    )

    st.divider()

    st.caption("How it works")

    st.write(
        "StudyTwin analyzes your Python code, "
        "tracks debugging and complexity patterns, "
        "and builds a profile that evolves over time."
    )

    st.divider()

    st.caption("Stack")

    st.write(
        "Python • AST • SQLite • Streamlit • AI"
    )


# ============================================================
# GET USER DATA
# ============================================================

history = get_history(user_id)

twin = calculate_twin(history)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">StudyTwin</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your personal developer intelligence system'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TABS
# ============================================================

overview_tab, code_tab, ai_tab, history_tab = st.tabs(
    [
        "Overview",
        "Code Lab",
        "AI Mentor",
        "History"
    ]
)


# ============================================================
# OVERVIEW TAB
# ============================================================

with overview_tab:

    st.header("Your Developer Twin")

    st.caption(
        "Your profile becomes more meaningful as you analyze more code."
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Debugging",
            f"{twin['debugging']}/100"
        )

    with col2:
        st.metric(
            "Code Efficiency",
            f"{twin['complexity']}/100"
        )

    with col3:
        st.metric(
            "Analyses",
            twin["submissions"]
        )

    with col4:

        if twin["debugging"] < twin["complexity"]:
            focus = "Debugging"
        elif twin["complexity"] < twin["debugging"]:
            focus = "Efficiency"
        else:
            focus = "Balanced"

        st.metric(
            "Current Focus",
            focus
        )

    st.divider()

    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("Debugging proficiency")

        st.progress(
            min(max(int(twin["debugging"]), 0), 100)
        )

        st.write(
            get_skill_level(twin["debugging"])
        )

    with right:

        st.subheader("Code efficiency")

        st.progress(
            min(max(int(twin["complexity"]), 0), 100)
        )

        st.write(
            get_skill_level(twin["complexity"])
        )

    st.divider()

    # --------------------------------------------------------
    # CURRENT INSIGHT
    # --------------------------------------------------------

    st.subheader("Current insight")

    if twin["submissions"] == 0:

        st.info(
            "Your Developer Twin hasn't learned anything yet. "
            "Go to Code Lab and analyze your first Python program."
        )

    elif twin["complexity"] < twin["debugging"]:

        st.warning(
            "Your debugging profile is currently stronger than "
            "your code-efficiency profile. Focus on nested loops "
            "and Big-O concepts."
        )

    elif twin["debugging"] < twin["complexity"]:

        st.warning(
            "Your code-efficiency profile is currently stronger "
            "than your debugging profile. Focus on Python errors, "
            "tracebacks, and debugging techniques."
        )

    else:

        st.success(
            "Your debugging and code-efficiency skills are "
            "currently balanced."
        )

    st.info(
        "The more submissions you analyze, the more your "
        "Developer Twin can identify recurring patterns."
    )


# ============================================================
# CODE LAB TAB
# ============================================================

with code_tab:

    st.header("Code Lab")

    st.caption(
        "Paste Python code to analyze debugging patterns "
        "and estimated algorithmic complexity."
    )

    # --------------------------------------------------------
    # SAMPLE CODE BUTTON
    # --------------------------------------------------------

    sample1 = """def find_common(numbers1, numbers2):
    common = []

    for x in numbers1:
        for y in numbers2:
            if x == y:
                common.append(x)

    return common
"""

    sample2 = """def find_max(numbers):
    maximum = numbers[0]

    for number in numbers:
        if number > maximum:
            maximum = number

    return maximum
"""

    sample3 = """def calculate_sum(numbers)

    total = 0

    for number in numbers:
        total += number

    return total
"""

    sample_col1, sample_col2, sample_col3 = st.columns(3)

    with sample_col1:
        if st.button("Load O(n²) example"):
            st.session_state.sample_code = sample1

    with sample_col2:
        if st.button("Load O(n) example"):
            st.session_state.sample_code = sample2

    with sample_col3:
        if st.button("Load debugging example"):
            st.session_state.sample_code = sample3

    if "sample_code" not in st.session_state:
        st.session_state.sample_code = sample1

    # --------------------------------------------------------
    # CODE INPUT
    # --------------------------------------------------------

    code = st.text_area(
        "Python code",
        value=st.session_state.sample_code,
        height=360
    )

    analyze_button = st.button(
        "Analyze Code",
        type="primary",
        use_container_width=True
    )

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    if analyze_button:

        if not code.strip():

            st.warning(
                "Please enter some Python code first."
            )

        else:

            with st.spinner(
                "StudyTwin is analyzing your code..."
            ):

                result = analyze_code(code)

                debugging = result["debugging"]
                complexity = result["complexity"]

                save_submission(
                    user_id=user_id,
                    code=code,
                    debugging_score=result["debugging_score"],
                    complexity_score=result["complexity_score"],
                    complexity=complexity["complexity"],
                    issues=debugging["issues"]
                )

                updated_history = get_history(user_id)

                updated_twin = calculate_twin(
                    updated_history
                )

                recommendations = generate_recommendations(
                    updated_twin
                )

                st.session_state.last_analysis = {
                    "result": result,
                    "twin": updated_twin
                }

                st.session_state.last_recommendations = (
                    recommendations
                )

                st.session_state.last_ai_feedback = None

            st.success(
                "Analysis complete. Your Developer Twin was updated."
            )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if st.session_state.last_analysis:

        data = st.session_state.last_analysis

        result = data["result"]

        debugging = result["debugging"]

        complexity = result["complexity"]

        st.divider()

        st.subheader("Analysis results")

        # ================================================
        # DEBUGGING
        # ================================================

        debug_col, complexity_col = st.columns(2)

        with debug_col:

            st.markdown("#### Debugging")

            if debugging["syntax_valid"]:

                st.success("Syntax is valid.")

                if debugging["issues"]:

                    for issue in debugging["issues"]:

                        st.warning(issue)

                else:

                    st.write(
                        "No obvious debugging issues detected."
                    )

            else:

                error = debugging["syntax_error"]

                st.error(
                    f"Line {error['line']}: {error['message']}"
                )

        # ================================================
        # COMPLEXITY
        # ================================================

        with complexity_col:

            st.markdown("#### Complexity")

            metric_col1, metric_col2 = st.columns(2)

            with metric_col1:

                st.metric(
                    "Estimated Big-O",
                    complexity["complexity"]
                )

            with metric_col2:

                st.metric(
                    "Loop depth",
                    complexity["max_loop_depth"]
                )

            st.write(
                f"Loops detected: {complexity['loop_count']}"
            )

            if complexity["max_loop_depth"] >= 2:

                st.warning(
                    complexity["message"]
                )

            else:

                st.success(
                    complexity["message"]
                )

        # ================================================
        # SCORES
        # ================================================

        st.divider()

        score_col1, score_col2 = st.columns(2)

        with score_col1:

            st.write(
                "Debugging score"
            )

            st.progress(
                result["debugging_score"]
            )

            st.write(
                f"{result['debugging_score']}/100"
            )

        with score_col2:

            st.write(
                "Complexity score"
            )

            st.progress(
                result["complexity_score"]
            )

            st.write(
                f"{result['complexity_score']}/100"
            )

        # ================================================
        # RECOMMENDATION
        # ================================================

        st.divider()

        st.subheader("What should you work on next?")

        recommendations = (
            st.session_state.last_recommendations
        )

        for recommendation in recommendations:

            if recommendation["priority"] == "High":

                st.error(
                    f"{recommendation['skill']}\n\n"
                    f"{recommendation['message']}"
                )

            elif recommendation["priority"] == "Medium":

                st.warning(
                    f"{recommendation['skill']}\n\n"
                    f"{recommendation['message']}"
                )

            else:

                st.success(
                    f"{recommendation['skill']}\n\n"
                    f"{recommendation['message']}"
                )


# ============================================================
# AI MENTOR TAB
# ============================================================

with ai_tab:

    st.header("AI Mentor")

    st.caption(
        "Your AI mentor uses your Developer Twin to provide "
        "personalized guidance."
    )

    current_history = get_history(user_id)

    current_twin = calculate_twin(
        current_history
    )

    if current_twin["submissions"] == 0:

        st.info(
            "Analyze at least one piece of code first. "
            "Your AI Mentor needs your coding history."
        )

    else:

        st.subheader("Current Developer Twin")

        ai_col1, ai_col2, ai_col3 = st.columns(3)

        with ai_col1:

            st.metric(
                "Debugging",
                f"{current_twin['debugging']}/100"
            )

        with ai_col2:

            st.metric(
                "Efficiency",
                f"{current_twin['complexity']}/100"
            )

        with ai_col3:

            st.metric(
                "Submissions",
                current_twin["submissions"]
            )

        st.divider()

        if st.button(
            "Generate AI Feedback",
            type="primary"
        ):

            recommendations = generate_recommendations(
                current_twin
            )

            with st.spinner(
                "AI Mentor is studying your profile..."
            ):

                feedback = get_ai_feedback(
                    current_twin,
                    recommendations
                )

            st.session_state.last_ai_feedback = feedback

        if st.session_state.last_ai_feedback:

            st.subheader("Your personalized feedback")

            st.write(
                st.session_state.last_ai_feedback
            )

        else:

            st.info(
                "Click 'Generate AI Feedback' to get "
                "personalized guidance."
            )


# ============================================================
# HISTORY TAB
# ============================================================

with history_tab:

    st.header("Developer History")

    st.caption(
        "Your coding history shows how your Developer Twin evolves."
    )

    current_history = get_history(user_id)

    if current_history:

        dataframe = pd.DataFrame(
            current_history,
            columns=[
                "ID",
                "Debugging",
                "Complexity",
                "Big-O",
                "Issues",
                "Date"
            ]
        )

        # ---------------------------------------------
        # SUMMARY
        # ---------------------------------------------

        hist_col1, hist_col2, hist_col3 = st.columns(3)

        with hist_col1:

            st.metric(
                "Submissions",
                len(dataframe)
            )

        with hist_col2:

            st.metric(
                "Average Debugging",
                f"{dataframe['Debugging'].mean():.0f}/100"
            )

        with hist_col3:

            st.metric(
                "Average Efficiency",
                f"{dataframe['Complexity'].mean():.0f}/100"
            )

        st.divider()

        # ---------------------------------------------
        # CHART
        # ---------------------------------------------

        st.subheader("Skill progression")

        chart_data = dataframe[
            ["Debugging", "Complexity"]
        ]

        st.line_chart(
            chart_data,
            height=350
        )

        st.divider()

        # ---------------------------------------------
        # TABLE
        # ---------------------------------------------

        st.subheader("Submission history")

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No submissions yet. Start by analyzing code in Code Lab."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "StudyTwin • Static Code Analysis • Developer Profiling • AI Mentor"
)