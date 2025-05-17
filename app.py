import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- Page config ---
st.set_page_config(
    page_title="NYC 311 Complaint Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)
rel_path = 'data/nyc_311_complaints_cleaned.csv' # /src/scripts/NYC_311_API_Project/
st.text(f"Looked for file at: {os.path.abspath(rel_path)}")
# --- Load data ---
@st.cache_data
def load_data(path=f"{rel_path}"):
    if not os.path.exists(path):
        st.error("CSV file not found. Please make sure the snapshot exists.")
        return pd.DataFrame()
    return pd.read_csv(path, parse_dates=["created_date", "closed_date"], low_memory=False)

df = load_data()
st.title("📈 NYC 311 Complaint Explorer")
st.write(
    """
    This interactive dashboard allows you to explore NYC 311 service complaints by agency and time of day.
    Use the sidebar to view dataset details and filter by agency. The visualizations highlight complaint volume trends and service patterns.
    You can also download both the filtered dataset and hourly summary for further analysis.
    """
)

if df.empty:
    st.stop()

# --- Ensure hour column exists ---
if "hour" not in df.columns:
    df["hour"] = pd.to_datetime(df["created_date"], errors="coerce").dt.hour

# --- Filter agency names that appear >1 time in any hour ---
temp = df.groupby(["hour", "agency_name"]).size().reset_index(name="count")
valid_agencies = temp[temp["count"] > 1]["agency_name"].dropna().unique()
df = df[df["agency_name"].isin(valid_agencies)]

# --- Sidebar agency filter ---
agency_options = sorted(valid_agencies)
selected_agency = st.selectbox(
    "Filter by Agency (appears >1x in any hour)",
    ["All"] + agency_options
)
if selected_agency != "All":
    df = df[df["agency_name"] == selected_agency]

# --- Sidebar metadata ---
st.sidebar.markdown("### 🧬 Data Overview")
st.sidebar.markdown(f"**Shape:** `{df.shape[0]:,}` rows × `{df.shape[1]}` columns")
st.sidebar.markdown("**Columns:**")
st.sidebar.write(df.columns.tolist())

# --- Tabs ---
tab1, tab2, tab3 = st.tabs([
    "📊 Complaints by Agency", 
    "📈 Volume by Hour", 
    "📄 Filtered Data"
])

# === TAB 1: Bar Chart by Agency Name ===
with tab1:
    st.markdown("### 📊 Total Complaint Count by Agency")

    if "agency_name" in df.columns:
        agency_counts = (
            df.groupby("agency_name")
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
        )

        fig_bar = px.bar(
            agency_counts,
            x="agency_name",
            y="count",
            title="Total Complaints by Agency",
            labels={
                "agency_name": "Agency",
                "count": "Number of Complaints"
            }
        )
        fig_bar.update_layout(
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Column 'agency_name' not found in dataset.")

# === TAB 2: Line Graph by Hour ===
with tab2:
    st.markdown("### 📈 Total Complaints by Hour")

    hourly_volume = (
        df.groupby("hour")
        .size()
        .reset_index(name="total_complaints")
    )

    fig = px.line(
        hourly_volume,
        x="hour",
        y="total_complaints",
        title="Total NYC 311 Complaints by Hour of Day",
        labels={
            "hour": "Hour of Day",
            "total_complaints": "Total Number of Complaints"
        },
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Only includes agencies that occurred more than once in any single hour.")

# === TAB 3: Filtered Data + Downloads ===
with tab3:
    st.markdown("### 📄 Filtered Dataset")
    st.dataframe(df.head(100), use_container_width=True)

    st.markdown("### 📥 Download Data")

    csv_full = df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Dataset (CSV)",
        data=csv_full,
        file_name="nyc_311_filtered.csv",
        mime="text/csv"
    )

    csv_hourly = hourly_volume.to_csv(index=False)
    st.download_button(
        label="Download Hourly Complaint Volume Summary (CSV)",
        data=csv_hourly,
        file_name="complaint_volume_by_hour.csv",
        mime="text/csv"
    )
