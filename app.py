from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from image_match import is_similar
from models import init_db, insert_item, get_items
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.route('/')
def index():
    return render_template('post.html')

@app.route('/post', methods=['POST'])
def post_item():
    item_type = request.form['type']
    title = request.form['title']
    desc = request.form['desc']
    img = request.files['image']

    unique_name = f"{uuid.uuid4().hex}_{secure_filename(img.filename)}"
    path = os.path.join(UPLOAD_FOLDER, unique_name)
    img.save(path)

    matched = None
    existing = get_items('found' if item_type == 'lost' else 'lost')
    for item in existing:
        if is_similar(item[4], path):
            matched = item
            break

    insert_item(item_type, title, desc, path)

    if matched:
        return render_template('match.html', item={
            'title': matched[2],
            'desc': matched[3],
            'image': matched[4]
        })

    return redirect('/')

@app.route('/view/<item_type>')
def view_items(item_type):
    items = get_items(item_type)
    return render_template('list.html', items=items, type=item_type)

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
