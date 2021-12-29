import tornado
import tornado.ioloop
import tornado.web
import pymongo
import datetime
import os.path

# serverURL = '119.45.163.114'
# user = 'james'
# password = 'IYT7i6rfTR&%R*&'
# localport = '127.0.0.1'

client = pymongo.MongoClient("mongodb://james:IYT7i6rfTR&%25R*&@119.45.163.114:27017/TweetScraper")

db = client['TweetScraper']
collection = db['tweetday']

# print(collection.find_one())

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        _id = []
        created_at = []
        text = []
        favorites = []
        retweets = []
        username = []
        url = []

        limit = 500

        for tweet in collection.find():
            _id.append(tweet['_id'])
            d = datetime.datetime.fromisoformat(tweet['created_at'].replace("Z",""))
            created_at.append(d.strftime("%B-%d-%Y // %I:%M:%S %p"))
            text.append(tweet['text'] + "")
            favorites.append(tweet['like_count'])
            retweets.append(tweet['retweet_cou'])
            url.append(tweet['url'])
            if len(_id) == limit: break

        self.render("index.html", _id = _id, created_at = created_at, text = text, retweets = retweets, favorites = favorites, url = url, limit = limit)    

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler)
        ]

        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "static")
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    application = Application()
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
