import pdfplumber
import pandas as pd

class Pdfextractor:
    
    def __init__(self):
        self.keywords = [
            'revenue', 'sales', 'income', 'profit', 'loss', 
            'assets', 'liabilities', 'equity', 'cash', 'debt',
            'balance sheet', 'income statement', 'cash flow',
            'ebitda', 'gross profit', 'net income', 'expenses'
        ]
    
    def pdf_extractor(self, pdf_path: str):
        try:
            with pdfplumber.open(pdf_path) as file:
                all_texts = ''
                all_tables = []
                
                for page_num, page in enumerate(file.pages):
                    text = page.extract_text()
                    if text:
                        all_texts += f'\n--- Page {page_num+1} ---\n{text}'
                    
                    tables = page.extract_tables()
                    for table_num, table in enumerate(tables):
                        if table and any(any(cell for cell in row) for row in table):
                            data = pd.DataFrame(table)
                            
                            all_tables.append({
                                "page_num": page_num+1,
                                'table_num': table_num+1,
                                'data': data,
                                'is_financial': self.isfinancial(table)
                            })
                            
                return {
                    'text': all_texts,
                    'tables': all_tables,
                    'total_pages': len(file.pages)
                }
                
        except Exception as e:
            print(f"File Processing error: {e}")
            return {'text': '', 'tables': [], 'total_pages': 0}
        
    
    def isfinancial(self, table) -> bool:
        search_text = ''
        
        for row in table:
            for cell in row:
                if cell:
                    search_text += str(cell).lower() + ' '
                    
        return any(keyword in search_text for keyword in self.keywords)

