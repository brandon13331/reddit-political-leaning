import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import praw
import re

SCORE_THRESHOLD = 10
OUT_CSV = 'output.csv'

comment_index = 0

comments = []
word_pattern = re.compile('[^\s\w|_]+', re.UNICODE)
right_feature_words = ['wall', 'build', 'iran', 'america', 'trump',
        'drain', 'swamp', 'cuck', 'witch', 'hunt', 'locked']
left_feature_words = ['capitalist', 'capitalism', 'anticapitalism', 
        'syndicalist', 'bourgeoisie', 'proletariat', 'marx', 'marxist',
        'ml']
feature_words = [''] + left_feature_words + right_feature_words;

def get_comments():
    for submission in r.subreddit('the_donald').hot(limit=1):
        submission.comments.replace_more(limit=None)
        for top_level_comment in submission.comments:
            if top_level_comment.score >= SCORE_THRESHOLD:
                comments.append(top_level_comment.body)

def remove_stopwords():
    stop_words = set(stopwords.words('english'))
    for comment in comments:
        comment = word_pattern.sub('', str(comment))
        comment = comment.lower()
        word_tokens = word_tokenize(comment)
        filtered_sentence = [w for w in word_tokens if not w in stop_words] 
        word_freq = [filtered_sentence.count(w) for w in feature_words]
        write_frequency_count(word_freq)

# writes frequency counts to the csv file
def write_frequency_count(word_freq):
    global comment_index
    word_freq.pop(0)
    word_freq.insert(0, comment_index)
    comment_index += 1
    with open(OUT_CSV, mode='a') as output:
        output_writer = csv.writer(output, delimiter=',',
                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(word_freq)
    

def write_csv_headers():
    with open(OUT_CSV, mode='w') as output:
        output_writer = csv.writer(output, delimiter=',',
                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(feature_words)
    

if __name__ == "__main__":
    write_csv_headers()
    user_agent = "Data scraper 1.0 for hackathon project"
    r = praw.Reddit(user_agent=user_agent,
                    client_id='',
                    client_secret='',
                    username='',
                    password=''
                    )
    get_comments()
    remove_stopwords()
