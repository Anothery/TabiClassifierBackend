from classifier import classify_image
from PIL import Image
from color_processor import get_dominant_colors_palette
from flask import  Flask, request, jsonify, Response

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'gif', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def json_response(data, status):
    if(status != 200):
        return jsonify(error = data), status
    else:
        return jsonify(data), status


@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
            return json_response('No file part', 400)

    file = request.files['file']

    if file.filename == '':
        return json_response('No selected file', 400)

    if file:
        if not allowed_file(file.filename):
            return json_response('File extension is not allowed', 400)
        else:
            try:
                pil_image = Image.open(file.stream)
                return json_response({ 'predictions' : classify_image(pil_image),
                                       'colors': get_dominant_colors_palette(Image.open(file.stream))}, 200)
            except Exception as ex:
                return json_response(str(ex), 422)


@app.route('/')
def root():
    return jsonify('The world is beautiful')

        
if __name__ == "__main__":
    app.run()


