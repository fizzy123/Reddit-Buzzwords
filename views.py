from datetime import datetime, timedelta
from nltk.corpus import stopwords
import pytz, urllib2

from buzzwords.models import Post, Comment
from django.shortcuts import render

def index(request):
    if not request.GET.has_key('end'):
        end = datetime.now(pytz.utc)
    else:
        end = urllib2.unquote(request.GET['end'].decode("utf8"))
        end = datetime.strptime(end, "%d/%m/%y")

    if not request.GET.has_key('start'):
        start = end + timedelta(days=-7);
    else:
        start = urllib2.unquote(request.GET['start'].decode("utf8"))
        start = datetime.strptime(start, "%d/%m/%y")

    stops = stopwords.words('english') + ['']
    score_dict = {}
    for post in Post.objects.all().filter(created_at__range=(start, end)):
        for word in urllib2.unquote(post.title.decode("utf8")).split(' '):
            word = word.replace(',','').replace('\'','').replace('!','').replace('.','').replace('?','')
            if word not in stops:
                if score_dict.has_key(word):
                    score_dict[word] = score_dict[word] + post.score
                else:
                    score_dict[word] = post.score
                    
        for comment in Comment.objects.all().filter(created_at__range=(start, end), post = post):
            for word in urllib2.unquote(comment.text.decode("utf8")).split(' '):
                word = word.replace(',','').replace('\'','').replace('!','').replace('.','').replace('?','')
                if word not in stops:
                    if score_dict.has_key(word):
                        score_dict[word] = score_dict[word] + comment.score
                    else:
                        score_dict[word] = comment.score   
    scores = []
    for key, val in score_dict.iteritems():
        scores.append([key, val])

    return render(request, 'buzzwords/index.html', {'scores':sorted(scores, key=lambda score: score[1], reverse=True)[0:30], 'start':start, 'end':end})
