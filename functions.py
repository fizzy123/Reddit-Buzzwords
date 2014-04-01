import json, urllib2, os, time

from buzzwords.models import Post, Comment

def update_database():
    hdr = { 'User-Agent' : 'Gif Grabber by /u/fizzzzzzzzzzzy' }
    req = urllib2.Request("http://www.reddit.com/r/all/top.json?t=day", headers=hdr)
    posts_json = json.load(urllib2.urlopen(req))
    for post_json in posts_json['data']['children']:
        post = Post(title=urllib2.quote(post_json['data']['title'].lower().encode("utf8")), score=post_json['data']['score']) 
        post.save()
        req = urllib2.Request("http://www.reddit.com" + post_json['data']['permalink'][:-1]+".json", headers=hdr)
        comments_json = None
        while not comments_json:
            try:
                comments_json = json.load(urllib2.urlopen(req))
            except urllib2.HttpError, e:
                print e
                time.sleep(30)
        for comment in comments_json[1]['data']['children']:
            if (comment['data'].has_key('body')):
                comment = Comment(text=urllib2.quote(comment['data']['body'].lower().encode("utf8")), post = post, score=int(comment['data']['ups'])-int(comment['data']['downs']));
                comment.save()
