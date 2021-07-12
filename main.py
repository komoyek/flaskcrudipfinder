import ipapi
from flask import Flask, request, render_template

#pip install ipapi


app = Flask(__name__)



@app.route('/', methods = ['GET', 'POST'])
def Index():
    return render_template('index.html')

@app.route('/search', methods = ['GET', 'POST'])
def Search():
    return render_template('search.html')

@app.route('/result', methods = ['GET', 'POST'])
def result():
    search = request.form.get('search')
    data = ipapi.location(ip=search, output='json')
    return render_template('result.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)