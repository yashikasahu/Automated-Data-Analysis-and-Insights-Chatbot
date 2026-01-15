import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

class EDAProcessor:
    def __init__(self, df):
        self.df = df
        self.num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    def clean_data(self, strategy='auto'):
        """Clean data with flexible strategies"""
        df_clean = self.df.copy()
        
        # Numeric columns
        for col in self.num_cols:
            if df_clean[col].isnull().any():
                if strategy == 'median':
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                elif strategy == 'mean':
                    df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                else:  # auto
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
        
        # Categorical columns
        for col in self.cat_cols:
            if df_clean[col].isnull().any() and not df_clean[col].mode().empty:
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
        
        return df_clean
    
    def get_summary(self):
        """Get data summary"""
        return {
            'shape': self.df.shape,
            'missing': self.df.isnull().sum().sum(),
            'dtypes': self.df.dtypes.value_counts().to_dict(),
            'memory_mb': round(self.df.memory_usage(deep=True).sum() / 1024**2, 2)
        }
    
    def get_stats(self):
        """Get statistical information"""
        stats = {}
        if self.num_cols:
            stats['numeric'] = self.df[self.num_cols].describe()
        if self.cat_cols:
            stats['categorical'] = {col: self.df[col].value_counts().head() for col in self.cat_cols[:5]}
        return stats

def show_overview(processor):
    """Display data overview"""
    summary = processor.get_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{summary['shape'][0]:,}")
    col2.metric("Columns", summary['shape'][1])
    col3.metric("Missing", summary['missing'])
    col4.metric("Memory (MB)", summary['memory_mb'])

def show_analysis(processor):
    """Display analysis based on data types"""
    stats = processor.get_stats()
    
    # Numeric analysis
    if 'numeric' in stats:
        st.subheader("Numeric Variables")
        st.dataframe(stats['numeric'].round(3))
        
        # Simple correlation if multiple numeric columns
        if len(processor.num_cols) > 1:
            st.subheader("Correlations")
            corr = processor.df[processor.num_cols].corr()
            st.dataframe(corr.round(3))
    
    # Categorical analysis
    if 'categorical' in stats:
        st.subheader("Categorical Variables")
        for col, counts in stats['categorical'].items():
            with st.expander(f"{col} - Top Values"):
                st.dataframe(counts)

def download_data(df, filename="processed_data"):
    """Flexible download function"""
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button("📄 CSV", csv, f"{filename}.csv", "text/csv")
    
    with col2:
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        st.download_button("📊 Excel", buffer.getvalue(), f"{filename}.xlsx", 
                          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def main():
    try:
        st.title("🔧 Flexible EDA Tool")
        
        if "df" not in st.session_state:
            st.warning("⚠️ Upload data first")
            return
        
        # Initialize processor
        processor = EDAProcessor(st.session_state["df"])
        
        # Sidebar controls
        st.sidebar.header("Options")
        clean_strategy = st.sidebar.selectbox("Clean Strategy", ["auto", "median", "mean"])
        show_raw = st.sidebar.checkbox("Show Raw Data")
        
        # Main content
        if show_raw:
            st.subheader("Raw Data")
            st.dataframe(processor.df.head(50))
        
        st.subheader("Overview")
        show_overview(processor)
        
        st.subheader("Analysis")
        show_analysis(processor)
        
        # Cleaning
        if st.button("🧹 Clean Data"):
            cleaned_df = processor.clean_data(clean_strategy)
            st.session_state["df"] = cleaned_df
            st.success("Data cleaned!")
            st.rerun()
        
        # Download
        st.subheader("Download")
        download_data(st.session_state["df"])
        
    except Exception as e:
        if "ScriptRunContext" in str(e):
            print("⚠️ This is a Streamlit app. Run it with: streamlit run filename.py")
        else:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    # Check if running in Streamlit context
    try:
        import streamlit.runtime.scriptrunner.script_run_context as ctx
        if ctx.get_script_run_ctx() is None:
            print("⚠️ This is a Streamlit app!")
            print("Run it with: streamlit run your_filename.py")
            exit(1)
    except:
        pass
    
    main()