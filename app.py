from flask import Flask, render_template, redirect, url_for
from flask import request, session, jsonify
from datetime import timedelta

app = Flask(__name__)
app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

user_dict = {'ofir@gmail.com': ['1234', 'Ofir'],
             'morbarz@gmail.com': ['2385', 'Mor'],
             'shirmali@gmail.com': ['3845', 'Shir'],
             'yaelhak@gmail.com': ['6483', 'Yael'],
             'cori@gmail.com': ['0583', 'Coral']}

flowers_dict = {'Rose':['Red, Yellow, White', 'Red Rose: 20, Yellow Rose: 10, White Rose: 20'],
                'Sunflower': ['Yellow', '30'],
                'Tulip': ['Pink, Blue', 'Pink Tulip: 20, Blue Tulip: 15'],
                'Gypsophila': ['White', '30']}


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('homePage.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/assignment3_1')
def assignment3_1():
    bouquets = ['Andy Bouquet', 'Camilla Bouquet', 'White Bloom Bouquet', 'Red Roses Bouquet']
    return render_template('assignment3_1.html', bouquets=bouquets)



@app.route('/assignment3_2', methods=['GET', 'POST'])
def assignment3_2():
    logedin = False
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        if username in user_dict:
            pas_in_dict = user_dict[username][0]
            name_in_dict = user_dict[username][1]
            if pas_in_dict == password and name_in_dict == name:
                session['name'] = name
                session['logedin'] = True
                logedin = True
                return render_template('assignment3_2.html', message='Your already registered, welcome back', name=name)
            else:
                return render_template('assignment3_2.html',
                                       message='This user name is already taken, please try another one :)')

        else:
            user_dict[username] = [password, name]
            session['name'] = name
            session['logedin'] = True
            return render_template('assignment3_2.html',
                                   message='Welcome to our flower shop',
                                   name=user_dict[username][1])


    elif 'flower_type' in request.args:
        flower_type = request.args['flower_type']
        if flower_type is '':
           return render_template('assignment3_2.html', flowers_dict=flowers_dict)
        elif flower_type in flowers_dict:
            return render_template('assignment3_2.html',
                                   flower_type=flower_type,
                                   flower_color=flowers_dict[flower_type][0],
                                   flower_amount=flowers_dict[flower_type][1])
        else:
            return render_template('assignment3_2.html',
                                   message='This flower type is not in stock, try to find another type')
    elif logedin == True:
        return render_template('assignment3_2.html', message='Your already registered, welcome back')
    else:
        return render_template('assignment3_2.html')


@app.route('/endSession')
def logout_func():
    session['logedin'] = False
    logedin = False
    session.clear()
    return redirect(url_for('assignment3_2'))


@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))


if __name__ == '__main__':
    app.run(debug=True)
