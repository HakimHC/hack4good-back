import sys
from typing import Union, List

import os
import ast
from dotenv import load_dotenv
import json
import openai
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI


def get_info_from_database(supermarket_path):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    new_vectorstore = FAISS.load_local(
        supermarket_path, embeddings, allow_dangerous_deserialization=True
    )
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(
            # engine="gpt-4-1106-preview",
            temperature=0.0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        ),
        chain_type="stuff",
        retriever=new_vectorstore.as_retriever(),
        verbose=True,
    )
    return qa


class Agent:
    def __init__(self, prompt):
        load_dotenv()
        self.prompt = prompt

        self.meal_type = ["breakfast", "lunch", "dinner"]

        self.data = {}
        self.res = []
        self.init_data()

    def init_data(self):
        option_from_prompt = self.orchestrator()
        if option_from_prompt == "1":
            self.diet_expert()
        elif option_from_prompt == "2":
            self.recipe_ingredient_analyzer(self.prompt)
        elif option_from_prompt == "3":
            self.get_prices_from_supermarkets(self.prompt)

    def orchestrator(self):
        template = """given this prompt {prompt},, analyze its content to determine its primary focus. Your task is 
        to categorize the prompt based on the following options: If the prompt is related to creating or following a diet 
        plan, choose '1'. If the prompt involves identifying ingredients required for a particular recipe, choose '2'. If 
        the prompt is focused on obtaining current prices for specific ingredients, choose '3'. If the prompt does not 
        fit any of the above categories, select '4'. Respond with the number corresponding to the most relevant 
        category."""

        prompt_template = PromptTemplate(input_variables=["prompt"], template=template)

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

        chain = LLMChain(llm=llm, prompt=prompt_template)
        response = chain.invoke({"prompt": self.prompt})
        return response["text"]

    def diet_expert(self):
        diet_scheme = """
        {
            "meals": [
            {
                "day": "1",
                "breakfast": "Avena con plátano y nueces",
                "lunch": "ensalada de quinoa con vegetales",
                "dinner": "sopa de lentejas"
            },
        """

        messages = [{
            "role": "system",
            "content": f"""Based on the user's dietary preferences, restrictions, and goals, generate a JSON response 
            containing a list of suggested meals, if the number of days is not specified, only answer for 1 day. The 
            meals should be diverse, nutritionally balanced, and tailored to the user's specific needs. Ensure the 
            response is formatted as a JSON object formatted like this example {diet_scheme}, it should be in spanish
                     """},
            {'role': 'user', 'content': self.prompt}]

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        response_string = response.choices[0].message.content
        day_meals = json.loads(response_string)["meals"]
        for meals in day_meals:
            print("MEAL", meals)
            for meal_type in self.meal_type:
                self.tmp_res = {}
                self.recipe_ingredient_analyzer(meals[meal_type])
                self.res.append({meal_type: self.tmp_res})

    def recipe_ingredient_analyzer(self, prompt):
        ingredient_scheme = """
             ["Salsa de tomate", "Queso mozzarella fresco", "Albahaca fresca", "Aceite de oliva virgen extra"]
        """
        messages = [
            {
                "role": "system",
                "content": f"""For any given meal mentioned by the user, provide a list of up to four main ingredients 
                required to " prepare the meal. Focus on the key ingredients that are essential for the dish, 
                ensuring the list has a maximum of 3 ingredients and is concise and relevant. the output would be a json 
                in spanish like this example {ingredient_scheme}."""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        self.tmp_res["description"] = prompt
        self.tmp_res["ingredients"] = []
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response_string = response.choices[0].message.content
        list_ingredient = ast.literal_eval(response_string)
        # data = json.loads(response_string)
        # ingredients_list = data

        # The ingredients_list variable now holds the list of ingredients
        print("List ingredients: ", list_ingredient)
        for ingredient in list_ingredient:
            res = self.get_prices_from_supermarkets(ingredient)
            _dct = {"name": ingredient, "items": res}
            self.tmp_res["ingredients"].append(_dct)

    def get_prices_from_supermarkets(self, prompt):
        load_dotenv()

        qa_dia = get_info_from_database(os.environ.get("VEC_DIA"))
        qa_mercadona = get_info_from_database(os.environ.get("VEC_MERCADONA"))
        qa_carrefour = get_info_from_database(os.environ.get("VEC_CARREFOUR"))

        output_scheme = """
        {
                            "name": "Aceite de oliva",
                            "items":
                                {
                                    "product": "Aceite oliva virgen Carbonell botella 1 l"
                                    "market": "Dia",
                                    "price": 10,
                                    "url": "https://example.com/banana"
                                }

        """
        output_scheme_mercadona = """
        {
                            "name": "Aceite de oliva",
                            "items":
                                {
                                    "product": "Aceite oliva virgen Carbonell botella 1 l"
                                    "market": "Dia",
                                    "price": 10,
                                    "url": "https://example.com/banana"
                                    "img_url": "https://example.com/banana"
                                }

        """

        # res = qa.run(f"supermarket")

        tmp = []

        try:
            res_dia = qa_dia.run(f""" find me  information about this product  {prompt}, get me  the product name,
            market, price and url. I want only one product, the cheapest option, the out put should be formatted like this: {output_scheme}
        """)
            print(res_dia)
            item_res = json.loads(res_dia)["items"][0]
            tmp.append(item_res)
        except Exception as e:
            print(f"ERROR: {e}")

        try:
            res = qa_carrefour.run(f""" find me  information about this product  {prompt}, get me  the product name,
            market, price and url. I want only one product, the cheapest option, the out put should be formatted like this: {output_scheme}
        """)
            print(res)
            item_res = json.loads(res)["items"][0]
            tmp.append(item_res)
        except Exception as e:
            print(f"ERROR: {e}")
        try:
            res = qa_mercadona.run(f""" find me  information about this product  {prompt}, get me  the product name,
                market, price url and img_url. I want only one product, the cheapest option, the out put should be formatted like this: {output_scheme_mercadona}
            """)
            print(res)
            item_res = json.loads(res)["items"][0]
            tmp.append(item_res)
        except Exception as e:
            print(f"ERROR: {e}")

        return tmp

    def get_res(self):
        return self.res



if __name__ == "__main__":
    print("Hello ReAct LangChain!")
    # orchestrator("cuanto cuesta una barra de pan")
    print("yeaaahhh")
    agent = Agent("hazme un menu sano para un dia, vegano y ligero")
    print(agent.get_res(), file=sys.stderr)

    res = agent.get_res()

    with open('out.json', 'w') as f:
        f.write(json.dumps(res, indent=2))
    # diet_expert("make a healthy diet for 2 days, i want to eat alien flesh")
    # recipe_ingredient_analyzer("Grilled salmon with quinoa and asparagus")
    # diet_expert("please solve the following equation: 3 + 3")
    # agent.get_prices_from_supermarkets()