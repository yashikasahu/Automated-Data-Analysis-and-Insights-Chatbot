
# 🤖 AI-Powered Data Chatbot

An advanced **AI chatbot for intelligent data analysis** built with **Streamlit**. This tool allows users to upload datasets and ask complex questions to AI models (OpenAI GPT, Google Gemini, Anthropic Claude, or custom APIs) to generate **insights, visualizations, and actionable recommendations**.

---

## **Features**

- Upload CSV, Excel, or JSON datasets
- Multi-API support:
  - OpenAI GPT
  - Google Gemini
  - Anthropic Claude
  - Custom LLM APIs
- Intelligent AI analysis:
  - Statistical summaries
  - Data quality assessments
  - Pattern detection
  - Business insights
  - Actionable recommendations
  - Visualization suggestions
- Pre-built question suggestions for quick analysis
- Chat history management
- Demo mode for testing without API keys
- Advanced options: Include visualization/code, set analysis depth

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/your-username/ai-data-chatbot.git
cd ai-data-chatbot
````

2. Create a virtual environment (recommended):

```bash
python -m venv venv
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## **Usage**

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Upload your dataset (CSV, Excel, or JSON)
3. Choose your AI provider and enter your API key (or use Demo Mode)
4. Ask questions and get **intelligent insights** from your data
5. View chat history and AI recommendations

---

## **API Providers**

* **OpenAI GPT**: Requires API key from [OpenAI Platform](https://platform.openai.com/api-keys)
* **Google Gemini**: Requires API key from [Google AI Studio](https://aistudio.google.com/)
* **Anthropic Claude**: Requires API key from [Anthropic Console](https://console.anthropic.com/)
* **Custom API**: Can use Hugging Face, local models, or other LLM endpoints

---

## **Demo Mode**

Enable **Demo Mode** in the sidebar to test the chatbot without any API key. The bot will generate pre-defined responses for demonstration purposes.

---

## **Tech Stack**

* Python
* Streamlit
* Pandas, NumPy
* Plotly (for visualization)
* Requests (for API calls)
* OpenAI / Google Gemini / Anthropic / Custom LLM APIs

---

## **Future Enhancements**

* Automatic chart generation from AI recommendations
* Follow-up questions from AI for deeper analysis
* Export chat history and AI insights
* Token-efficient summarization for large datasets
* Deployment with secure API keys

---

## **Folder Structure Suggestion**

```
ai-data-chatbot/
├── app.py                   # Main Streamlit app
├── pages/                   # Optional: multi-page Streamlit components
├── utils/                   # Helper functions and modules
│   ├── ai_chatbot.py
│   └── data_utils.py
├── requirements.txt         # Python dependencies
├── README.md
└── sample_data/             # Example CSV/Excel files
```

---

## **Requirements**

```txt
streamlit>=1.25.0
pandas>=2.0.0
numpy>=1.25.0
plotly>=5.15.0
requests>=2.31.0
openai>=1.9.0
google-generativeai>=0.1.0
anthropic>=0.2.0
```

> Optional: If you don’t use Google Gemini or Anthropic, you can skip installing those libraries.

---

## **License**

This project is licensed under the MIT License.

```

---

If you want, I can also **create a `requirements_full.txt` with exact versions that I know work with your code**, so anyone can run your chatbot without any errors.  

Do you want me to do that next?
```
