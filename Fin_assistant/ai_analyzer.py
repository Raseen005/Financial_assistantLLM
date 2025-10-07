from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import requests

class Deepseek:
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.conversation_history = []
        self.model_name = 'deepseek-ai/deepseek-coder-1.3b-instruct'
        self.local_model_path = './models/deepseek-coder-1.3b-instruct'
        
    def check_internet_connection(self):
        try:
            requests.get('https://huggingface.co', timeout=3)
            return True
        except Exception:
            return False
        
    def load_model(self):
        try:
            is_online = self.check_internet_connection()
            
            if os.path.exists(self.local_model_path):
                model_source = self.local_model_path
                local_only = True
                
            elif is_online:
                print("Downloading Model from Hugging Face Hub...")
                model_source = self.model_name   
                local_only = False
                
            else:
                return "No Internet Connection"
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_source,
                trust_remote_code=True,
                local_files_only=local_only
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_source,
                trust_remote_code=True,
                local_files_only=local_only,
                dtype=torch.float16 if self.device == 'cuda' else torch.float32,
                device_map='auto' if self.device == 'cuda' else None
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            self.model.save_pretrained(self.local_model_path)
            self.tokenizer.save_pretrained(self.local_model_path)
                
            return True
        
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
        
    def analyze_financial_question(self, question: str, context: str) -> str:
        if self.model is None:
            if not self.load_model():
                return "Check the internet connection or local model folder."
            
        try:
            prompt = f"""
You are a professional financial analyst. Use the following financial document content to answer the question.

FINANCIAL DOCUMENT CONTENT:
{context}

QUESTION: {question}

INSTRUCTIONS:
- Answer based ONLY on the document content.
- If info is missing, say: "The information is not available in the document."
- Be precise and professional.
- Include calculations when applicable.

ANSWER:
"""
            inputs = self.tokenizer.encode(prompt, return_tensors='pt')
            attention_mask = inputs.ne(self.tokenizer.pad_token_id).long()

            if self.device == 'cuda':
                inputs = inputs.to(self.device)
                attention_mask = attention_mask.to(self.device)

                
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=400,
                    attention_mask = attention_mask,
                    temperature=0.3,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            answer = full_response[len(prompt):]
            
            if 'ANSWER:' in answer:
                answer = answer.split('ANSWER:')[-1].strip()
                
            self.conversation_history.append({
                'question': question,
                'answer': answer,
                'context_preview': context[:200] + '...'
            })
            
            return answer
        
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "Error while generating answer."
        

