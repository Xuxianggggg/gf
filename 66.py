from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# 用于存储分配结果
assignments_db = {}

def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def assign_gifts(names):
    recipients = names[:]
    while True:
        random.shuffle(recipients)
        if all(n != r for n, r in zip(names, recipients)):
            break
    return dict(zip(names, recipients))

@app.route('/create', methods=['POST'])
def create_assignment():
    data = request.json
    names = data.get('names')
    if not names or len(names) != 9:
        return jsonify({'error': '请提交9个名字'}), 400

    assignment = assign_gifts(names)
    unique_id = generate_unique_id()
    assignments_db[unique_id] = assignment

    return jsonify({'link': f'http://localhost:5000/result/{unique_id}'})

@app.route('/result/<unique_id>', methods=['GET'])
def get_result(unique_id):
    assignment = assignments_db.get(unique_id)
    if not assignment:
        return "链接无效或已过期", 404

    result_html = "<h1>🎁 匿名送礼物分配结果 🎁</h1><ul>"
    for giver, receiver in assignment.items():
        result_html += f"<li>{giver} 🎁 {receiver}</li>"
    result_html += "</ul>"
    return result_html

if __name__ == '__main__':
    app.run(debug=True)
