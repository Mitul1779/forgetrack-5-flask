from flask import Flask, render_template, request, redirect, jsonify, abort
import random
import string

def url_code_generator(length=6):
    chars = string.ascii_letters + string.digits
    chars = ''.join(random.choice(chars) for _ in range(length))
    if chars in urls:
        return url_code_generator(length)
    return chars

app = Flask(__name__)

urls = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', "").strip()
        if not url:
            return render_template('index.html', error="Please enter a valid URL.")
        print(f"Received URL: {url}")
        for code, info in urls.items():
            if info["url"] == url:
                print(f"URL already exists: {url}")
                print(f"URL code: {code}")
                return render_template('index.html', message="This URL has already been submitted.", url_code=code)
        url_code = url_code_generator()
        urls[url_code] = {
            "url": url,
            "clicks": 0
        }
        return render_template('index.html', url=url, url_code=url_code)
    
    return render_template('index.html')
    
@app.route('/<code>')
def redirect_url(code):
    if code in urls:
        url_info = urls[code]
        url_info["clicks"] += 1
        return redirect(url_info["url"])
    abort(404, description="URL code not found.")

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', urls=urls)

@app.route('/api/links')
def api_links():
    return jsonify(urls)



if __name__ == '__main__':
    app.run(debug=True)