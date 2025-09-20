from flask import Flask, jsonify, request
import tensorflow as tf
from transformers import AutoTokenizer, TFT5ForConditionalGeneration
import os
from flask_cors import CORS

# Model path to use the model further
model_path = os.path.join(os.path.dirname(__file__), '..', 'model_')
print(model_path)

# Loading Tokenizer ad tf model from model folder
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = TFT5ForConditionalGeneration.from_pretrained(model_path, from_pt=False)

app = Flask(__name__) # Flask app
CORS(app)

# Home route
@app.route('/', methods=["GET"])
def home():
    '''
    Home route to check if the app is running or not.
    '''
    print("You're in home page!")
    return jsonify({"service": "Policy Summarizer API", "status": "running"})


@app.route("/summarize", methods=["POST"])
def summarize():
    '''
    Summarizaer function that takes in text input from frontend in json form and returns summarized version of text!
    '''
    try:
        data = request.get_json() # PArses json input data
        print(data)
        
        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400
        
        text = data.get('text', '') # Retrives text from data
        
        if not text.strip():
            return jsonify({'error': 'Did not receive any Text!!'}), 400
        
        # Tokenizing the input text
        inputs = tokenizer('summarize: '+ text, return_tensors='tf', max_length= 512, truncation = True)
        
        # Generating the summary
        outputs = model.generate(inputs['input_ids'], max_length = 100, num_beams= 4, early_stopping=True)
        
        # Decoding the tokenized summary obtained
        summary = tokenizer.decode(outputs[0], skip_special_tokens = True)
        
        return jsonify({'summary': summary}) # Returns summary as json for frontend
    
    # Exceptional error handling
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Running the app
if __name__ == '__main__':
    app.run(debug=True)
