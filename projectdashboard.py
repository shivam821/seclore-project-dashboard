import streamlit as st
import pandas as pd
import plotly.express as px

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
    df = pd.read_csv("ProjectAllProjectsDashboard.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ==================================================
# COLUMN NAMES FROM YOUR CSV
# ==================================================

PROJECT_COL = "Name"
TC_COL = "Technical consultant"
STATE_COL = "State"
PRIORITY_COL = "Priority"
DELAY_COL = "Delay(In days)"
GEOGRAPHY_COL = "Geography"
EFFORT_COL = "Actual Effort"

# ==================================================
# DATA CLEANING
# ==================================================

if DELAY_COL in df.columns:
    df[DELAY_COL] = pd.to_numeric(
        df[DELAY_COL],
        errors="coerce"
    ).fillna(0)

# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.title("Filters")

filtered_df = df.copy()

selected_tc = st.sidebar.multiselect(
    "Technical Consultant",
    sorted(df[TC_COL].dropna().astype(str).unique())
)

selected_geo = st.sidebar.multiselect(
    "Geography",
    sorted(df[GEOGRAPHY_COL].dropna().astype(str).unique())
)

selected_priority = st.sidebar.multiselect(
    "Priority",
    sorted(df[PRIORITY_COL].dropna().astype(str).unique())
)

if selected_tc:
    filtered_df = filtered_df[
        filtered_df[TC_COL].astype(str).isin(selected_tc)
    ]

if selected_geo:
    filtered_df = filtered_df[
        filtered_df[GEOGRAPHY_COL].astype(str).isin(selected_geo)
    ]

if selected_priority:
    filtered_df = filtered_df[
        filtered_df[PRIORITY_COL].astype(str).isin(selected_priority)
    ]

# ==================================================
# KPI SECTION
# ==================================================

total_projects = len(filtered_df)

active_projects = len(
    filtered_df[
        filtered_df[STATE_COL].isin(
            [
                "In Progress",
                "To Be Initiated"
            ]
        )
    ]
)

on_hold_projects = len(
    filtered_df[
        filtered_df[STATE_COL] == "On Hold"
    ]
)

completed_projects = len(
    filtered_df[
        filtered_df[STATE_COL] == "Complete"
    ]
)

total_consultants = (
    filtered_df[TC_COL]
    .nunique()
)

avg_delay = round(
    filtered_df[DELAY_COL].mean(),
    1
)

# ==================================================
# HEADER
# ==================================================

st.title("📊 Project Portfolio Dashboard")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Projects", total_projects)
c2.metric("Active", active_projects)
c3.metric("On Hold", on_hold_projects)
c4.metric("Completed", completed_projects)
c5.metric("Consultants", total_consultants)
c6.metric("Avg Delay", avg_delay)

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
        title="Projects by State"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    geo_count = (
        filtered_df[GEOGRAPHY_COL]
        .value_counts()
        .head(10)
        .reset_index()
    )

    geo_count.columns = ["Geography", "Count"]

    fig = px.bar(
        geo_count,
        x="Geography",
        y="Count",
        title="Projects by Geography"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3 = st.tabs(
    [
        "🚀 Ongoing Projects",
        "⏸️ On Hold Projects",
        "👨‍💻 TC Workload"
    ]
)

# ==================================================
# TAB 1 - ONGOING PROJECTS
# ==================================================

with tab1:

    st.subheader("Ongoing Projects")

    ongoing_df = filtered_df[
        filtered_df[STATE_COL].isin(
            [
                "In Progress",
                "To Be Initiated"
            ]
        )
    ]

    st.metric(
        "Total Ongoing Projects",
        len(ongoing_df)
    )

    st.dataframe(
        ongoing_df,
        use_container_width=True,
        height=600
    )

# ==================================================
# TAB 2 - ON HOLD
# ==================================================

with tab2:

    st.subheader("On Hold Projects")

    hold_df = filtered_df[
        filtered_df[STATE_COL] == "On Hold"
    ]

    st.metric(
        "Projects On Hold",
        len(hold_df)
    )

    st.dataframe(
        hold_df,
        use_container_width=True,
        height=600
    )

# ==================================================
# TAB 3 - CONSULTANT WORKLOAD
# ==================================================

with tab3:

    st.subheader("Technical Consultant Workload")

    active_df = filtered_df[
        filtered_df[STATE_COL].isin(
            [
                "In Progress",
                "To Be Initiated",
                "On Hold"
            ]
        )
    ]

    workload_df = (
        active_df
        .groupby(TC_COL)
        .agg(
            Active_Projects=("Id", "count"),
            Avg_Delay=(DELAY_COL, "mean")
        )
        .reset_index()
        .sort_values(
            "Active_Projects",
            ascending=False
        )
    )

    fig = px.bar(
        workload_df,
        x=TC_COL,
        y="Active_Projects",
        title="Active Projects by Consultant",
        text="Active_Projects"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        workload_df,
        use_container_width=True
    )

# ==================================================
# TOP DELAYED PROJECTS
# ==================================================

st.divider()

st.subheader("🔴 Top Delayed Projects")

delayed_df = (
    filtered_df
    .sort_values(
        DELAY_COL,
        ascending=False
    )
    .head(20)
)

st.dataframe(
    delayed_df[
        [
            "Name",
            "Technical consultant",
            "Priority",
            "State",
            "Delay(In days)"
        ]
    ],
    use_container_width=True
)

# ==================================================
# EXPORT
# ==================================================

st.divider()

csv = filtered_df.to_csv(index=False)

st.download_button(
    "📥 Export Filtered Data",
    csv,
    "filtered_projects.csv",
    "text/csv"
)