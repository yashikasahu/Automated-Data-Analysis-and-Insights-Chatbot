import os
import streamlit as st
from groq import Groq
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Data Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(30deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(30deg); }
    }
    
    .chat-container {
        background: linear-gradient(135deg, #667eea11, #764ba211);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .user-message {
        background: linear-gradient(135deg, #ff6b6b, #ff8e53);
        color: white;
        border: none;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 20px 20px 5px 20px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        transform: translateX(0);
        transition: all 0.3s ease;
    }
    
    .user-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        border: none;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 20px 20px 20px 5px;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        transform: translateX(0);
        transition: all 0.3s ease;
    }
    
    .bot-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
    }
    
    .info-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85));
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Add some sparkle animations */
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0); }
        50% { opacity: 1; transform: scale(1); }
    }
    
    .sparkle {
        position: absolute;
        background: radial-gradient(circle, #fff, transparent);
        border-radius: 50%;
        pointer-events: none;
        animation: sparkle 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Load Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "df" not in st.session_state:
    st.session_state.df = None

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Data Assistant</h1>
    <p>Powered by Groq | Your intelligent companion for data analysis and insights</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🛠️ Configuration")
    
    # API Key status
    if GROQ_API_KEY:
        st.success("✅ Groq API Key loaded")
    else:
        st.error("❌ No Groq API Key found")
        st.info("Please set GROQ_API_KEY in your environment variables")
    
    st.markdown("---")
    
    # Model selection
    st.markdown("### 🧠 Model Settings")
    model_options = {
        "llama-3.3-70b-versatile": "Llama 3.3 70B (Recommended)",
        "llama-3.1-70b-versatile": "Llama 3.1 70B",
        "mixtral-8x7b-32768": "Mixtral 8x7B"
    }
    
    selected_model = st.selectbox(
        "Choose Model:",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=0
    )
    
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 100, 1000, 600, 50)
    
    st.markdown("---")
    
    # Data upload section
    st.markdown("### 📊 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload CSV file for analysis",
        type=['csv'],
        help="Upload a CSV file to enable data-specific queries"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.success(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
            
            # Show basic info
            st.markdown("**Dataset Info:**")
            st.write(f"• Shape: {df.shape}")
            st.write(f"• Columns: {', '.join(df.columns[:3])}{'...' if len(df.columns) > 3 else ''}")
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    st.markdown("---")
    
    # Chat controls
    st.markdown("### 💬 Chat Controls")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Initialize Groq client
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

    def ask_groq(user_question, df=None):
        context = ""
        if df is not None:
            try:
                # Get dataset summary
                context = f"""
                Dataset Summary:
                - Shape: {df.shape}
                - Columns: {list(df.columns)}
                - Data types: {df.dtypes.to_dict()}
                
                Sample data (first 5 rows):
                {df.head(5).to_string()}
                
                Statistical summary:
                {df.describe().to_string()}
                """
            except Exception:
                context = "Could not parse dataframe."

        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": "You are a direct AI assistant. Give short, clear, straight-to-the-point answers. No lengthy explanations unless specifically asked. Be concise and factual."},
                {"role": "user", "content": f"Dataset Context:\n{context}\n\nUser Question: {user_question}"}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        st.markdown("### 💬 Chat with AI")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 📝 Conversation History")
            for i, (question, answer, timestamp) in enumerate(st.session_state.chat_history):
                with st.expander(f"💭 Query {i+1} - {timestamp}", expanded=(i == len(st.session_state.chat_history)-1)):
                    st.markdown(f'<div class="user-message"><strong>You:</strong> {question}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="bot-message"><strong>AI:</strong> {answer}</div>', unsafe_allow_html=True)
        
        # Input section
        st.markdown("### ✨ Ask a Question")
        
        # Example questions
        if st.session_state.df is not None:
            st.markdown("**💡 Try these example questions:**")
            examples = [
                "What are the key insights from this dataset?",
                "Show me summary statistics",
                "What patterns do you see in the data?",
                "Are there any missing values or data quality issues?",
                "What correlations exist between variables?"
            ]
            example_buttons = st.columns(len(examples))
            for i, example in enumerate(examples):
                with example_buttons[i % len(example_buttons)]:
                    if st.button(f"📊 {example[:20]}...", key=f"example_{i}"):
                        st.session_state.current_question = example
        
        # Question input
        user_input = st.text_area(
            "💬 Your question:",
            value=st.session_state.get("current_question", ""),
            placeholder="e.g., Give me insights about this data, or ask any general question...",
            height=100,
            key="question_input"
        )
        
        # Submit button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            submit_button = st.button("🚀 Ask AI", type="primary")
        with col_btn2:
            if st.button("🎲 Random Question"):
                random_questions = [
                    "What's interesting about artificial intelligence?",
                    "Explain quantum computing simply",
                    "What are the latest trends in data science?",
                    "How does machine learning work?",
                    "What is the future of technology?"
                ]
                import random
                st.session_state.current_question = random.choice(random_questions)
                st.rerun()
        
        # Process question
        if submit_button and user_input.strip():
            with st.spinner("🤔 AI is thinking..."):
                try:
                    df = st.session_state.get("df", None)
                    reply = ask_groq(user_input, df=df)
                    
                    # Add to chat history
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.chat_history.append((user_input, reply, timestamp))
                    
                    # Clear the input
                    st.session_state.current_question = ""
                    
                    # Rerun to show updated history
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        elif submit_button:
            st.warning("⚠️ Please enter a question first.")
    
    with col2:
        # Info cards
        st.markdown("### 📊 Quick Stats")
        
        if st.session_state.df is not None:
            df = st.session_state.df
            
            # Dataset metrics
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric("📝 Rows", f"{len(df):,}")
            with col_metric2:
                st.metric("📋 Columns", len(df.columns))
            
            # Data preview
            st.markdown("### 👀 Data Preview")
            st.dataframe(df.head(3), use_container_width=True)
            
            # Column info
            st.markdown("### 📊 Column Types")
            col_types = df.dtypes.value_counts()
            for dtype, count in col_types.items():
                st.write(f"• **{dtype}**: {count} columns")
        
        else:
            st.info("📤 Upload a CSV file to see dataset statistics")
        
        # Chat statistics
        st.markdown("### 💬 Chat Statistics")
        st.metric("Total Questions", len(st.session_state.chat_history))
        
        # Tips
        st.markdown("""
        ### 💡 Tips
        - Upload a CSV for data-specific insights
        - Ask follow-up questions for deeper analysis  
        - Use specific questions for better answers
        - Try the example questions above
        """)

else:
    st.error("⚠️ No GROQ_API_KEY found. Please set it in your environment.")
    st.info("""
    To set up your API key:
    1. Get your API key from [Groq Console](https://console.groq.com)
    2. Set environment variable: `export GROQ_API_KEY=your_api_key`
    3. Restart the application

    """)

