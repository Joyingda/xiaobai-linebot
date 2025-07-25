from flask import Flask, request

app = Flask(__name__)

@app.route('/callback', methods=['POST'])
def callback():
    print('📨 收到 LINE Event：', request.json)
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
