# Financial Analysis Bot

A powerful AI-powered financial analysis assistant that can extract and analyze information from financial PDF documents. Built with Streamlit, ChromaDB, and the Deepseek AI model.



## 🌟 Features

- **PDF Document Processing**: Extract text and financial tables from PDF files
- **Intelligent Q&A**: Ask questions about your financial documents and get AI-powered answers
- **Vector Database**: Efficient document retrieval using ChromaDB and sentence transformers
- **Offline Capability**: Works with or without internet connection
- **Financial Focus**: Specifically tuned for financial document analysis
- **Dual Interface**: Web app (Streamlit) and command-line interface

## 📁 Project Structure

```
Financial_assistantLLM/
├── app.py                 # Main Streamlit web application
├── financial_chatbot.py   # Command-line chatbot interface
├── ai_analyzer.py        # Deepseek AI model integration
├── pdf.py               # PDF text and table extraction
├── vector_store.py      # ChromaDB vector database management
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/Raseen005/Financial_assistantLLM.git
cd Financial_assistantLLM
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Application**

**Option 1: Web Interface (Recommended)**
```bash
streamlit run app.py
```

**Option 2: Command Line Interface**
```bash
python financial_chatbot.py
```

## 💻 Usage

### Web Interface

1. **Start the application**: Run `streamlit run app.py`
2. **Upload PDF**: Use the file uploader to upload a financial PDF document
3. **Ask Questions**: Once processed, type your questions in the chat interface

**Example Questions:**
- "What was the company's revenue last year?"
- "Show me the balance sheet details"
- "Calculate the profit margin"
- "What are the main assets listed?"

### Command Line Interface

1. **Place PDF**: Put your PDF file in the same directory as `financial_chatbot.py`
2. **Run chatbot**: Execute `python financial_chatbot.py`
3. **Ask questions**: Type your financial questions at the prompt
4. **Exit**: Type 'quit', 'exit', or 'end'

## 🔧 How It Works

### Architecture Overview

1. **PDF Extraction**: Uses `pdfplumber` to extract text and identify financial tables
2. **Vector Storage**: Converts documents into embeddings stored in ChromaDB
3. **AI Analysis**: Leverages Deepseek-Coder model for financial question answering
4. **Context Retrieval**: Finds relevant document sections for each query
5. **Response Generation**: Provides accurate, context-aware answers

### Technical Details

- **Model**: `deepseek-ai/deepseek-coder-1.3b-instruct`
- **Embeddings**: `all-MiniLM-L6-v2` sentence transformer
- **Vector DB**: ChromaDB with persistent storage
- **Chunking**: 1000-character chunks with 200-character overlap

## 📊 Supported Document Types

- Annual reports and financial statements
- Balance sheets and income statements
- Cash flow statements
- Quarterly financial reports
- Audit reports
- Financial presentations

## ⚙️ Configuration

### Model Settings

The application automatically downloads and caches the Deepseek model locally. On first run, it will:
- Check for internet connection
- Download the model if not available locally
- Cache the model in `./models/` directory for offline use

### Vector Database

- Persistent storage in `./chroma_db/`
- Automatic cleanup on new document upload
- Efficient similarity search for relevant content

## 🛠️ Troubleshooting

### Common Issues

**Model Download Fails:**
- Check internet connection
- Ensure sufficient disk space (~2GB for model)
- Verify firewall settings

**PDF Processing Errors:**
- Verify PDF is not password protected
- Ensure PDF contains extractable text (not scanned images)
- Check PDF file integrity

**Memory Issues:**
- Close other memory-intensive applications
- For large PDFs, ensure adequate RAM
- Consider using CPU-only mode if GPU memory is limited

### Performance Tips

- GPU recommended for faster inference
- Process one document at a time for optimal performance
- Keep questions specific and focused for better accuracy
- Initial processing may take longer for large documents

## 🎯 Example Use Cases

```python
# Example financial analysis queries:
- "What is the net income for the last quarter?"
- "Compare current assets vs current liabilities"
- "What are the major expense categories?"
- "Show me the revenue growth trend"
- "Calculate debt-to-equity ratio"
```

