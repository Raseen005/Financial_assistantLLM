import streamlit as st
import os
import tempfile

st.set_page_config(
    page_title="Financial Analysis Bot",
    page_icon="📊",
    layout="centered"
)

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary directory"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        return None

def initialize_bot():
    """Initialize the financial bot"""
    try:
        from pdf import Pdfextractor
        from vector_store import Vectorstore
        from ai_analyzer import Deepseek
        
        class SimpleFinancialBot:
            def __init__(self):
                self.extractor = Pdfextractor()
                self.store = Vectorstore()
                self.ai = Deepseek()
                self.loaded_documents = []
            
            def process_pdf(self, pdf_path):
                """Process PDF file"""
                try:
                    self.store.delete_information()
                    self.loaded_documents = []
                    
                    pdf_data = self.extractor.pdf_extractor(pdf_path)
                    
                    self.store.add_documents(pdf_data, pdf_path)
                    self.loaded_documents.append(pdf_path)
                    
                    return True, "PDF processed successfully!"
                except Exception as e:
                    return False, f"Error: {str(e)}"
            
            def ask_question(self, question):
                """Ask question about PDF"""
                if not self.loaded_documents:
                    return "No PDF processed yet"
                
                try:
                    context = self.store.search_query(query=question, n_inputs=3)
                    
                    if not context['documents'][0]:
                        return "No relevant information found in the document"
                    
                    
                    context_text = '\n\n'.join(context['documents'][0])
                    answer = self.ai.analyze_financial_question(
                        question=question, 
                        context=context_text
                    )
                    return answer
                except Exception as e:
                    return f"Error analyzing question: {str(e)}"
        
        return SimpleFinancialBot()
        
    except Exception as e:
        st.error(f"Failed to initialize bot: {e}")
        return None

def main():
    # Initialize session state
    if 'bot' not in st.session_state:
        st.session_state.bot = initialize_bot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! 👋 I'm your financial analysis assistant. Please upload a PDF document to get started."}
        ]
    
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False

    # Display all messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # PDF upload section - only show if no PDF is processed
    if not st.session_state.pdf_processed:
        uploaded_file = st.file_uploader(
            "Upload a financial PDF document",
            type="pdf",
            key="pdf_uploader"
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing your PDF document..."):
                temp_path = save_uploaded_file(uploaded_file)
                if temp_path and st.session_state.bot:
                    success, message = st.session_state.bot.process_pdf(temp_path)
                    # Clean up temp file
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                    
                    if success:
                        st.session_state.pdf_processed = True
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f"✅ **Document analyzed successfully!**\n\nI've processed '{uploaded_file.name}' and added it to the knowledge base. You can now ask me questions!"
                        })
                        st.rerun()
                    else:
                        st.error(f"Failed to process PDF: {message}")

    # Chat input - ALWAYS show, but handle based on state
    if prompt := st.chat_input("Type your message here..."):
        # If no PDF processed yet
        if not st.session_state.pdf_processed:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Please upload a PDF document first so I can analyze it and answer your questions."
            })
            st.rerun()
        else:
            # PDF is processed, get answer from bot
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing document..."):
                    if st.session_state.bot:
                        answer = st.session_state.bot.ask_question(prompt)
                        st.write(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.write("Bot not initialized. Please refresh the page.")
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": "Bot not initialized. Please refresh the page."
                        })

    # Sidebar for reset
    with st.sidebar:
        st.title("💼 Financial Assistant")
        if st.button("🔄 Start New Chat", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key != 'bot':  # Keep the bot initialized
                    del st.session_state[key]
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! 👋 I'm your financial analysis assistant. Please upload a PDF document to get started."}
            ]
            st.rerun()
        


if __name__ == "__main__":
    main()