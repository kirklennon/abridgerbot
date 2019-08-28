from twython import Twython
import sqlite3

# Add developer tokens below
twitter = Twython("", "",
                  "", "")
# Edit accounts to follow below
accounts = ['kirklennon', 'voxdotcom', 'qz']

conn = sqlite3.connect('abridger.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Twitter (url TEXT)')

def abridger(account):
    user_tweets = twitter.get_user_timeline(screen_name=account,
                                        include_rts=False)
    for tweet in user_tweets:
        try: 
            url = tweet['entities']['urls'][0]['expanded_url']
        except:
            continue
        cur.execute('SELECT url FROM Twitter WHERE url = ? LIMIT 1', (url, ))
        foundurl = cur.fetchone()
        if foundurl is None:
            cur.execute('INSERT INTO Twitter (url) VALUES (?)', (url, ))
            conn.commit()
            print('Added', url)
            twitter.retweet(id=tweet['id_str'])

for account in accounts:
    abridger(account)
cur.close()
