from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    title = ['Resume', '']
    return render_template('home.html', title=title)

@app.route('/cv')
def cv():
    title = ['Resume', '']
    return render_template('cv.html', title=title)


@app.route('/login')
def login():
    title = ['Login', '']
    return render_template('login.html', title=title)


@app.route('/register')
def register():
    title = ['Register', '']
    return render_template('register.html', title=title)

@app.route('/logout')
def logout():
    title = ['logout', '']
    return render_template('logout.html', title=title)


@app.route('/dashboard')
def dashboard():
    title = ['Dashboard', '']
    return render_template('dashboard.html', title=title)



if __name__ == "__main__":
    app.run(debug=True)