from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_data = None
    if request.method == 'POST':
        user_data = {
            'name': request.form['name'],
            'city': request.form['city'],
            'hobby': request.form['hobby'],
            'age': request.form['age']
        }
    return render_template('index.html', user_data=user_data)

if __name__ == '__main__':
    app.run(debug=True)
