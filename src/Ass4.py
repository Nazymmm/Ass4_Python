from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from selenium import webdriver
PATH = "/web-drivers/chromedriver"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismysecretkey'

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:satbaevna03*@localhost/PythonNew"
db = SQLAlchemy(app)

class News(db.Model):
    __tablename_ = 'news'
    id = db.Column('id', db.Integer, primary_key = True)
    coin_name = db.Column('coin_name', db.String(100))
    news = db.Column('news' ,db.String(1000000))

    def __init__(self, coin_name, news):
        self.coin_name = coin_name
        self.news = news

@app.route('/coin', methods = ['GET', 'POST'])
def coin():
    if request.method == 'POST':
        coin = request.form.get('coin')
        coin.lower
        url = 'https://coinmarketcap.com/currencies/'+ coin.lower() + '/news/'
        driver = webdriver.Chrome(PATH)
        driver.get(url)
        page = driver.page_source
        page_soup = BeautifulSoup(page, 'html.parser')
        containers = page_soup.find_all("a", {"class":"svowul-0 jMBbOf cmc-link"})
        das = ''
        for news in containers:
            das += '<p>' + news.find('p').text + '</p>'
        new_par = News(coin, das)
        db.session.add(new_par)
        db.session.commit()
        return '''
                  <p>The coin news: ''' + new_par.news + '''</p>'''
    return '''
           <form method="POST">
               <div><label>Coin: <input type="text" name="coin"></label></div>
               <input type="submit" value="Submit">
           </form>'''
    
if __name__ == '__main__':
    app.run(debug=True)