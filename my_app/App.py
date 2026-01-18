import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import time
import os
#run requirements.txt to install all required libraries
#set up env for GROQ_API_KEY

API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))


# Page configuration
st.set_page_config(
    page_title="Data Upload Hub",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main theme adjustments */
    .stApp {
        background-color: #0e1117;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1f4e79 0%, #2d5aa0 50%, #3a6bc7 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(31, 78, 121, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .upload-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #3a6bc7;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
        color: #ffffff;
    }
    
    .upload-container:hover {
        border-color: #4a7bd7;
        box-shadow: 0 8px 25px rgba(58, 107, 199, 0.3);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #3a6bc7;
        color: #ffffff;
    }
    
    .feature-card h4 {
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .feature-card p {
        color: #b3b3b3;
        margin: 0;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #1f4e79 0%, #2d5aa0 50%, #3a6bc7 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(31, 78, 121, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .success-message {
        background: linear-gradient(135deg, #0f5132 0%, #198754 50%, #20c997 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
        box-shadow: 0 4px 20px rgba(15, 81, 50, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .file-info {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    /* Fix text colors for dark theme */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #ffffff !important;
    }
    
    .stMarkdown p {
        color: #e0e0e0 !important;
    }
    
    /* Style dataframes for dark theme */
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1f4e79 0%, #3a6bc7 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2d5aa0 0%, #4a7bd7 100%);
        box-shadow: 0 4px 15px rgba(58, 107, 199, 0.3);
        transform: translateY(-2px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px 8px 0 0;
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1f4e79 0%, #3a6bc7 100%) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>📊 Data Upload Hub</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">Transform your data into insights with our powerful analytics platform</p>
</div>
""", unsafe_allow_html=True)

# Create columns for layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Upload section
    st.markdown("""
    <div class="upload-container">
        <h2>🚀 Upload Your Data File</h2>
        <p style="margin: 1rem 0; color: #666;">Drag and drop your file here or click to browse</p>
        <p style="font-size: 0.9rem; color: #888;">Supported formats: CSV, Excel (XLS/XLSX), JSON</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=["csv", "xlsx", "xls"],
        help="Upload your data file to get started with analysis"
    )

# Features section
st.markdown("---")
st.markdown("### ✨ Platform Features")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    <div class="feature-card">
        <h4>📈 Smart Analytics</h4>
        <p>Automated data profiling and statistical analysis to understand your data better.</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class="feature-card">
        <h4>🎨 Beautiful Visualizations</h4>
        <p>Create stunning charts and graphs with our interactive visualization tools.</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
    <div class="feature-card">
        <h4>⚡ Fast Processing</h4>
        <p>Lightning-fast data processing and real-time preview of your datasets.</p>
    </div>
    """, unsafe_allow_html=True)

# File processing
if uploaded_file:
    with st.spinner('Processing your file...'):
        time.sleep(0.5)  # Small delay for better UX
        
        try:
            # Determine file type and read accordingly
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                file_type = "CSV"
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(uploaded_file)
                file_type = "Excel"
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)
                file_type = "JSON"
            else:
                st.error("❌ Unsupported file format")
                st.stop()

            # Store dataframe in session state
            st.session_state["df"] = df
            
            # Success message
            st.markdown(f"""
            <div class="success-message">
                ✅ File uploaded successfully! Your {file_type} file is ready for analysis.
            </div>
            """, unsafe_allow_html=True)
            
            # File information
            st.markdown("### 📋 File Information")
            
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.markdown(f"""
                <div class="file-info">
                    <strong>📁 File Name:</strong> {uploaded_file.name}<br>
                    <strong>📊 File Type:</strong> {file_type}<br>
                    <strong>💾 File Size:</strong> {uploaded_file.size:,} bytes
                </div>
                """, unsafe_allow_html=True)
            
            with info_col2:
                st.markdown(f"""
                <div class="stats-container">
                    <h4>📊 Dataset Statistics</h4>
                    <p><strong>Rows:</strong> {len(df):,}</p>
                    <p><strong>Columns:</strong> {len(df.columns):,}</p>
                    <p><strong>Memory Usage:</strong> {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Data preview
            st.markdown("### 👀 Data Preview")
            st.markdown("Here's a quick look at your data:")
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["📋 First 10 Rows", "📊 Data Types", "📈 Summary Statistics"])
            
            with tab1:
                st.dataframe(df.head(10), use_container_width=True)
            
            with tab2:
                dtype_df = pd.DataFrame({
                    'Column': df.columns,
                    'Data Type': df.dtypes.values,
                    'Non-Null Count': df.count().values,
                    'Null Count': df.isnull().sum().values
                })
                st.dataframe(dtype_df, use_container_width=True)
            
            with tab3:
                # Only show summary for numeric columns
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    st.dataframe(numeric_df.describe(), use_container_width=True)
                else:
                    st.info("No numeric columns found for summary statistics.")
            
            # Next steps
            st.markdown("---")
            st.markdown("### 🚀 Next Steps")
            
            next_col1, next_col2 = st.columns(2)
            
            with next_col1:
                if st.button("📊 Start EDA Analysis", type="primary", use_container_width=True):
                    st.success("Navigate to the EDA page from the sidebar to begin your analysis!")
            
            with next_col2:
                if st.button("📈 Create Visualizations", type="secondary", use_container_width=True):
                    st.success("Head to the Visualization page to create stunning charts!")
            
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.info("Please make sure your file is properly formatted and try again.")

else:
    # Show example when no file is uploaded
    st.markdown("---")
    st.markdown("### 💡 Getting Started")
    
    example_col1, example_col2 = st.columns(2)
    
    with example_col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📝 Prepare Your Data</h4>
            <ul style="text-align: left;">
                <li>Ensure your CSV has headers in the first row</li>
                <li>Check for consistent data types in columns</li>
                <li>Remove any unnecessary formatting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with example_col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 What You Can Do</h4>
            <ul style="text-align: left;">
                <li>Exploratory Data Analysis (EDA)</li>
                <li>Interactive visualizations</li>
                <li>Statistical insights</li>
                <li>Data quality assessment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>Built with ❤️ using Streamlit | Ready to transform your data into insights</p>
</div>

""", unsafe_allow_html=True)

