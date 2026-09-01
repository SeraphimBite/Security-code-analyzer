"""
Example: Using a trained model for inference on new code
"""

import torch
from transformers import AutoTokenizer

# Assuming you've trained a model and saved it
from vulnerability_detection_improved import CodeT5PoolingClassifier, Config

def predict_vulnerability(code_snippet, model_path='outputs/best_model_attention.pt'):
    """
    Predict if a code snippet is vulnerable
    
    Args:
        code_snippet: String containing the code to analyze
        model_path: Path to trained model checkpoint
        
    Returns:
        dict: Prediction result with confidence scores
    """
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
    
    # Load model
    checkpoint = torch.load(model_path, map_location=Config.DEVICE)
    pooling_method = checkpoint.get('pooling', 'attention')
    
    model = CodeT5PoolingClassifier(Config.MODEL_NAME, pooling=pooling_method)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(Config.DEVICE)
    model.eval()
    
    # Tokenize input
    inputs = tokenizer(
        code_snippet,
        return_tensors="pt",
        truncation=True,
        max_length=Config.MAX_LEN,
        padding="max_length"
    )
    
    # Move to device
    input_ids = inputs['input_ids'].to(Config.DEVICE)
    attention_mask = inputs['attention_mask'].to(Config.DEVICE)
    
    # Predict
    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        probs = torch.softmax(logits, dim=1)
        prediction = torch.argmax(logits, dim=1).item()
        confidence = probs[0][prediction].item()
    
    return {
        'is_vulnerable': bool(prediction),
        'confidence': confidence,
        'vulnerability_probability': probs[0][1].item(),
        'safe_probability': probs[0][0].item()
    }


# Example Usage
if __name__ == "__main__":
    
    # Example 1: Buffer overflow vulnerability
    vulnerable_code = """
    void copy_data(char *input) {
        char buffer[10];
        strcpy(buffer, input);  // Potential buffer overflow
    }
    """
    
    result = predict_vulnerability(vulnerable_code)
    print("Example 1: Buffer Overflow")
    print(f"  Vulnerable: {result['is_vulnerable']}")
    print(f"  Confidence: {result['confidence']:.2%}")
    print(f"  Vulnerability Probability: {result['vulnerability_probability']:.2%}\n")
    
    
    # Example 2: Safe code with bounds checking
    safe_code = """
    void copy_data(char *input) {
        char buffer[10];
        strncpy(buffer, input, sizeof(buffer) - 1);
        buffer[sizeof(buffer) - 1] = '\\0';
    }
    """
    
    result = predict_vulnerability(safe_code)
    print("Example 2: Safe Code")
    print(f"  Vulnerable: {result['is_vulnerable']}")
    print(f"  Confidence: {result['confidence']:.2%}")
    print(f"  Vulnerability Probability: {result['vulnerability_probability']:.2%}\n")
    
    
    # Example 3: SQL Injection vulnerability
    sql_injection_code = """
    void execute_query(char *user_input) {
        char query[256];
        sprintf(query, "SELECT * FROM users WHERE name='%s'", user_input);
        execute_sql(query);
    }
    """
    
    result = predict_vulnerability(sql_injection_code)
    print("Example 3: SQL Injection")
    print(f"  Vulnerable: {result['is_vulnerable']}")
    print(f"  Confidence: {result['confidence']:.2%}")
    print(f"  Vulnerability Probability: {result['vulnerability_probability']:.2%}\n")
