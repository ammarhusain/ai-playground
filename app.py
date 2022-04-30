import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = "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" #os.getenv("OPENAI_API_KEY")

conversation_prompt = [{'you': 'What does HTML stand for?', 
                        'me': 'Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.'},
                        {'you': 'When did the first airplane fly?',
                        'me': 'On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.'},
                        {'you': 'What is the meaning of life?',
                        'me': 'I’m not sure. I’ll ask my friend Google.'},
                        {'you': 'Why is the sky blue?',
                        'me': 'You really ask dumb questions. Its refraction of light'}
                    ]


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        msg = request.form["animal"]
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=generate_prompt(msg),
            temperature=0.9,
            max_tokens=500,
        )
        model_response = response.choices[0].text
        print(f"model_response : {response.choices}")
        conversation_prompt.append({'you': msg, 'me': model_response})
        return redirect(url_for("index", result=model_response))


    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(msg):
    prompt = """Ammar is a highly intelligent question answering chatbot that reluctantly answers questions with sarcastic responses. His responses are rooted in truth.:

    """
    for chat in conversation_prompt:
        prompt += "You: " + chat['you'] + '\n'
        prompt += "Ammar: " + chat['me'] + '\n'

    prompt  += "You: " + msg.capitalize() + "\nAmmar: "
    print(f"prompt: {prompt}")
    return prompt

if __name__ == "__main__":
    app.run()