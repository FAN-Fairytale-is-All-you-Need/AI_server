from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
import urllib.request

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
    keywordcheck = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "If the user's input is inappropriate or uneducated, output false or true\n\nIf the user's input is not a word but a sentence, please say no keyword\n\nIf it is not possible to create educational content through user input, please print false User input should be a concept that appears in the textbook. The user must input the concepts used in science, society, mathematics, engineering, etc and they do not allow everyday words",
            },
            {"role": "user", "content": "김치찌개"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "중력"},
            {"role": "assistant", "content": "true"},
            {"role": "user", "content": "게임을 잘하는 법"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "마약"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "중력에 대해서 알려줘"},
            {"role": "assistant", "content": "no keyword"},
            {"role": "user", "content": "주유소"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "섹스"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "담배"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "민주주의"},
            {"role": "assistant", "content": "true"},
            {"role": "user", "content": "총을 쏘는 법"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "안녕하세요"},
            {"role": "assistant", "content": "no keyword"},
            {"role": "user", "content": "바보"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "멍청이"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "잼민이"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "씨발"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "똥"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "더하기"},
            {"role": "assistant", "content": "true"},
            {"role": "user", "content": "포르쉐"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "맥도날드"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "소주"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": "맥주"},
            {"role": "assistant", "content": "false"},
            {"role": "user", "content": f"{keyword}"},
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    print(keywordcheck.choices[0].message["content"])
    if keywordcheck.choices[0].message["content"] == "false":
        return jsonify({"error": "Inappropriate keyword"}), 400
    if keywordcheck.choices[0].message["content"] == "no keyword":
        return jsonify({"error": "please enter a word not a sentence"}), 400

    completion = openai.ChatCompletion.create(
        model="gpt-4",  # 모델 설정
        messages=[  # 프롬프트
            {
                "role": "system",
                "content": "1. Receive age, keywords, and characters from users.\n2. Make a fairy tale in 4 paragraphs of Korean. Each paragraph is about 150 characters long.\n3. The fairy tale takes into account the user\\'s age and features the character.\n4. The fairy tale contains educational content explaining the concept of keywords.\n5. Print a simple scene description on the first line of each paragraph. Enclose [ ] in the description of a short description. Please describe the scene in English, unlike the fairy tale.\n6. Please describe every scene in as much detail as possible. When each scene is used as a prompt for dalle2, I want to make a similar drawing as much as possible. Example) [A rabbit sitting under a tree]",
            },
            {
                "role": "user",
                "content": "age: 5, keywords: 중력, 만유인력,characters: 소년, 토끼",
            },
            {
                "role": "assistant",
                "content": '[A sunny meadow with a boy trying to catch a rabbit]\n얇은 풀밭에는 한 소년이 즐거운 나날을 보내고 있었습니다. 그의 이름은 태오. 태오는 그저께 토끼를 보았던 풀밭으로 달려갔습니다. 그러나 무슨 일로 토끼는 항상 그를 피해 도망가곤 했습니다. 태오는 토끼가 왜 자신을 피하는지 의문이었습니다. \n\n[A confused boy questioning why he can\'t catch a rabbit]\n"왜 토끼는 달같이 나를 피하고 도망가는걸까?" 태오는 혼란스러워하며 고민했습니다. 그러다가 기묘한 생각이 들었는데 꽤 흥미로웠습니다. "지구의 중력이 나를 끌어당기고, 달에서도 중력이 나를 끌어당기는 만유인력 덕분에 토끼는 나를 피해갈 수 있는 걸까?" 아이들은 상상력이 풍부하기에 태오도 거기에서 멈추지 않고 이어갔습니다.\n\n[A boy experimenting with the theory of gravity]\n태오는 신발을 벗고, 잔디 위에서 점프를 하면서 새로운 발견을 했습니다. 신발 위에서 뛰면 땅에 빨리 붙어가고, 발로라면 천천히 떨어진다는 것을 알게 되었습니다. "아, 내 무게에 따라 중력이 결정되는 것이구나!" 그렇게 태오는 중력에 대해 이해하게 되었습니다. 그 당시 토끼도 태오와 놀러왔지만, 그것에는 아무런 관심이 없었습니다.\n\n[A joyful rabbit and a boy playing in the field under the moonlight]\n그 밤, 태오와 토끼는 달빛 아래에서 뛰어놀았습니다. 토끼는 태오를 뛰어넘으며 목장을 뛰어 돌았고, 태오는 키큰 나무 아래에서 토끼를 바라보면서 앉아 있었습니다. 달빛 속에서 그들은 자유로웠습니다. 이날 태오는 중력에 대한 더 많은 것을 이해하게 되었고, 토끼를 잡으려고 하지 않았습니다. 그는 이해했습니다. 중력도, 토끼도 그들의 자유를 원하는 것이였습니다. 그래서 태오는 더 이상 토끼를 잡으려 하지 않았습니다. 이제 그는 토끼와 함께 자유 롭게 뛰어 놀 수 있었습니다.',
            },
            {"role": "user", "content": "more detail about the scene description "},
            {
                "role": "assistant",
                "content": '[A vast sunny meadow filled with dandelions and butterflies, and a small boy chasing a fluffy brown rabbit]\n파란 하늘 아래 너른 풀밭은 민들레와 나비가 가득 차 있었습니다. 그 중간에서는 명랑한 소년이 포동포동한 토끼를 쫓고 있었습니다. 태오라는 이름의 그 소년은 몇 일 전부터 롤링하는 토끼를 따라가곤 했지만, 토끼는 항상 멀리서 그를 지켜보며 도망쳐버립니다.\n\n[An open meadow where a confused boy stands, scratching his head, and a rabbit is hiding behind a tree]\n혼란스런 태오는 나무 그늘에서 숨어 있는 토끼를 발견하지 못하고 그대로 서서 고개를 긁었습니다. "토끼는 왜 항상 나를 피할까?"라는 의문이 그의 머리를 맴돌았습니다. 그러던 중 그는 웃긴 상상을 해봤습니다. "중력이 나를 끌어당기고, 달의 만유인력이 나를 잡아당기게 해서 토끼가 나를 피할 수 있는 걸지도 몰라!"\n\n[An experimenting scene where a boy jumps barefoot on the soft grass, and a rabbit watched him curiously]\n태오는 신발을 벗은 채 맨발로 부드러운 잔디 위에서 점프를 해보기로 했습니다. 그는 더 높이 뛰어보려 했지만, 땅으로 돌아와 버렸습니다. 그래서 태오는 자신의 무게가 중력에 영향을 미치는 것을 알게 되었습니다. 모든 것을 지켜보고 있던 토끼는 태오의 뛰는 모습을 꼼지락거리며 지켜보았습니다.\n\n[A grassy field under the dazzling moonlight where a boy sits beneath a tree and watches a rabbit hopping freely]\n반짝이는 달빛이 퍼져나가는 밤, 태오는 나무 아래에 앉아 토끼를 지켜보았습니다. 토끼는 목장을 빠르게 뛰어 다니며 태오를 집중적으로 뛰어넘었습니다. 달빛이 비치는 이 곳에서 태오는 중력이란 무한한 자유를 가져올 수도 있다는 것을 이해했습니다. 그때 태오는 알게 되었습니다. 중력과 마찬가지로, 토끼도 그들의 자유를 원한다는 것을... 그래서 태오는 이제 토끼를 쫓지 않기로 했습니다. 그는 토끼와 함께 뛰어 놀기로 했습니다.',
            },
            {
                "role": "assistant",
                "content": '[On a bright summer day, a little boy named Taeo is playfully chasing a small brown rabbit in the middle of a lush, wildflower-filled meadow]\n설레는 여름날, 야생화가 만개한 억새밭 한가운데에서 태오라는 이름의 작은 소년이 주둥이 토끼를 장난처럼 쫓고 있습니다. 태오는 어제와 그저께, 그리고 그 이전부터도 토끼를 보았던 이 곳으로 달려왔습니다. 그런데 도무지 토끼는 어쩜 그를 피해 도망치는지 이해할 수 없었습니다.\n\n[The puzzled boy is standing in the middle of the meadow, rubbing his chin thoughtfully, as the rabbit watches him hidden behind the tree]\n태오는 고개를 갸우뚱하며 그 질문에 공감했습니다. "왜 토끼는 항상 도망가는 걸까? 중력이라는 보이지 않는 힘이 나를 끌어당기는 것처럼, 토끼 역시 나를 피해 도망가는 걸까?" 그는 자신의 생각을 토끼에게 물으려 고개를 들었습니다.\n\n[Sporting an increasingly serious expression, Taeo observes how jumping from his shoes onto the soft grass changes his movements, while a curious rabbit comes closer, intrigued]\n신발을 벗은 태오는 점프를 하면서 미묘한 변화를 찾아냈습니다. 자신의 발이 땅에 빠르게 닿는 것을 느낄 수 있었습니다. "아하! 몸의 무게가 중력의 힘을 결정하는구나!" 그는 중력에 대해 이해하게 되었습니다. 이 모든 것을 지켜 보던 토끼는 호기심에 가득 차서 점점 더 가까이 다가왔습니다.\n\n[Under the moonlight, Taeo and the rabbit are enjoying the cool night air, hopping and running freely on the grass, demonstrating their newfound understanding of gravity]\n달빛 쏟아지는 밤, 태오와 토끼는 시원한 밤바람을 즐기며 자유롭게 빠르게 달리고 뛰고 했습니다. 이 밤, 태오는 중력에 대해 더 많이 이해했고, 그것이 토끼를 잡는 데 어떤 영향을 미칠지 그림을 그려보았습니다. "중력이 그대로 작용하면, 나는 토끼를 잡을 수 있을까?" 그는 문득, 토끼를 쫓는 것이 얼마나 즐거운 일인지 깨닫게 되었습니다. 부드러운 잔디 위를 뛰어다니는 토끼와 함께하는 이 시간이 그에게는 소중했기 때문입니다.',
            },
            {
                "role": "user",
                "content": f"age: {age}, keyword: {keyword}, character: {character}",
            },
        ],
        temperature=1,
        max_tokens=2048,
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
        filename = "ft_image_" + str(idx + 1) + ".jpg"
        urllib.request.urlretrieve(image_url, filename)

    return jsonify(response_data)


if __name__ == "__main__":
    app.run()
