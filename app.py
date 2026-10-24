
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("Care Transition Efficiency & Placement Outcome Analytics")
st.write(
    "Explore reported counts across CBP custody, HHS care, "
    "transfers, and discharges."
)

st.info(
    "This dashboard shows aggregate reported counts. "
    "It does not measure individual case processing times."
)

# Load the dataset
st.sidebar.header("Dataset")
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

data_folder = Path(__file__).parent / "data"
csv_files = sorted(data_folder.glob("*.csv"))

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    elif csv_files:
        df = pd.read_csv(csv_files[0])
        st.sidebar.success(f"Loaded: {csv_files[0].name}")
    else:
        st.warning("Upload your CSV file using the sidebar.")
        st.stop()

    df.columns = df.columns.astype(str).str.strip()
    df = df.dropna(how="all").copy()

    # Identify the date column
    date_candidates = [
        col for col in df.columns
        if "date" in col.lower()
    ]
    date_col = date_candidates[0] if date_candidates else None

    if date_col:
        df[date_col] = pd.to_datetime(
            df[date_col], errors="coerce"
        )

    # Convert columns containing numbers into numeric data
    for col in df.columns:
        if col == date_col:
            continue

        if df[col].dtype == "object":
            cleaned = (
                df[col].astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
                .replace({"": None, "nan": None, "None": None})
            )
            converted = pd.to_numeric(cleaned, errors="coerce")

            if converted.notna().sum() > 0:
                df[col] = converted

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # Dataset overview
    st.header("1. Dataset Preview")
    a, b, c = st.columns(3)
    a.metric("Total Rows", f"{len(df):,}")
    b.metric("Total Columns", len(df.columns))
    c.metric("Numeric Columns", len(numeric_cols))

    st.dataframe(df.head(15), use_container_width=True)

    if not numeric_cols:
        st.error(
            "No numeric columns were detected. "
            "Please check your CSV data."
        )
        st.stop()

    # Choose graph columns
    st.sidebar.header("Graph Settings")
    default_cols = numeric_cols[:min(4, len(numeric_cols))]

    selected_cols = st.sidebar.multiselect(
        "Choose columns for graphs",
        options=numeric_cols,
        default=default_cols
    )

    if not selected_cols:
        st.warning("Select at least one column in Graph Settings.")
        st.stop()

    # Summary statistics
    st.header("2. Summary Statistics")
    st.dataframe(
        df[selected_cols].describe().round(2),
        use_container_width=True
    )

    # Individual graphs
    st.header("3. Individual Graphs")

    for col in selected_cols:
        if date_col and df[date_col].notna().any():
            plot_df = df[[date_col, col]].dropna().sort_values(date_col)

            fig = px.line(
                plot_df,
                x=date_col,
                y=col,
                markers=True,
                title=f"{col} Over Time"
            )
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title=col
            )
        else:
            plot_df = df[[col]].dropna().reset_index(drop=True)
            plot_df["Record"] = plot_df.index + 1

            fig = px.line(
                plot_df,
                x="Record",
                y=col,
                markers=True,
                title=f"{col} by Record"
            )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key=f"line_{numeric_cols.index(col)}"
        )

    # Comparison graph
    st.header("4. Compare Reported Counts")

    if date_col and df[date_col].notna().any():
        comparison_df = df[[date_col] + selected_cols].dropna(
            subset=[date_col]
        )

        comparison = comparison_df.melt(
            id_vars=[date_col],
            value_vars=selected_cols,
            var_name="Measure",
            value_name="Count"
        )

        fig = px.line(
            comparison,
            x=date_col,
            y="Count",
            color="Measure",
            title="Comparison of Selected Counts"
        )
    else:
        comparison_df = df[selected_cols].reset_index(drop=True)
        comparison_df["Record"] = comparison_df.index + 1

        comparison = comparison_df.melt(
            id_vars=["Record"],
            value_vars=selected_cols,
            var_name="Measure",
            value_name="Count"
        )

        fig = px.line(
            comparison,
            x="Record",
            y="Count",
            color="Measure",
            title="Comparison of Selected Counts"
        )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="comparison_chart"
    )

    # Missing data
    st.header("5. Missing Values")
    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": [
            int(df[col].isna().sum()) for col in df.columns
        ]
    })
    st.dataframe(missing_df, use_container_width=True)

    # Download data
    st.header("6. Download Data")
    st.download_button(
        "Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="care_transition_analysed_data.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error("The dashboard encountered an error.")
    st.exception(e)

