import requests
from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask import request
import mysql.connector

assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         template_folder='templates')

@assignment_4.route('/assignment4')
def assignment4_func():
    query = 'select * from users'
    user_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=user_list)


@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    query = 'select * from users'
    users = interact_db(query, query_type='fetch')
    for user in users:
        if email == user.email:
            return render_template('assignment4.html', message1='This user is already exist, please try again.', users=users)

    if name == ' ':
        return render_template('assignment4.html', message1='Please fill all fields', users=users)
    else:
        query = "INSERT INTO users(name, email, password) VALUES ('%s', '%s', '%s')" % (name, email, password)
        interact_db(query=query, query_type='commit')
        query1 = 'select * from users'
        users1 = interact_db(query1, query_type='fetch')
        return render_template('assignment4.html', message2='Welcome to our website, ', user=name, users=users1)


@assignment_4.route('/update_user', methods=['POST'])
def update_user():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    query = 'select * from users'
    users = interact_db(query, query_type='fetch')
    for user in users:
        if email == user.email:
           if name == '' and password != '':
                query = "UPDATE users SET password='%s' WHERE email = '%s'" % (password, email)
                interact_db(query=query, query_type='commit')
                query1 = 'select * from users'
                users1 = interact_db(query1, query_type='fetch')
                return render_template('assignment4.html', message3='Your profile has been updated, ', user=name, users=users1)
           elif password == '' and name != '':
                query = "UPDATE users SET name='%s' WHERE email = '%s'" % (name, email)
                interact_db(query=query, query_type='commit')
                query1 = 'select * from users'
                users1 = interact_db(query1, query_type='fetch')
                return render_template('assignment4.html', message3='Your profile has been updated, ', user=name,users=users1)
           elif password != '' and name != '':
               query = "UPDATE users SET name='%s', password='%s' WHERE email = '%s'" % (name, password, email)
               interact_db(query=query, query_type='commit')
               query1 = 'select * from users'
               users1 = interact_db(query1, query_type='fetch')
               return render_template('assignment4.html', message3='Your profile has been updated, ', user=name,
                                      users=users1)
           else:
                return render_template('assignment4.html', message3='There is nothing to update', user=name, users=users)

    return render_template('assignment4.html', message3='User is not in database, please sign up first.', users=users)


@assignment_4.route('/delete_user', methods=['POST'])
def delete_user():
    email = request.form['email']
    password = request.form['password']
    query = 'select * from users'
    users = interact_db(query, query_type='fetch')
    for user in users:
        if email == user.email:
            if int(password) == user.password:
                query = "DELETE FROM users WHERE email='%s'" % email
                interact_db(query, query_type='commit')
                query1 = 'select * from users'
                users1 = interact_db(query1, query_type='fetch')
                return render_template('assignment4.html',
                                       message4='User was deleted, thank you for being part of Bloom family.', users=users1)
            else:
                return render_template('assignment4.html',
                                   message4='Password or email was not correct, please try again', users=users)
    return render_template('assignment4.html',
                           message4='User does not exist in database, there is no one to delete.', users=users)


@assignment_4.route('/assignment_4/users')
def users_response():
    query = 'select * from users'
    list = interact_db(query, query_type='fetch')
    return jsonify(list)



@assignment_4.route('/outer_source')
def outer_source_frontend():
    return render_template('outer_source.html')


@assignment_4.route('/outer_source/backend')
def outer_source_backend():
    userID = request.args['userID']
    res = requests.get(f"https://reqres.in/api/users/{userID}")
    return render_template('outer_source.html', request_data=res.json()['data'])


@assignment_4.route('/assignment4/restapi_users/', defaults={'user_id': -1})
@assignment_4.route('/assignment4/restapi_users/<user_id>')
def get_user(user_id):
    if user_id == -1:
        query = f'SELECT * FROM users'
        users_list = interact_db(query, query_type='fetch')
        return_list = []
        for user in users_list:
            user_dict = {
                'name': user.name,
                'email': user.email
            }
            return_list.append(user_dict)
        return jsonify(return_list)

    else:
        query = f'SELECT * FROM users WHERE id={user_id}'
        users_list = interact_db(query, query_type='fetch')
        if len(users_list) == 0:
            return_dict = {
                'message': 'user was not found, try again.'
            }
        else:
            user = users_list[0]
            return_dict = {
                'name': user.name,
                'email': user.email
            }
    return jsonify(return_dict)




def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='assignment_4')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value
