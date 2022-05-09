import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

generic_conversation_buffer = [{'you': 'What does HTML stand for?', 
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
        # Check for questions to Ammar-Bot
        ammar_question = request.form["ammar-question"]
        if len(ammar_question) > 0:
            response = openai.Completion.create(
                model="davinci:ft-personal:ammar-hangouts-chatbot-2022-04-30-17-15-40", #"davinci:ft-personal:ammmar-hangouts-chatbot-2022-04-30-01-23-28", #"text-davinci-001",
                prompt=ammar_question.capitalize() + '\n\n\n###\n\n',
                temperature=0.8,
                max_tokens=100,
            )
            ammar_response = response.choices[0].text[:response.choices[0].text.find('##END##')]
            print(f"Ammar-bot model_response : {response.choices}")
            return redirect(url_for("index", ammar_prompt=ammar_question, ammar_result=ammar_response))

        # Check for questions to Generic-Bot
        generic_question = request.form["generic-question"]
        if len(generic_question) > 0:
            print(f"Trying to answer {generic_question}")
            response = openai.Completion.create(
                model="text-davinci-001",
                prompt=generate_prompt(generic_question),
                temperature=0.8,
                max_tokens=100,
            )
            generic_response = response.choices[0].text[:response.choices[0].text.find('##END##')]
            generic_conversation_buffer.append({'you': generic_question.capitalize(), 'me': generic_response})
            print(f"Generic-bot model_response : {response.choices}")
            return redirect(url_for("index", generic_prompt=generic_question, generic_result=generic_response))

    return render_template("index.html", 
        ammar_prompt=request.args.get("ammar_prompt"),
        ammar_result=request.args.get("ammar_result"),
        generic_prompt=request.args.get("generic_prompt"),
        generic_result=request.args.get("generic_result")        
        )


def generate_prompt(msg):
    prompt  = msg.capitalize() + '\n\n\n###\n\n'

    print(f"prompt: {prompt}")
    return prompt

def generate_prompt(msg):
    prompt = """Ammar is a highly intelligent question answering human that has knowledge of all of the universe but reluctantly answers questions with sarcastic responses. 
                He tries to be funny but is not good at it. 
                His responses are rooted in truth.:

    """
    for chat in generic_conversation_buffer:
        prompt += "You: " + chat['you'] + '\n'
        prompt += "Ammar: " + chat['me'] + '\n'

    prompt  += "You: " + msg.capitalize() + "\nAmmar: "
    print(f"Generic prompt: {prompt}")
    return prompt

if __name__ == "__main__":
    app.run()

    