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
        login_ = request.form["login"]
        password = request.form["password"]
        user = User.query.filter_by(login=login_, password=password).first()
        if user is not None:
            user_token=jwt.encode({"login": login_, "password": password}, app.config['SECRET_KEY'], algorithm="HS256")
            user.token = user_token
            db.session.add(user)
            db.session.commit()
            return  redirect("/coin")
        else:
            return f"<h1>Could not found a user with login: {login_}</h1>"
   
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

    result_list = []
    while True:
        url_api = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10&sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false'
        response = requests.get(url=url_api)
        data = response.json()
        for i in range(0, 10):
            result_list.append({
                'id': data['data']['cryptoCurrencyList'][i]['id'],
                'name': data['data']['cryptoCurrencyList'][i]['name'],

            })
        
        
        coin_id = 0
        for i in range(len(result_list)):
            if result_list[i]['name'] == coin_name.lower().title():
                coin_id = result_list[i]['id']
        urls = f'https://api.coinmarketcap.com/content/v3/news?coins={coin_id}'
        res = requests.get(url=urls)
        data_news = res.json()
        data_news_json = []
        for i in range(0, len(data_news['data'])):
            data_news_json.append({
                'Title': data_news['data'][i]['meta']['title'],
                'Paragraph': data_news['data'][i]['meta']['subtitle']
            })
        return data_news_json

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

        exists=False
        
        for row in db.session.query(News).filter_by(coin_name=coinName):
            if row.coin_name == coinName:
                exists=True

        for i in range(0, len(result) - 1):
            title.append(result[i]['Title'])
            parag.append(result[i]['Paragraph'])
            
            # for summ in summarizer(result[i]['Title'],max_length=120,min_length=30,do_sample=False):
            #     sum_title.append(summ['summary_text'])
            for summ in summarizer(result[i]['Paragraph'],max_length=120,min_length=30,do_sample=False):
                sum_parag.append(summ['summary_text'])
            
            if not exists:
                news_n = News(f'{coinName}', f'{title[i]}', f'{parag[i]}')
                db.session.add(news_n)
                db.session.commit()
        
        #print(sum_title)

    return render_template('coin.html', form=form, title=title, parag=sum_parag)






if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()