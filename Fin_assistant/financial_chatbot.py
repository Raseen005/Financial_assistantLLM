from pdf import Pdfextractor
from vector_store import Vectorstore
from ai_analyzer import Deepseek
import os

class Financial_bot:
    
    def __init__(self):
        self.extractor = Pdfextractor()
        self.store = Vectorstore()
        self.ai = Deepseek()
        self.loaded_documents = []
        self.store.delete_information()
        self.process_pdf()
    
    def process_pdf(self):
        """Find and process the first PDF file found"""
        path = ''
        for file in os.listdir('.'):
            if file.endswith('.pdf'):
                path = file
                break       
        if not path:  
            print("No PDF files found in directory")
            return False
        
        try:
            if not os.path.exists(path):
                return False
            
            pdf_data = self.extractor.pdf_extractor(path)
            
            self.store.add_documents(pdf_data, path)  
            self.loaded_documents.append(path)
            
            print("Data Processed Successfully")
            return True
            
        except Exception as e:
            print(f" Data Load Failed: {e}")
            return False
        
        
    def ask_question(self, question: str) -> str:
        """Ask question - automatically processes PDF first"""
        
        
        
        if not self.loaded_documents:
            return " Documents are not loaded or PDF is empty"
        
        # Search for relevant information
        context = self.store.search_query(query=question, n_inputs=3)
        
        if not context['documents'][0]:
            return " No relevant information found"
        
        # Prepare context for AI
        context_text = '\n\n'.join(context['documents'][0])
        
        print(" Thinking...")
        
        # Get AI answer
        answer = self.ai.analyze_financial_question(question=question, context=context_text)
        
        return answer

if __name__ == '__main__':
    bot = Financial_bot()


    print("Financial Bot - Ask questions about your PDF!")
    print("Make sure you have a PDF file in the same folder")
    print("-" * 50)

    to_exit = ['quit', 'exit', 'end']

    while True:
        question = input("Ask about the company financial health > ")
        if question.lower() in to_exit:
            print('\n')
            print("Bye....")
            break
        
        print(bot.ask_question(question=question))
        print("type quit to exit the chat..")

        