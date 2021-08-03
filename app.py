from flask import Flask,request,jsonify,render_template
from infer_api import seg_api
from base64 import b64encode
from flask_cors import *
from io import BytesIO
from gevent import pywsgi
from network import check_ipv6

app = Flask(__name__,template_folder="./dist",
            static_folder="./dist/assets")
CORS(app, supports_credentials=True)

@app.route('/', defaults = {'path': ''}, methods=['GET'])
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/api/v1/<datatype>',methods=['POST'])
def api_v1(datatype):
    if datatype == 'file':
        data = request.files.get('file')
        buffered = BytesIO()
        data.save(buffered)
        image_base64 = b64encode(buffered.getvalue()).decode('utf-8')
    elif datatype == 'json':
        data = request.get_json()
        image_base64 = data['image']
    else:
        return jsonify(msg="error")
    result = seg_api(image_base64)
    image_seg_result,image_base64_result,score,GLR = result[0],result[1],result[2],result[3]
    return jsonify(proportion=image_seg_result,image=image_base64_result,score=score,gvr=GLR)

if __name__ == '__main__':
    ipv6_support = check_ipv6()

    if ipv6_support:
        server = pywsgi.WSGIServer(('::', 5000), app) #ipv6
    else:
        server = pywsgi.WSGIServer(('0.0.0.0', 5000), app) #ipv4
    
    print('Run successfully!Please use your browser to access the following ip address:')
    print('---   http://localhost:5000/ ')
    server.serve_forever()