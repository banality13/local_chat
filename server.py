from flask import Flask, render_template, request, abort, redirect, url_for

app = Flask(__name__)

FILENAME='messages.txt'

usernames=["ilan", "blanca", "theo"]

def return_messages(): 
    messages=[]
    file_object = open(FILENAME, 'r')
    for line in file_object: 
        messages.append(line)
    file_object.close()
    return messages

def add_message_to_file(newmessage): 
    file_object = open(FILENAME, 'a')
    file_object.write(newmessage)
    file_object.write('\n')
    file_object.close()

@app.route("/", methods=['post', 'get'])
def hello(): 
    name="_"
    if request.method=='POST' : 
        name = request.form.get("username")
        res = redirect(url_for('chatroom'))
        res.set_cookie('name', name)
        return res
    if request.method=='GET' : 
        return render_template('index.html', name="")
    else : 
        return render_template('index.html', name="error")

@app.route('/chatroom', methods=['post', 'get'])
def chatroom(): 
    name = request.cookies.get('name')
    if request.method=="GET" : 
        return render_template('chatroom.html', name=name, messages=return_messages())
    if request.method=="POST":
        newmessage= request.form.get("newmessage")
        add_message_to_file(name + ": "+ newmessage)
        return render_template('chatroom.html', name=name,messages=return_messages())
        
    else : 
        return render_template('chatroom.html', messages="error")

