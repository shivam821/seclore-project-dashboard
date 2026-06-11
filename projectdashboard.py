# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import ollama

# # ==================================================
# # PAGE CONFIG
# # ==================================================

# st.set_page_config(
#     page_title="Project Portfolio Dashboard",
#     page_icon="📊",
#     layout="wide"
# )

# # ==================================================
# # LOAD DATA
# # ==================================================

# @st.cache_data
# def load_data():
#     df = pd.read_csv("ProjectAllProjectsDashboard.csv")
#     df.columns = df.columns.str.strip()
#     return df

# df = load_data()

# # ==================================================
# # COLUMN NAMES FROM YOUR CSV
# # ==================================================

# PROJECT_COL = "Name"
# TC_COL = "Technical consultant"
# STATE_COL = "State"
# PRIORITY_COL = "Priority"
# DELAY_COL = "Delay(In days)"
# GEOGRAPHY_COL = "Geography"
# EFFORT_COL = "Actual Effort"

# # ==================================================
# # DATA CLEANING
# # ==================================================

# if DELAY_COL in df.columns:
#     df[DELAY_COL] = pd.to_numeric(
#         df[DELAY_COL],
#         errors="coerce"
#     ).fillna(0)

# # ==================================================
# # SIDEBAR FILTERS
# # ==================================================

# st.sidebar.title("Filters")

# filtered_df = df.copy()

# selected_tc = st.sidebar.multiselect(
#     "Technical Consultant",
#     sorted(df[TC_COL].dropna().astype(str).unique())
# )

# selected_geo = st.sidebar.multiselect(
#     "Geography",
#     sorted(df[GEOGRAPHY_COL].dropna().astype(str).unique())
# )

# selected_priority = st.sidebar.multiselect(
#     "Priority",
#     sorted(df[PRIORITY_COL].dropna().astype(str).unique())
# )

# if selected_tc:
#     filtered_df = filtered_df[
#         filtered_df[TC_COL].astype(str).isin(selected_tc)
#     ]

# if selected_geo:
#     filtered_df = filtered_df[
#         filtered_df[GEOGRAPHY_COL].astype(str).isin(selected_geo)
#     ]

# if selected_priority:
#     filtered_df = filtered_df[
#         filtered_df[PRIORITY_COL].astype(str).isin(selected_priority)
#     ]

# # ==================================================
# # KPI SECTION
# # ==================================================

# total_projects = len(filtered_df)

# active_projects = len(
#     filtered_df[
#         filtered_df[STATE_COL].isin(
#             [
#                 "In Progress",
#                 "To Be Initiated"
#             ]
#         )
#     ]
# )

# on_hold_projects = len(
#     filtered_df[
#         filtered_df[STATE_COL] == "On Hold"
#     ]
# )

# completed_projects = len(
#     filtered_df[
#         filtered_df[STATE_COL] == "Complete"
#     ]
# )

# total_consultants = (
#     filtered_df[TC_COL]
#     .nunique()
# )

# avg_delay = round(
#     filtered_df[DELAY_COL].mean(),
#     1
# )

# # ==================================================
# # HEADER
# # ==================================================

# st.title("📊 Project Portfolio Dashboard")

# c1, c2, c3, c4, c5, c6 = st.columns(6)

# c1.metric("Projects", total_projects)
# c2.metric("Active", active_projects)
# c3.metric("On Hold", on_hold_projects)
# c4.metric("Completed", completed_projects)
# c5.metric("Consultants", total_consultants)
# c6.metric("Avg Delay", avg_delay)

# st.divider()

# # ==================================================
# # CHARTS
# # ==================================================

# left, right = st.columns(2)

# with left:

#     state_count = (
#         filtered_df[STATE_COL]
#         .value_counts()
#         .reset_index()
#     )

#     state_count.columns = ["State", "Count"]

#     fig = px.pie(
#         state_count,
#         names="State",
#         values="Count",
#         title="Projects by State"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

# with right:

#     geo_count = (
#         filtered_df[GEOGRAPHY_COL]
#         .value_counts()
#         .head(10)
#         .reset_index()
#     )

#     geo_count.columns = ["Geography", "Count"]

#     fig = px.bar(
#         geo_count,
#         x="Geography",
#         y="Count",
#         title="Projects by Geography"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

# # ==================================================
# # TABS
# # ==================================================

# tab1, tab2, tab3, tab4 = st.tabs(
#     [
#         "🚀 Ongoing Projects",
#         "⏸️ On Hold Projects",
#         "👨‍💻 TC Workload",
#         "🤖 Ask AI"
#     ]
# )

# # ==================================================
# # TAB 1 - ONGOING PROJECTS
# # ==================================================

# with tab1:

#     st.subheader("Ongoing Projects")

#     ongoing_df = filtered_df[
#         filtered_df[STATE_COL].isin(
#             [
#                 "In Progress",
#                 "To Be Initiated"
#             ]
#         )
#     ]

#     st.metric(
#         "Total Ongoing Projects",
#         len(ongoing_df)
#     )

#     st.dataframe(
#         ongoing_df,
#         use_container_width=True,
#         height=600
#     )

# # ==================================================
# # TAB 2 - ON HOLD
# # ==================================================

# with tab2:

#     st.subheader("On Hold Projects")

#     hold_df = filtered_df[
#         filtered_df[STATE_COL] == "On Hold"
#     ]

#     st.metric(
#         "Projects On Hold",
#         len(hold_df)
#     )

#     st.dataframe(
#         hold_df,
#         use_container_width=True,
#         height=600
#     )

# # ==================================================
# # TAB 3 - CONSULTANT WORKLOAD
# # ==================================================

# with tab3:

#     st.subheader("Technical Consultant Workload")

#     active_df = filtered_df[
#         filtered_df[STATE_COL].isin(
#             [
#                 "In Progress",
#                 "To Be Initiated",
#                 "On Hold"
#             ]
#         )
#     ]

#     workload_df = (
#         active_df
#         .groupby(TC_COL)
#         .agg(
#             Active_Projects=("Id", "count"),
#             Avg_Delay=(DELAY_COL, "mean")
#         )
#         .reset_index()
#         .sort_values(
#             "Active_Projects",
#             ascending=False
#         )
#     )

#     fig = px.bar(
#         workload_df,
#         x=TC_COL,
#         y="Active_Projects",
#         title="Active Projects by Consultant",
#         text="Active_Projects"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.dataframe(
#         workload_df,
#         use_container_width=True
#     )



# with tab4:

#     st.subheader("🤖 Ask Questions About Projects")

#     question = st.text_input(
#         "Ask a question",
#         placeholder="Who has the highest average delay?"
#     )

#     if st.button("Ask AI") and question:

#         try:

#             with st.spinner("Analyzing projects..."):

#                 # Create summarized data instead of sending raw rows

#                 workload = (
#                     filtered_df
#                     .groupby("Technical consultant")
#                     .agg(
#                         Active_Projects=("Id", "count"),
#                         Avg_Delay=("Delay(In days)", "mean")
#                     )
#                     .reset_index()
#                     .sort_values(
#                         "Active_Projects",
#                         ascending=False
#                     )
#                 )

#                 state_summary = (
#                     filtered_df["State"]
#                     .value_counts()
#                     .to_string()
#                 )

#                 prompt = f"""
# You are a Project Portfolio Assistant.

# Project State Summary:

# {state_summary}

# Consultant Summary:

# {workload.head(20).to_string(index=False)}

# User Question:

# {question}

# Answer using ONLY the data above.
# Keep the answer concise.
# """

#                 response = ollama.chat(
#                     model="llama3",
#                     messages=[
#                         {
#                             "role": "user",
#                             "content": prompt
#                         }
#                     ]
#                 )

#                 # Works with newer and older ollama versions
#                 try:
#                     answer = response["message"]["content"]
#                 except:
#                     answer = response.message.content

#                 st.markdown("### 🤖 Answer")
#                 st.write(answer)

#         except Exception as e:

#             st.error(f"Ollama Error: {e}")

# # ==================================================
# # TOP DELAYED PROJECTS
# # ==================================================

# st.divider()

# st.subheader("🔴 Top Delayed Projects")

# delayed_df = (
#     filtered_df
#     .sort_values(
#         DELAY_COL,
#         ascending=False
#     )
#     .head(20)
# )

# st.dataframe(
#     delayed_df[
#         [
#             "Name",
#             "Technical consultant",
#             "Priority",
#             "State",
#             "Delay(In days)"
#         ]
#     ],
#     use_container_width=True
# )

# # ==================================================
# # EXPORT
# # ==================================================

# st.divider()

# csv = filtered_df.to_csv(index=False)

# st.download_button(
#     "📥 Export Filtered Data",
#     csv,
#     "filtered_projects.csv",
#     "text/csv"
# )

































import streamlit as st
import pandas as pd
import plotly.express as px
import ollama
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Project Portfolio Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    # Updated to the exact file provided
    df = pd.read_csv("ProjectAllOpenProjectsDashboard.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ==================================================
# COLUMN NAMES FROM UPDATED CSV
# ==================================================

PROJECT_COL = "Name"
PROJECT_TYPE_COL = "Project Type"
HOSTING_COL = "Hosting Type"
TC_COL = "Technical consultant"
SC_COL = "Solution Consultant"
OWNER_COL = "Project Owner"
START_DATE_COL = "Scheduled start date"
END_DATE_COL = "Scheduled end date"
PRIORITY_COL = "Priority"
COMPLETED_COL = "Is Technical Deployment Completed"
EFFORT_COL = "Actual Effort (In Hrs)"
STATE_COL = "State"

# ==================================================
# DATA CLEANING
# ==================================================

# Convert Dates
df[START_DATE_COL] = pd.to_datetime(df[START_DATE_COL], errors='coerce')
df[END_DATE_COL] = pd.to_datetime(df[END_DATE_COL], errors='coerce')

# Convert Effort Numeric
df[EFFORT_COL] = pd.to_numeric(df[EFFORT_COL], errors="coerce").fillna(0)

# Fill Missing Text values for filter predictability
df[TC_COL] = df[TC_COL].fillna("Unassigned").astype(str)
df[HOSTING_COL] = df[HOSTING_COL].fillna("Unknown").astype(str)
df[PRIORITY_COL] = df[PRIORITY_COL].fillna("Medium").astype(str)

# Calculate dynamic days remaining (or overdue) based on current year/time context
today = pd.to_datetime(datetime.now().date())
df['Days_Remaining'] = (df[END_DATE_COL] - today).dt.days

# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.title("Filters")

filtered_df = df.copy()

selected_tc = st.sidebar.multiselect(
    "Technical Consultant",
    sorted(df[TC_COL].unique())
)

selected_hosting = st.sidebar.multiselect(
    "Hosting Type",
    sorted(df[HOSTING_COL].unique())
)

selected_priority = st.sidebar.multiselect(
    "Priority",
    sorted(df[PRIORITY_COL].unique())
)

if selected_tc:
    filtered_df = filtered_df[filtered_df[TC_COL].isin(selected_tc)]

if selected_hosting:
    filtered_df = filtered_df[filtered_df[HOSTING_COL].isin(selected_hosting)]

if selected_priority:
    filtered_df = filtered_df[filtered_df[PRIORITY_COL].isin(selected_priority)]

# ==================================================
# KPI SECTION
# ==================================================

total_projects = len(filtered_df)

active_projects = len(
    filtered_df[filtered_df[STATE_COL].str.strip().isin(["In Progress", "To Be Initiated"])]
)

on_hold_projects = len(
    filtered_df[filtered_df[STATE_COL].str.strip() == "On Hold"]
)

completed_projects = len(
    filtered_df[filtered_df[STATE_COL].str.strip() == "Complete"]
)

total_consultants = filtered_df[TC_COL].nunique()
total_effort = round(filtered_df[EFFORT_COL].sum(), 1)

# ==================================================
# HEADER
# ==================================================

st.title("📊 Project Portfolio Dashboard")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Total Projects", total_projects)
c2.metric("Active Status", active_projects)
c3.metric("On Hold", on_hold_projects)
c4.metric("Completed Status", completed_projects)
c5.metric("Consultants Assigned", total_consultants)
c6.metric("Total Effort (Hrs)", total_effort)

st.divider()

# ==================================================
# CHARTS
# ==================================================

left, right = st.columns(2)

with left:
    state_count = (
        filtered_df[STATE_COL]
        .value_counts()
        .reset_index()
    )
    state_count.columns = ["State", "Count"]

    fig = px.pie(
        state_count,
        names="State",
        values="Count",
        title="Projects by State Status",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    hosting_count = (
        filtered_df[HOSTING_COL]
        .value_counts()
        .reset_index()
    )
    hosting_count.columns = ["Hosting Type", "Count"]

    fig = px.bar(
        hosting_count,
        x="Hosting Type",
        y="Count",
        title="Projects by Hosting Architecture",
        color="Hosting Type"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🚀 Ongoing Projects",
        "⏸️ On Hold Projects",
        "👨‍💻 TC Workload & Effort",
        "🤖 Ask AI"
    ]
)

# ==================================================
# TAB 1 - ONGOING PROJECTS
# ==================================================

with tab1:
    st.subheader("Ongoing Projects Tracking")

    ongoing_df = filtered_df[
        filtered_df[STATE_COL].str.strip().isin(["In Progress", "To Be Initiated"])
    ]

    st.metric("Total Ongoing Projects", len(ongoing_df))
    st.dataframe(ongoing_df, use_container_width=True, height=400)

# ==================================================
# TAB 2 - ON HOLD
# ==================================================

with tab2:
    st.subheader("On Hold Allocations")

    hold_df = filtered_df[filtered_df[STATE_COL].str.strip() == "On Hold"]

    st.metric("Projects On Hold", len(hold_df))
    st.dataframe(hold_df, use_container_width=True, height=400)

# ==================================================
# TAB 3 - CONSULTANT WORKLOAD
# ==================================================

with tab3:
    st.subheader("Technical Consultant Workload Distribution")

    workload_df = (
        filtered_df.groupby(TC_COL)
        .agg(
            Assigned_Projects=("Id", "count"),
            Total_Effort_Hrs=(EFFORT_COL, "sum")
        )
        .reset_index()
        .sort_values("Assigned_Projects", ascending=False)
    )

    fig = px.bar(
        workload_df,
        x=TC_COL,
        y="Assigned_Projects",
        title="Volume of Project Allocations by Technical Consultant",
        text="Assigned_Projects",
        color="Total_Effort_Hrs"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(workload_df, use_container_width=True)

# ==================================================
# TAB 4 - ASK AI
# ==================================================

with tab4:
    st.subheader("🤖 Ask Questions About Projects")

    question = st.text_input(
        "Ask a question",
        placeholder="Who has logged the most hours of Actual Effort?"
    )

    if st.button("Ask AI") and question:
        try:
            with st.spinner("Analyzing parameters..."):
                # Structured payload optimization matching your specific column schema
                ai_workload = (
                    filtered_df.groupby(TC_COL)
                    .agg(
                        Projects=("Id", "count"),
                        Total_Effort=(EFFORT_COL, "sum")
                    )
                    .reset_index()
                    .sort_values("Projects", ascending=False)
                )

                ai_state = filtered_df[STATE_COL].value_counts().to_string()

                prompt = f"""
You are a Project Portfolio Assistant.

Project State Distribution:
{ai_state}

Consultant Workload Profile:
{ai_workload.head(15).to_string(index=False)}

User Question:
{question}

Answer using ONLY the project ecosystem metrics context block above. 
Keep the answer direct and metric-driven.
"""

                response = ollama.chat(
                    model="llama3",
                    messages=[{"role": "user", "content": prompt}]
                )

                try:
                    answer = response["message"]["content"]
                except (KeyError, AttributeError):
                    answer = response.message.content

                st.markdown("### 🤖 Answer")
                st.write(answer)

        except Exception as e:
            st.error(f"Ollama Connection Error: {e}")

# ==================================================
# CLOSING CRITICAL VISIBILITY: RISK METRICS
# ==================================================

st.divider()
st.subheader("🔴 Time Critical & High Effort Initiatives")

# Replaced missing delay mechanics with a sorted look at active high-hours deployments
at_risk_df = (
    filtered_df.sort_values(by=[EFFORT_COL], ascending=False)
    .head(15)
)

st.dataframe(
    at_risk_df[[PROJECT_COL, PROJECT_TYPE_COL, HOSTING_COL, TC_COL, STATE_COL, EFFORT_COL]],
    use_container_width=True
)

# ==================================================
# EXPORT
# ==================================================

st.divider()
csv = filtered_df.to_csv(index=False)
st.download_button(
    "📥 Export Cleaned Segment Data",
    csv,
    "filtered_projects.csv",
    "text/csv"
)
