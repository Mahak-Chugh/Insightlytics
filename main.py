import streamlit as st
import pandas as pd
import numpy as np
#import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Data Analysis App", layout="wide", page_icon="📊")

# Title of the app
st.title("📊 Data Analysis App")
st.markdown("""
Welcome to the **Data Analysis App**! Upload your dataset (CSV, Excel, or TXT) and explore its insights with interactive visualizations.
""")

# Sidebar for file upload
st.sidebar.header("📂 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt", "csv", "xlsx", "xls"])

# Function to load data
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.txt'):
        return pd.read_csv(file, delimiter='\t')
    elif file.name.endswith('.xlsx') or file.name.endswith('.xls'):
        return pd.read_excel(file)
    else:
        st.error("Unsupported file format")
        return None

# Load data if file is uploaded
if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    if df is not None:
        st.sidebar.success("File uploaded successfully!")
        
        # Display the dataframe in an expandable section
        with st.expander("🔍 View Raw Data"):
            st.write(df)
        
        # Basic EDA
        st.subheader("📊 Exploratory Data Analysis (EDA)")
        
        # Show basic statistics in tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Summary Statistics", "Missing Values", "Correlation Heatmap", "Categorical Insights"])
        
        with tab1:
            st.write("**Summary Statistics**")
            st.write(df.describe())
        
        with tab2:
            st.write("**Missing Values**")
            st.write(df.isnull().sum())
        
        with tab3:
            st.write("**Correlation Heatmap**")
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_columns) > 1:
                corr = df[numeric_columns].corr()
                fig = px.imshow(corr, text_auto=True, color_continuous_scale="Viridis")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough numeric columns for a correlation heatmap.")
        
        with tab4:
            st.write("**Categorical Insights**")
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
            if len(categorical_columns) > 0:
                selected_cat_col = st.selectbox("Select a categorical column", categorical_columns, key="cat_insights_selectbox")
                st.write(df[selected_cat_col].value_counts())
            else:
                st.warning("No categorical columns found.")
        
        # Data Visualization
        st.subheader("📈 Data Visualization")
        
        # Select columns for visualization
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        
        # Sidebar for visualization options
        st.sidebar.header("📊 Visualization Options")
        
        # Dynamically adjust plot types based on dataset
        available_plots = []
        if len(numeric_columns) > 0:
            available_plots.extend(["Histogram", "Box Plot", "Scatter Plot", "Pair Plot"])
        if len(categorical_columns) > 0:
            available_plots.append("Bar Plot")
        
        if len(available_plots) == 0:
            st.warning("No compatible plot types available. Ensure your dataset has numeric or categorical columns.")
        else:
            plot_type = st.sidebar.selectbox("Select Plot Type", available_plots, key="plot_type_selectbox")
            
            if plot_type == "Histogram":
                if len(numeric_columns) > 0:
                    selected_column = st.sidebar.selectbox("Select a numeric column", numeric_columns, key="histogram_selectbox")
                    bins = st.sidebar.slider("Number of bins", min_value=5, max_value=100, value=20, key="histogram_bins")
                    fig = px.histogram(df, x=selected_column, nbins=bins, title=f"Histogram of {selected_column}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No numeric columns available for a histogram.")
            
            elif plot_type == "Box Plot":
                if len(numeric_columns) > 0:
                    selected_column = st.sidebar.selectbox("Select a numeric column", numeric_columns, key="boxplot_selectbox")
                    fig = px.box(df, y=selected_column, title=f"Box Plot of {selected_column}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No numeric columns available for a box plot.")
            
            elif plot_type == "Scatter Plot":
                if len(numeric_columns) > 1:
                    x_axis = st.sidebar.selectbox("Select X-axis", numeric_columns, key="scatter_x_selectbox")
                    y_axis = st.sidebar.selectbox("Select Y-axis", numeric_columns, key="scatter_y_selectbox")
                    color_column = st.sidebar.selectbox("Optional: Color by", [None] + categorical_columns, key="scatter_color_selectbox")
                    fig = px.scatter(df, x=x_axis, y=y_axis, color=color_column, title=f"{x_axis} vs {y_axis}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Not enough numeric columns for a scatter plot.")
            
            elif plot_type == "Bar Plot":
                if len(categorical_columns) > 0:
                    selected_column = st.sidebar.selectbox("Select a categorical column", categorical_columns, key="barplot_selectbox")
                    fig = px.bar(df[selected_column].value_counts(), title=f"Bar Plot of {selected_column}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No categorical columns available for a bar plot.")
            
            elif plot_type == "Pair Plot":
                if len(numeric_columns) > 1:
                    selected_columns = st.sidebar.multiselect("Select numeric columns", numeric_columns, default=numeric_columns[:3], key="pairplot_selectbox")
                    if len(selected_columns) > 1:
                        fig = px.scatter_matrix(df[selected_columns], title="Pair Plot")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Please select at least two numeric columns.")
                else:
                    st.warning("Not enough numeric columns for a pair plot.")
        
        # Dynamic Slider for filtering data
        st.sidebar.header("🔧 Dynamic Data Filter")
        if len(numeric_columns) > 0:
            selected_column_filter = st.sidebar.selectbox("Select a column to filter", numeric_columns, key="filter_selectbox")
            min_val = float(df[selected_column_filter].min())
            max_val = float(df[selected_column_filter].max())
            selected_range = st.sidebar.slider("Select range", min_val, max_val, (min_val, max_val), key="filter_slider")
            filtered_df = df[(df[selected_column_filter] >= selected_range[0]) & (df[selected_column_filter] <= selected_range[1])]
            st.subheader("Filtered Data")
            st.write(filtered_df)
        
        # Download filtered data
        st.sidebar.header("📥 Download Filtered Data")
        if st.sidebar.button("Download Filtered Data as CSV", key="download_button"):
            filtered_df.to_csv("filtered_data.csv", index=False)
            st.sidebar.success("Filtered data downloaded successfully!")
        
else:
    st.sidebar.info("Please upload a file to get started.")
