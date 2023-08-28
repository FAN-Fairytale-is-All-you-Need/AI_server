from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re

app = Flask(__name__)
CORS(app)

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/generate", methods=["POST"])
def process_data():
    data = request.get_json()  # JSON 데이터를 받아옴
    age = data.get("age")
    keyword = data.get("keyword")
    character = data.get("character")
    print(age, keyword, character)

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": '1. Receive age, keywords, and characters from users.\n2. Make a fairy tale in 4 paragraphs of Korean. Each paragraph is about 150 characters long.\n3. The fairy tale takes into account the user\'s age and features the character.\n4. The fairy tale contains educational content explaining the concept of keywords.\n5. Print a simple scene description on the first line of each paragraph. Enclose [ ] in the description of a short description. Please describe the scene in English, unlike the fairy tale.\n6. Scene descriptions are mainly subject-oriented. I\'m going to send it to dalle2 to create an image. Please describe the scene in English Example) [A rabbit sitting under a tree]\n\nBelow is an example of the results\n\n[A rabbit sitting under a thick tree in the jungle]\n어느 날, 깊은 정글 속에 살고 있는 귀여운 토끼가 나무 밑에 앉아 있었습니다. 그는 머리 위에 달린 사과를 보며 궁금해하였습니다. "왜 그 사과가 떨어지지 않을까요?" 토끼는 고개를 갸우뚱거렸습니다. 상상력이 풍부한 토끼는 어쩌면 나무에 사과를 매달아놓은 사람이 있을지도 모른다고 생각했습니다.\n\n[A rabbit looking at an apple with its chin resting on it]\n그때 갑자기, 바람이 세차게 불기 시작했습니다. 그 바람에 흔들리던 사과는 토끼의 머리 위에 떨어져 버렸습니다. 놀란 토끼는 왜 사과가 위에서 아래로 떨어졌는지 이해할 수 없었습니다. 이때, 숲에서 지내는 현명한 부엉이가 토끼에게 중력에 대해 설명해주었습니다. "중력은 모든 물체를 지구 중심으로 끌어당기는 힘이야." 토끼는 눈을 크게 뜨며 놀라워했습니다.\n\n[A scene where an owl explains gravity to a rabbit]\n부엉이는 다음으로 토끼에게 실험을 제안했습니다. "이번에는 돌과 꽃잎을 동시에 떨어트려 볼래? 중력은 모든 물체에 동일하게 작용하기 때문에, 무게와 상관없이 같은 시간에 땅에 닿게 될 거야." 토끼는 부엉이의 말에 의문을 가지며 돌과 꽃잎을 동시에 떨어트려 보았습니다. 그런데 너무 놀랍게도 돌과 꽃잎이 동시에 땅에 닿았습니다.\n\n[A surprised rabbit and a proudly smiling owl]\n토끼는 중력에 대한 새로운 사실을 알게 되어 눈이 반짝반짝 빛났습니다. 그리고 그날부터는 자신이 뛰어갈 때나 물건을 떨어트릴 때마다 중력을 느꼈습니다. 부엉이는 토끼의 표정을 보며 웃었습니다. 그것은 토끼가 세상을 이해하려고 열심히 노력하는 모습이 자랑스러웠기 때문입니다. 그래서 토끼는 중력이라는 힘을 알게 되었고, 더욱 지혜롭게 세상을 바라보게 되었습니다.',
            },
            {
                "role": "user",
                "content": f"age: {age}, keyword: {keyword}, character: {character}",
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    print(completion)
    text = completion.choices[0].message["content"]

    pattern = r"\[([^\[\]]+)\]([^[]+)"
    matches = re.findall(pattern, text)

    response_data = {}
    for idx, (scene_title, scene_content) in enumerate(matches):
        response = openai.Image.create(
            prompt=scene_title.strip() + "in fairy tale style",
            n=1,
            size="256x256",
            response_format="url",
        )

        image_url = response["data"][0]["url"]
        response_data[f"scene{idx+1}_text"] = scene_content.strip()
        response_data[f"scene{idx+1}_image_url"] = image_url

    # print(response_data)

    return jsonify(response_data)


if __name__ == "__main__":
    app.run()
