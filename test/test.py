from flask import Flask, render_template, redirect 
from flask import request
from flask.json import jsonify
import jwt
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from bs4 import BeautifulSoup
from urllib.request import urlopen
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import requests
from transformers import pipeline




app = Flask(__name__,template_folder="my_templates")
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567@localhost:5432/coin'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user_n'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(120), unique=True, nullable=False)


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String(20), nullable=False)
    title = db.Column(db.Text, nullable=False)
    paragraph = db.Column(db.Text, nullable=False)

    def __init__(self, coin_name, title, paragraph):
        self.coin_name = coin_name
        self.title= title
        self.paragraph = paragraph



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        user = User.query.filter_by(login=login, password=password).first()
        if user is not None:
            user_token=jwt.encode({"login": login, "password": password}, app.config['SECRET_KEY'], algorithm="HS256")
            user.token = user_token
            db.session.add(user)
            db.session.commit()
            return  redirect("/coin")
        else:
            return f"<h1>Could not found a user with login: {login}</h1>"
   
    return render_template("login.html")


@app.route("/protected",methods=["GET"])
def protected():
    s_token=request.args.get("token")
    jwt_token=jwt.decode(s_token,app.config['SECRET_KEY'],algorithms=["HS256"])
    if jwt_token:
        login_ = jwt_token.get("login")
        password = jwt_token.get("password")
        user = User.query.filter_by(login=login_, password=password).first()
        if user is not None:
            return "<h1>Hello, token which is provided is correct </h1>"
    return "<h1>Hello, Could not verify the token</h1>"





def dataToCoin( coin_name):
    for i in range(len(coin_name)):
        if coin_name[i] == ' ' or coin_name[i] == '.':
            coin_name = coin_name.replace(' ', '-')

    my_list = []
    while True:
        api = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10&sortBy=market_cap&sortType=desc&convert=EUR&cryptoType=all'
        sending = requests.get(url=api)
        
        
        data = sending.json()
        
        
        for i in range(0, 10):
            my_list.append({
                'id': data['data']['cryptoList'][i]['id'],
                'name': data['data']['cryptoList'][i]['name'],

            })
        
        
        cur_id = 0
        
        
        for i in range(len(my_list)):
            if my_list[i]['name'] == coin_name.lower().title():
                cur_id = my_list[i]['id']
        cur_url = f'https://api.coinmarketcap.com/content/v3/news?coins={cur_id}'
        responding = requests.get(url=cur_url)
        formatNews = responding.json()
        json_format = []
        
        
        for i in range(0, len(formatNews['data'])):
            json_format.append({
                'Title': formatNews['data'][i]['meta']['title'],
                'Paragraph': formatNews['data'][i]['meta']['subtitle']
            })
        return json_format 

class CoinForm(FlaskForm):
    coin_name = StringField('Coin')
    submit = SubmitField('Submit')

@app.route("/coin", methods=["GET", "POST"])
def coin():

    form = CoinForm()
    summarizer = pipeline("summarization")

    title = []
    parag = []
    sum_title = []
    sum_parag = []

    if form.validate_on_submit():
        coinName = (str(form.coin_name.data)).lower()
        
        result = dataToCoin(coinName)

        ifIn=False
        
        for row in db.session.query(News).filter_by(coin_name=coinName):
            if row.coin_name == coinName:
                ifIn=True

        for i in range(0, len(result) - 1):
            title.append(result[i]['Title'])
            parag.append(result[i]['Paragraph'])
            
            # for summ in summarizer(result[i]['Title'],max_length=120,min_length=30,do_sample=False):
            #     sum_title.append(summ['summary_text'])
            for summ in summarizer(result[i]['Paragraph'],max_length=120,min_length=30,do_sample=False):
                sum_parag.append(summ['summary_text'])
            
            if not ifIn:
                news_n = News(f'{coinName}', f'{title[i]}', f'{parag[i]}')
                db.session.add(news_n)
                db.session.commit()
        
        #print(sum_title)

    return render_template('cur.html', form=form, title=title, parag=sum_parag)






if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()
