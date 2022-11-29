import flask
from flask import Flask
from flask import request
from flask.globals import g

import mysql.connector as MySQLConnector

#  inicialização do banco de dados
#  adicionamos o handle do conector no contexto do
#  app do flask.
def init_db():
    g.db = MySQLConnector.connect(
        host = "localhost",
        user = "root",
        password = "alunoaluno",
        database = "bentivi"
    )
    return g.db

# Recupera o handle do banco de dados
def get_db():
    if "db" not in g:
        g.db = init_db()
    
    return g.db

# Inicialização da aplicação flask
def init_app():
    app = flask.Flask(__name__)

    with app.app_context():
        init_db()

    return app

app = init_app()

#  Fechamos a conexão com o banco de dados
#  quando a aplicação se encerra.
@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@app.route("/")
def index():
    db = get_db()

    return "Is connected? %s" % ("Yes" if db.is_connected else "No")
#1
@app.route("/user/tweets/<user_id>")
def allTweetFromUser(user_id):
    db = get_db()
    c = db.cursor()
    c.execute(f"""
        select id, content
        from tweet
        where owner in (
            select id
            from user    
            where id = {user_id}
        )
    """)
    return c.fetchall()
#2
@app.route("/user/<user_id>", methods = ["GET"])
def allTweetFollows(user_id):
    db = get_db()
    c = db.cursor()
    c.execute(f"""
    select id 
    from tweet 
    where owner in (
        select id
        from user as u
        where id in (
            select user_follows_id
            from user_follows
            where user_followed = {user_id}
        )
    )
    """)
    return c.fetchall()
#3
@app.route("/user/follows/<user_id>", methods = ["GET"])
def allFollowsUsers(user_id):
    db = get_db()
    c = db.cursor()
    c.execute(f"""
    select nickname, id
    from user as u
    where id in (
        select user_follows_id
        from user_follows
        where user_followed_id = {user_id}
    )
    """)
    return c.fetchall()
#4
@app.route("/user/followed/<user_id>", methods = ["GET"])
def allfolleweduser(user_id):
    db = get_db()
    c = db.cursor()
    c.execute(f"""
    select nickname
    from user as u 
    where id in (
        select user_followed_id
        from user_follows
        where user_followed_id = {user_id}
    )
    """)
#5
@app.route("/tweet/parent/<user_id>", methods= ["GET"])
def tweetRetweet(tweet_id):
    db = get_db()
    c = db.cursor()
    c.execute(f"""
    select id
    from tweet as t
    where id (
        select parent 
        from tweet
        where id = {tweet_id}
    )
    """)
#6
@app.route("/tweet/text/<text>", methods = ["GET"])
def tweetText(text):
    db = get_db()
    c = db.cursor()
    c.execute(f"""
    select content
    from tweet 
    where content = {text}
    """)
#7
@app.route("/user/register", methods =["POST"])
def createUser():    
    db = get_db()
    c = db.cursor()
    user = []
    userData = request.form
    userID = userData["id"]
    userNickname = userData["nickname"]
    userEmail = userData["email"]
    userPassword = userData["password"]
    turfe = (userID, userNickname, userEmail, userPassword)
    user.append(turfe)
    sql = "insert into user values(%s, %s, %s, %s)"
    c.executemany(sql, user)
    db.commit()    
    return "Sucesso"

@app.route("/tweet/insert", methods = ["POST"])
def createTweet():
    db = get_db()
    c = db.cursor()
    tweet = []
    tdata = request.form
    tId = tdata["id"]
    tContent = tdata["content"]
    tRetweet = tdata["retweet"]
    tOwner = tdata["owner"]
    tParent = tdata["parent"]    if "parent" in tdata else None
    turfe = (tId, tContent, tRetweet, tOwner, tParent)
    tweet.append(turfe)
    sql = "insert into tweet values (%s, %s, %s, %s, %s)"
    c.executemany(sql, tweet)  
    db.commit()
    return "Tweet Inserido!"    

@app.route("/user/follows/", methods = ["POST"])
def userAddFollowers():
    db = get_db()
    c = db.cursor()
    follow = []
    fdata = request.form
    userFollowsId = fdata["user_follows_id"]
    userfOllowedId = fdata["user_followed_id"]
    turfe = (userFollowsId, userfOllowedId)
    follow.append(turfe)
    sql = "insert into user_follows values(%s, %s)"
    c.executemany(sql, follow)
    db.commit()
    return "Seguido"
