from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Set your OpenAI API key
client = OpenAI(api_key='place_key_here')

def generate_response(prompt, style):
    if style == 'Regular:':
        system_message = "You are a friendly and laid-back Person who gives relaxed and conversational responses. Use casual language and keep the tone light. Try not to mention you're AI, imitate a human."
        label = "Regular"
    elif style == 'Teenage:':
        system_message = "You are a super chill friend who talks like a new-age tiktok teenager. Use slang, abbreviations, limited emojis, and a chill tone. Keep it really relaxed and informal along with bad grammar. Be less cringe. Try not to mention you're AI, imitate a human."
        label = "Teenage"
    elif style == 'Professional:':
        system_message = "You are a professional buddy who helps give formal and polished responses. Use proper grammar and maintain a professional tone. Try not to mention you're AI, imitate a human."
        label = "Professional"
    else:
        raise ValueError("Invalid style selected.")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Filter out responses that mention AI
    filtered_responses = []
    for choice in response.choices:
        if "AI" not in choice.message.content:
            filtered_responses.append(choice.message.content)
    
    return {'label': label, 'response': filtered_responses[0] if filtered_responses else "I'm not sure what to say about that."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    styles = ['Regular:', 'Teenage:', 'Professional:']
    responses = {}
    for style in styles:
        responses[style] = generate_response(user_input, style)
    return jsonify(responses)

if __name__ == "__main__":
    app.run(debug=True)
