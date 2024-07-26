import openai
import os
from flask import Flask, request, jsonify, send_from_directory
import random

app = Flask(__name__)

# 環境変数からAPIキーを取得
openai.api_key = os.getenv('OPENAI_API_KEY')

# 卦のリスト（例）
hexagrams = [
    "䷀ 乾 Qián", "䷁ 坤 Kūn", "䷂ 屯 Zhūn", "䷃ 蒙 Méng", "䷄ 需 Xū",
    "䷅ 訟 Sòng", "䷆ 師 Shī", "䷇ 比 Bǐ", "䷈ 小畜 Xiǎo Chù", "䷉ 履 Lǚ",
    "䷊ 泰 Tài", "䷋ 否 Pǐ", "䷌ 同人 Tóng Rén", "䷍ 大有 Dà Yǒu", "䷎ 謙 Qiān",
    "䷏ 豫 Yù", "䷐ 隨 Suí", "䷑ 蠱 Gǔ", "䷒ 臨 Lín", "䷓ 觀 Guān",
    "䷔ 噬嗑 Shì Kè", "䷕ 賁 Bì", "䷖ 剝 Bō", "䷗ 復 Fù", "䷘ 無妄 Wú Wàng",
    "䷙ 大畜 Dà Chù", "䷚ 頤 Yí", "䷛ 大過 Dà Guò", "䷜ 坎 Kǎn", "䷝ 離 Lí",
    "䷞ 咸 Xián", "䷟ 恒 Héng", "䷠ 遯 Dùn", "䷡ 大壯 Dà Zhuàng", "䷢ 晉 Jìn",
    "䷣ 明夷 Míng Yí", "䷤ 家人 Jiā Rén", "䷥ 睽 Kuí", "䷦ 蹇 Jiǎn",
    "䷧ 解 Xiè", "䷨ 損 Sǔn", "䷩ 益 Yì", "䷪ 夬 Guài", "䷫ 姤 Gòu",
    "䷬ 萃 Cuì", "䷭ 升 Shēng", "䷮ 困 Kùn", "䷯ 井 Jǐng", "䷰ 革 Gé",
    "䷱ 鼎 Dǐng", "䷲ 震 Zhèn", "䷳ 艮 Gèn", "䷴ 漸 Jiàn", "䷵ 歸妹 Guī Mèi",
    "䷶ 豐 Fēng", "䷷ 旅 Lǚ", "䷸ 巽 Xùn", "䷹ 兌 Duì", "䷺ 渙 Huàn",
    "䷻ 節 Jié", "䷼ 中孚 Zhōng Fú", "䷽ 小過 Xiǎo Guò", "䷾ 既濟 Jì Jì",
    "䷿ 未濟 Wèi Jì"
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
    if advice.endswith("。"):
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
