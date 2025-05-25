import streamlit as st
from agent_chain import run_chain
import pandas as pd
import sqlite3

st.set_page_config(page_title="Restaurant SQL Agent", layout="wide")
st.title("🍽️ Natural Language SQL Agent for Restaurant DB")

st.markdown("Ask a question like:")
st.code("Show all restaurants in Mumbai with rating > 4.5")

# Initialize session state for storing the final answer
if "final_answer" not in st.session_state:
    st.session_state.final_answer = None

question = st.text_input("Enter your question", placeholder="e.g., Count of restaurants in Pune with >4.2 rating")

if st.button("Run"):
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating SQL and executing..."):
            try:
                final_answer = run_chain(question)
                st.session_state.final_answer = final_answer
            except Exception as e:
                st.error(f"Error: {e}")

# Show answer even after interaction
if st.session_state.final_answer:
    st.subheader("🧠 Final Answer")
    st.success(st.session_state.final_answer)

# Dashboard with filters
# Dashboard with filters
st.markdown("---")
st.header("📋 Restaurant Dashboard")

try:
    conn = sqlite3.connect("restaurant.db")
    df_all = pd.read_sql("SELECT * FROM restaurants", conn)

    if not df_all.empty:
        # Show dynamic filters
        st.subheader("🔍 Filter Options")
        filter_cols = st.multiselect("Select columns to filter", df_all.columns.tolist())

        filtered_df = df_all.copy()

        for col in filter_cols:
            if pd.api.types.is_numeric_dtype(df_all[col]):
                min_val = float(df_all[col].min())
                max_val = float(df_all[col].max())
                selected_range = st.slider(f"{col} range", min_val, max_val, (min_val, max_val))
                filtered_df = filtered_df[(filtered_df[col] >= selected_range[0]) & (filtered_df[col] <= selected_range[1])]
            
            elif pd.api.types.is_object_dtype(df_all[col]):
                unique_vals = df_all[col].dropna().unique().tolist()
                selected_vals = st.multiselect(f"Select {col}", unique_vals, default=unique_vals)
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]

            elif pd.api.types.is_datetime64_any_dtype(df_all[col]):
                min_date = df_all[col].min()
                max_date = df_all[col].max()
                selected_date = st.date_input(f"Select {col} range", (min_date, max_date))
                if isinstance(selected_date, tuple) and len(selected_date) == 2:
                    filtered_df = filtered_df[(df_all[col] >= selected_date[0]) & (df_all[col] <= selected_date[1])]

        st.subheader("Filtered Restaurant Data")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("No data available in 'restaurants' table.")
except Exception as e:
    st.error(f"Database Error: {e}")
