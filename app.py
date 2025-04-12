import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="YouTube Video Analysis", layout="wide")
st.title("📊 YouTube Video Data Analysis")

uploaded_file = st.file_uploader("Upload video_id_info.csv file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, on_bad_lines='skip')

    st.subheader("Initial Data Preview")
    st.write(df.head())

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    df.dropna(inplace=True)
    st.success("Dropped missing values")

    st.subheader("Statistical Summary")
    st.write(df.describe())

    # Conditional Visualizations
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    st.subheader("Correlation Heatmap")
    if len(numeric_cols) >= 2:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    st.subheader("Distribution Plot")
    dist_col = st.selectbox("Choose a column for distribution plot", numeric_cols)
    if dist_col:
        fig, ax = plt.subplots()
        sns.histplot(df[dist_col], kde=True, ax=ax)
        st.pyplot(fig)

    st.subheader("Box Plot")
    box_col = st.selectbox("Choose a column for box plot", numeric_cols, key='box')
    if box_col:
        fig, ax = plt.subplots()
        sns.boxplot(x=df[box_col], ax=ax)
        st.pyplot(fig)

else:
    st.info("👈 Upload a CSV file to begin analysis.")
