 from flask import Flask, render_template, request, redirect
import os
from image_match import is_similar
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
posts = []

@app.route('/')
def index():
    return render_template('post.html')

@app.route('/post', methods=['POST'])
def post_item():
    item_type = request.form['type']
    title = request.form['title']
    desc = request.form['desc']
    img = request.files['image']
    filename = secure_filename(img.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    img.save(path)

    post = {'type': item_type, 'title': title, 'desc': desc, 'image': path}
    matched = None

    if item_type == 'lost':
        for p in posts:
            if p['type'] == 'found' and is_similar(p['image'], path):
                matched = p
                break
    elif item_type == 'found':
        for p in posts:
            if p['type'] == 'lost' and is_similar(p['image'], path):
                matched = p
                break

    posts.append(post)
    if matched:
        return render_template('match.html', item=matched)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)