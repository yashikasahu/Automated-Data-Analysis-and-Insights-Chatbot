import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0rem 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2C3E50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
    }
    
    /* Chart containers */
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Warning/Info boxes */
    .stAlert {
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

class BeautifulDashboard:
    def __init__(self, df):
        self.df = df
        self.num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Set matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def create_hero_section(self):
        """Create beautiful hero section"""
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); 
                    border-radius: 20px; margin: 1rem 0; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);'>
            <h1 style='color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                📊 Analytics Dashboard
            </h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.2rem; margin: 0.5rem 0;'>
                Automated insights powered by your data
            </p>
            <p style='color: rgba(255,255,255,0.7); font-size: 1rem;'>
                ⚡ Real-time • 🎯 Smart Analysis • 📈 Beautiful Charts
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def show_beautiful_kpis(self):
        """Enhanced KPI cards with icons and colors"""
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            records = len(self.df)
            st.metric(
                label="📊 Total Records",
                value=f"{records:,}",
                delta=f"+{records} rows"
            )
        
        with col2:
            st.metric(
                label="📈 Numeric Fields",
                value=len(self.num_cols),
                delta=f"{round(len(self.num_cols)/len(self.df.columns)*100)}% of data"
            )
        
        with col3:
            st.metric(
                label="🏷️ Text Fields", 
                value=len(self.cat_cols),
                delta=f"{round(len(self.cat_cols)/len(self.df.columns)*100)}% of data"
            )
        
        with col4:
            missing = self.df.isnull().sum().sum()
            missing_pct = round((missing / (len(self.df) * len(self.df.columns))) * 100, 1)
            st.metric(
                label="❌ Missing Values",
                value=f"{missing:,}",
                delta=f"{missing_pct}% missing"
            )
        
        with col5:
            memory_mb = round(self.df.memory_usage(deep=True).sum() / 1024**2, 1)
            st.metric(
                label="💾 Memory Usage",
                value=f"{memory_mb} MB",
                delta="Optimized"
            )
    
    def create_stunning_charts(self):
        """Create beautiful, professional charts"""
        
        # Beautiful color palette
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']
        
        if len(self.num_cols) > 0:
            st.markdown("### 🎨 Data Distributions")
            
            # Create beautiful distribution plots
            num_charts = min(4, len(self.num_cols))
            
            if num_charts == 1:
                col = self.num_cols[0]
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
                
                # Histogram with KDE
                self.df[col].hist(bins=30, alpha=0.7, color=colors[0], ax=ax1, edgecolor='white')
                ax1.set_title(f'📊 Distribution: {col}', fontsize=14, fontweight='bold', pad=20)
                ax1.grid(True, alpha=0.3)
                
                # Box plot
                sns.boxplot(x=self.df[col], ax=ax2, color=colors[1])
                ax2.set_title(f'📦 Box Plot: {col}', fontsize=14, fontweight='bold', pad=20)
                ax2.grid(True, alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig)
            
            elif num_charts >= 2:
                fig, axes = plt.subplots(2, 2, figsize=(16, 12))
                axes = axes.flatten()
                
                for i, col in enumerate(self.num_cols[:4]):
                    color = colors[i % len(colors)]
                    
                    # Create histogram with gradient effect
                    n, bins, patches = axes[i].hist(self.df[col], bins=25, alpha=0.8, 
                                                   color=color, edgecolor='white', linewidth=1.2)
                    
                    # Add gradient to bars
                    for j, patch in enumerate(patches):
                        patch.set_facecolor(plt.cm.viridis(j / len(patches)))
                    
                    axes[i].set_title(f'✨ {col}', fontsize=12, fontweight='bold', pad=15)
                    axes[i].grid(True, alpha=0.3)
                    axes[i].set_facecolor('#f8f9fa')
                
                # Hide unused subplots
                for i in range(num_charts, 4):
                    axes[i].set_visible(False)
                
                plt.tight_layout()
                st.pyplot(fig)
        
        # Beautiful categorical charts
        if len(self.cat_cols) > 0:
            st.markdown("### 🌈 Category Analysis")
            
            for i, col in enumerate(self.cat_cols[:2]):
                top_values = self.df[col].value_counts().head(8)
                
                fig, ax = plt.subplots(figsize=(12, 7))
                
                # Create gradient bars
                bars = ax.bar(range(len(top_values)), top_values.values, 
                             color=[colors[j % len(colors)] for j in range(len(top_values))],
                             alpha=0.8, edgecolor='white', linewidth=2)
                
                # Add glowing effect
                for bar in bars:
                    bar.set_edgecolor('white')
                    bar.set_linewidth(2)
                
                ax.set_xticks(range(len(top_values)))
                ax.set_xticklabels(top_values.index, rotation=45, ha='right', fontsize=11)
                ax.set_title(f'🎯 Top Values: {col}', fontsize=16, fontweight='bold', pad=20)
                ax.set_ylabel('Count', fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='y')
                ax.set_facecolor('#f8f9fa')
                
                # Add value labels on bars
                for bar, value in zip(bars, top_values.values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(top_values.values),
                           f'{value:,}', ha='center', va='bottom', fontweight='bold', fontsize=10)
                
                plt.tight_layout()
                st.pyplot(fig)
        
        # Stunning correlation heatmap
        if len(self.num_cols) > 1:
            st.markdown("### 🔥 Correlation Heatmap")
            
            corr = self.df[self.num_cols].corr()
            
            fig, ax = plt.subplots(figsize=(12, 10))
            
            # Create mask for upper triangle
            mask = np.triu(np.ones_like(corr, dtype=bool))
            
            # Custom colormap
            cmap = sns.diverging_palette(250, 10, as_cmap=True)
            
            # Create heatmap with beautiful styling
            sns.heatmap(corr, mask=mask, cmap=cmap, center=0, square=True,
                       annot=True, fmt='.2f', cbar_kws={"shrink": .8},
                       linewidths=2, linecolor='white', ax=ax)
            
            ax.set_title('🔗 Feature Correlation Matrix', fontsize=18, fontweight='bold', pad=30)
            plt.tight_layout()
            st.pyplot(fig)
    
    def show_data_insights(self):
        """Beautiful insights section"""
        st.markdown("### 💡 Smart Insights")
        
        # Create insight cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0;
                        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);'>
                <h3 style='margin: 0; color: white;'>🎯 Data Quality</h3>
            """, unsafe_allow_html=True)
            
            # Data quality metrics
            total_cells = len(self.df) * len(self.df.columns)
            missing_cells = self.df.isnull().sum().sum()
            quality_score = round((1 - missing_cells/total_cells) * 100, 1)
            
            st.markdown(f"""
                <p style='margin: 0.5rem 0; color: white; font-size: 1.1rem;'>
                    Quality Score: <strong>{quality_score}%</strong><br>
                    Complete Records: <strong>{len(self.df.dropna()):,}</strong><br>
                    Missing Cells: <strong>{missing_cells:,}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #4ECDC4 0%, #66D9EF 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0;
                        box-shadow: 0 8px 32px rgba(78, 205, 196, 0.3);'>
                <h3 style='margin: 0; color: white;'>📈 Statistics</h3>
            """, unsafe_allow_html=True)
            
            if self.num_cols:
                avg_mean = round(self.df[self.num_cols].mean().mean(), 2)
                total_variance = round(self.df[self.num_cols].var().sum(), 2)
                
                st.markdown(f"""
                    <p style='margin: 0.5rem 0; color: white; font-size: 1.1rem;'>
                        Average Mean: <strong>{avg_mean}</strong><br>
                        Total Variance: <strong>{total_variance}</strong><br>
                        Numeric Features: <strong>{len(self.num_cols)}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    def show_top_correlations(self):
        """Show top correlations in a beautiful format"""
        if len(self.num_cols) > 1:
            st.markdown("### 🔗 Strongest Relationships")
            
            corr = self.df[self.num_cols].corr()
            correlations = []
            
            for i in range(len(corr.columns)):
                for j in range(i+1, len(corr.columns)):
                    correlations.append({
                        'Feature 1': corr.columns[i],
                        'Feature 2': corr.columns[j],
                        'Correlation': round(corr.iloc[i, j], 3),
                        'Strength': '🔥 Very Strong' if abs(corr.iloc[i, j]) > 0.8 else 
                                   '💪 Strong' if abs(corr.iloc[i, j]) > 0.6 else 
                                   '👍 Moderate' if abs(corr.iloc[i, j]) > 0.3 else '👌 Weak'
                    })
            
            corr_df = pd.DataFrame(correlations).sort_values('Correlation', key=abs, ascending=False)
            
            # Style the dataframe
            styled_df = corr_df.head(10).style.background_gradient(
                subset=['Correlation'], cmap='RdBu_r'
            ).format({'Correlation': '{:.3f}'})
            
            st.dataframe(styled_df, use_container_width=True)

def create_progress_animation():
    """Create loading animation"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(1, 101):
        progress_bar.progress(i)
        status_text.text(f'🚀 Loading dashboard... {i}%')
        
        if i == 100:
            status_text.text('✅ Dashboard ready!')
            break
    
    # Clear after loading
    import time
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()

def main():
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0; margin-bottom: 2rem;'>
        <h1 style='font-size: 4rem; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>
            📊 ANALYTICS HUB
        </h1>
        <p style='font-size: 1.3rem; color: #2C3E50; margin: 1rem 0; font-weight: 500;'>
            🚀 Automated • 🎯 Intelligent • ✨ Beautiful
        </p>
        <p style='color: #7F8C8D; font-size: 1rem;'>
            Built with ❤️ using Streamlit • Real-time insights at your fingertips
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for data
    if "df" not in st.session_state:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #FFA726 0%, #FFB74D 100%); 
                    border-radius: 20px; color: white; margin: 2rem 0;'>
            <h2 style='color: white; margin: 0;'>⚠️ No Data Found</h2>
            <p style='color: white; font-size: 1.1rem; margin: 1rem 0;'>
                Please upload your data file from the Home page to see the magic! ✨
            </p>
            <p style='color: rgba(255,255,255,0.9);'>
                Supported formats: CSV, Excel, JSON
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    df = st.session_state["df"]
    
    # Sidebar with beautiful styling
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem; margin-bottom: 2rem;'>
        <h2 style='color: #ECF0F1; margin: 0;'>⚙️ Controls</h2>
        <p style='color: #BDC3C7; font-size: 0.9rem;'>Customize your dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced controls
    sample_size = st.sidebar.slider("🎯 Analysis Sample", 10, len(df), min(5000, len(df)))
    show_advanced = st.sidebar.checkbox("🔬 Advanced Analytics", value=True)
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Dashboard"):
        create_progress_animation()
        st.rerun()
    
    # Current time
    st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 1rem; margin-top: 2rem; 
                background: rgba(255,255,255,0.1); border-radius: 10px;'>
        <p style='color: #ECF0F1; margin: 0; font-size: 0.9rem;'>
            🕐 Last Updated<br>
            <strong>{datetime.now().strftime('%H:%M:%S')}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use sample for performance
    df_sample = df.head(sample_size)
    dashboard = BeautifulDashboard(df_sample)
    
    # Create beautiful dashboard
    dashboard.show_beautiful_kpis()
    
    st.markdown("---")
    
    # Charts section
    dashboard.create_stunning_charts()
    
    if show_advanced:
        st.markdown("---")
        dashboard.show_data_insights()
        st.markdown("---")
        dashboard.show_top_correlations()
        
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.1) 100%); 
                border-radius: 15px; margin: 2rem 0;'>
        <h3 style='color: #2C3E50; margin: 0;'>🚀 Dashboard Complete!</h3>
        <p style='color: #7F8C8D; margin: 0.5rem 0;'>
            Your data has been automatically analyzed with beautiful visualizations
        </p>
        <p style='color: #BDC3C7; font-size: 0.9rem; margin: 0;'>
            💡 Upload new data to see instant updates • Built with Streamlit ⚡
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()