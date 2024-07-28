import openai
import os
from flask import Flask, request, jsonify, send_from_directory
import random

app = Flask(__name__)

# 環墁E��数からAPIキーを取征E
openai.api_key = os.getenv('OPENAI_API_KEY')

# 卦のリスト（例！E
hexagrams = [
    "䷀ 乾 Qián", "䷁E坤 Kūn", "䷁E屯 Zhūn", "䷁E蒁EMéng", "䷁E需 Xū",
    "䷁E訁ESòng", "䷁E師 Shī", "䷁E毁EBǁE, "䷁E小畜 Xiǎo Chù", "䷁E履 LǁE,
    "䷁E泰 Tài", "䷁E否 PǁE, "䷁E同人 Tóng Rén", "䷁E大朁EDà Yǒu", "䷁E謁EQiān",
    "䷁E豫 Yù", "䷁E隨 Suí", "䷁E蠱 GǁE, "䷁E臨 Lín", "䷁E觀 Guān",
    "䷁E噬嗁EShì Kè", "䷁E賁EBì", "䷁E剁EBŁE, "䷁E復 Fù", "䷁E無妁EWú Wàng",
    "䷁E大畁EDà Chù", "䷁E頤 Yí", "䷁E大遁EDà Guò", "䷁E坁EKǎn", "䷁E離 Lí",
    "䷁E咸 Xián", "䷁E恁EHéng", "䷠ 遯 Dùn", "䷡ 大壯 Dà Zhuàng", "䷢ 晁EJìn",
    "䷣ 明夷 Míng Yí", "䷤ 家人 JiāERén", "䷥ 睽 Kuí", "䷦ 蹁EJiǎn",
    "䷧ 解 Xiè", "䷨ 搁ESǔn", "䷩ 盁EYì", "䷪ 夬 Guài", "䷫ 姤 Gòu",
    "䷬ 萁ECuì", "䷭ 十EShēng", "䷮ 困 Kùn", "䷯ 亁EJǐng", "䷰ 革 Gé",
    "䷱ 鼁EDǐng", "䷲ 霁EZhèn", "䷳ 艮 Gèn", "䷴ 漸 Jiàn", "䷵ 歸妹 Guī Mèi",
    "䷶ 豁EFēng", "䷷ 旁ELǁE, "䷸ 巽 Xùn", "䷹ 允EDuì", "䷺ 渁EHuàn",
    "䷻ 節 Jié", "䷼ 中孁EZhōng Fú", "䷽ 小過 Xiǎo Guò", "䷾ 既濁EJì Jì",
    "䷿ 未濁EWèi Jì"
]

def get_advice_from_ai(question):
    hexagram = random.choice(hexagrams)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are an expert at providing clear and direct advice based on cosmic truths. Use the hexagram '{hexagram}' to derive the advice. Respond in Japanese."},
            {"role": "user", "content": f"User question: {question}\n\nProvide a concise yes or no answer and then a brief explanation based on your cosmic knowledge, but do not mention the hexagram."}
        ]
    )
    advice = response.choices[0].message.content.strip()
    if advice.endswith("、E):
        advice = advice[:-1]
    return advice

@app.route('/get_advice', methods=['POST'])
def get_advice():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    advice = get_advice_from_ai(question)
    return jsonify({"advice": advice})

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
