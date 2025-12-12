from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
import re

class ModelRouter:
    def __init__(self):
        # Base and adapter IDs
        self.base_model_id = "Qwen/Qwen2.5-1.5B-Instruct"
        self.adapter_id = "DeepakJ1218/fingesg4"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[Router] Using device: {self.device}")

        # Load tokenizer (shared)
        print("[Router] Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model_id,
            trust_remote_code=True
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # ---- LOAD BASE MODEL (for general questions) ----
        print("[Router] Loading base model (general chat)...")
        self.base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        ).to(self.device)
        self.base_model.eval()

        # ---- LOAD SEPARATE COPY + ESG ADAPTER ----
        print("[Router] Loading ESG model (separate copy + adapter)...")
        esg_base = AutoModelForCausalLM.from_pretrained(
            self.base_model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        self.esg_model = PeftModel.from_pretrained(
            esg_base,
            self.adapter_id,
            trust_remote_code=True
        ).to(self.device)
        self.esg_model.eval()

        print("[Router] ✓ Both models loaded successfully!\n")

    # ESG/Finance keyword detector
    def is_esg_query(self, text):
        text = text.lower()
        keywords = [
            "esg", "environment", "carbon", "emissions", "sustainability",
            "sdg", "scope 1", "scope 2", "scope 3",
            "water usage", "pollution", "waste",
            "company", "report", "disclosure", "footprint"
        ]
        return any(k in text for k in keywords)

    # Text generation helper with configurable token limit
    def generate(self, model, prompt, max_tokens=100):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                top_p=0.9,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )

        text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        # Extract only response after "Assistant:"
        if "Assistant:" in text:
            text = text.split("Assistant:")[-1].strip()
        
        # Remove ALL hashtags
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    # Main predict function with conversation context support
    def predict(self, user_message: str, conversation_context: str = "") -> str:
        """Routes to model and returns clean response with performance logging."""
        import time
        
        start_time = time.time()
        
        try:
            # Log input metrics
            input_chars = len(user_message)
            print(f"\n{'='*60}")
            print(f"📥 INPUT: {input_chars} characters")
            if conversation_context:
                print(f"📜 Context: Included")
            print(f"Query: {user_message[:100]}..." if len(user_message) > 100 else f"Query: {user_message}")
            
            # Detect simple greetings/small talk
            greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'thanks', 'thank you', 'ok', 'okay']
            is_greeting = any(greeting in user_message.lower() for greeting in greetings) and len(user_message.split()) <= 5
            
            if self.is_esg_query(user_message):
                # Use ESG fine-tuned model - FASTER with reduced tokens
                print(f"🎯 Model: ESG (fingesg3) | Max Tokens: 512")
                prompt = (
                    f"{conversation_context}"
                    f"You are an ESG & Finance specialist. Provide clear analysis using markdown.\n"
                    f"DO NOT add hashtags or emojis. Be professional and concise.\n\n"
                    f"User: {user_message}\nAssistant:"
                )
                
                gen_start = time.time()
                response = self.generate(self.esg_model, prompt, max_tokens=512)
                gen_time = time.time() - gen_start
                
                final_response = response  # Clean response without footer
            
            elif is_greeting:
                # SHORT response for greetings
                print(f"🎯 Model: Base (Qwen 2.5-1.5B) | Max Tokens: 50 (greeting)")
                prompt = (
                    f"{conversation_context}"
                    f"You are a friendly AI assistant. Give a brief, natural response.\n"
                    f"Keep it under 20 words. No explanations.\n\n"
                    f"User: {user_message}\nAssistant:"
                )
                
                gen_start = time.time()
                response = self.generate(self.base_model, prompt, max_tokens=50)
                gen_time = time.time() - gen_start
                
                # No footer for greetings
                final_response = response.strip()
            
            else:
                # Regular questions - medium response
                print(f"🎯 Model: Base (Qwen 2.5-1.5B) | Max Tokens: 250")
                prompt = (
                    f"{conversation_context}"
                    f"You are a helpful AI assistant. Answer the question clearly and concisely.\n"
                    f"Use the conversation history if available. Be accurate and brief.\n"
                    f"Stop when you've fully answered the question.\n\n"
                    f"User: {user_message}\nAssistant:"
                )
                
                gen_start = time.time()
                response = self.generate(self.base_model, prompt, max_tokens=250)
                gen_time = time.time() - gen_start
                
                final_response = response  # Clean response without footer
            
            # Calculate metrics
            total_time = time.time() - start_time
            output_chars = len(final_response)
            
            # Accurate token counting
            input_tokens = len(self.tokenizer.encode(user_message))
            output_tokens = len(self.tokenizer.encode(final_response))
            tokens_per_sec = output_tokens / gen_time if gen_time > 0 else 0
            
            # Log output metrics
            print(f"\n📤 OUTPUT: {output_chars} characters, {output_tokens} tokens")
            print(f"⏱️  Generation Time: {gen_time:.2f}s ({tokens_per_sec:.1f} tokens/sec)")
            print(f"⏱️  Total Time: {total_time:.2f}s")
            print(f"🔢 Input Tokens: {input_tokens} | Output Tokens: {output_tokens}")
            print(f"{'='*60}\n")
            
            return final_response
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return f"Error: {e}"


# Global instance for FastAPI
try:
    print("[Router] Initializing model instance...")
    model_instance = ModelRouter()
    print("[Router] ✓ Model instance ready for API calls\n")
except Exception as e:
    print(f"❌ CRITICAL ERROR: Failed to initialize model instance: {e}")
    print("⚠️  Application will start but model predictions will fail!")
    print("Please check:")
    print("  - GPU/CUDA availability")
    print("  - Hugging Face model download")
    print("  - Network connectivity")
    print("  - Disk space\n")
    model_instance = None  # Set to None to detect downstream
