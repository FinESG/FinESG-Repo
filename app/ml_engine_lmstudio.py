from openai import OpenAI
import time

class SimpleTokenizer:
    """Simple tokenizer for counting tokens (approximate)"""
    def encode(self, text):
        # Rough estimate: ~4 chars per token
        return list(range(len(text) // 4))
    
    @property
    def eos_token_id(self):
        return 0

class ModelRouter:
    """Fast LM Studio-powered model (works with Qwen 1.5B or any loaded model)"""
    
    def __init__(self):
        # Connect to LM Studio local server
        self.client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"  # LM Studio doesn't need real key
        )
        
        # Provide simple tokenizer for context_helper
        self.tokenizer = SimpleTokenizer()
        
        print("✓ Connected to LM Studio server")
    
    def predict(self, user_message: str, conversation_context: str = "") -> str:
        """Generate response using LM Studio"""
        
        start_time = time.time()
        
        try:
            # Build messages
            messages = []
            
            # System prompt
            messages.append({
                "role": "system",
                "content": "You are an ESG (Environmental, Social, Governance) specialist. Provide clear, professional analysis."
            })
            
            # Add context if provided
            if conversation_context:
                messages[0]["content"] += f"\n\nContext:\n{conversation_context}"
            
            # User message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call LM Studio (works with whatever model is loaded)
            print(f"🎯 Model: LM Studio (fingesg4) | Max Tokens: 2000")
            response = self.client.chat.completions.create(
                model="local-model",
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                stream=False
            )
            
            result = response.choices[0].message.content.strip()
            
            total_time = time.time() - start_time
            print(f"⚡ LM Studio response in {total_time:.2f}s")
            print(f"📤 OUTPUT: {len(result)} characters")
            print(f"⏱️  Total Time: {total_time:.2f}s\n")
            
            return result
            
        except Exception as e:
            print(f"❌ LM Studio Error: {e}")
            return f"Error: Make sure LM Studio server is running on http://localhost:1234"


# Global instance
try:
    print("[LM Studio] Connecting...")
    model_instance = ModelRouter()
    print("[LM Studio] ✓ Ready!\n")
except Exception as e:
    print(f"❌ Failed: {e}")
    model_instance = None
