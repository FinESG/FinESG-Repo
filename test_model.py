from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
import torch
import traceback

# TODO: Replace with your actual model ID
MODEL_ID = "DeepakJ1218/finesg3"  # User provided model

def test_model():
    print(f"Loading model: {MODEL_ID}...")
    try:
        from transformers import AutoConfig
        config = AutoConfig.from_pretrained(MODEL_ID, trust_remote_code=True)
        print(f"Model Config: {config}")
        
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
        # Try generic AutoModel first to see if it loads
        from transformers import AutoModel
        model = AutoModel.from_pretrained(MODEL_ID, trust_remote_code=True)
        
        print("Model loaded successfully!")
        
        input_text = "The future of AI is"
        inputs = tokenizer(input_text, return_tensors="pt")
        
        print(f"Generating response for: '{input_text}'")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=50)
            
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_model()
