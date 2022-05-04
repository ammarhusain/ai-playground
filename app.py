import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = "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" #os.getenv("OPENAI_API_KEY")

conversation_prompt = [{'you': 'What does HTML stand for?', 
                        'me': 'Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.'},
                        {'you': 'When did the first airplane fly?',
                        'me': 'On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.'},
                        # {'you': 'What is the meaning of life?',
                        # 'me': 'I’m not sure. I’ll ask my friend Google.'},
                        # {'you': 'Why is the sky blue?',
                        # 'me': 'You really ask dumb questions. Its refraction of light'}
                    ]


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        ammar_question = request.form["ammar-question"]
        if len(ammar_question) > 0:
            response = openai.Completion.create(
                model="davinci:ft-personal:ammar-hangouts-chatbot-2022-04-30-17-15-40", #"davinci:ft-personal:ammmar-hangouts-chatbot-2022-04-30-01-23-28", #"text-davinci-001",
                prompt=generate_prompt(ammar_question),
                temperature=0.9,
                max_tokens=100,
            )
            model_response = response.choices[0].text[:response.choices[0].text.find('##END##')]
            print(f"model_response : {response.choices}")
            conversation_prompt.append({'you': ammar_question.capitalize(), 'me': model_response})
            return redirect(url_for("index", ammar_result=model_response))
        generic_question = request.form["generic-question"]
        if len(generic_question) > 0:
            print(f"Trying to answer {generic_question}")
            return redirect(url_for("index", generic_result="No fucking idea"))

    return render_template("index.html", 
        ammar_result=request.args.get("ammar_result"),
        generic_result=request.args.get("generic_result"))


def generate_prompt(msg):
    prompt  = msg.capitalize() + '\n\n\n###\n\n'

    print(f"prompt: {prompt}")
    return prompt

if __name__ == "__main__":
    app.run()

    