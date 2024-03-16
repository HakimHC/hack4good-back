from flask import Flask, request, jsonify
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
import os
from agents import Agent


app = Flask(__name__)


@app.route('/', methods=['POST'])
def greet():
    try:
        data = request.get_json()
        prompt = data.get('prompt')

        print(f'Prompt: {prompt}')

        agent = Agent(prompt)
        ret = agent.get_res()
    except Exception as e:
        print(e)
        ret = {}

    return jsonify({"data": ret})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
