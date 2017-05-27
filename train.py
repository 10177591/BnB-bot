#
#
# Nokia Copyright...
############################################################

import pandas as pd
import numpy as np
import math
import re
from utils.log2_df import DFCreator
from utils.read_config import ConfigLoader
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from gensim import corpora, models, similarities

def feature_wcount(token, input_df):
    if token == 'wcount':
        count_df = input_df.applymap(wordcount)
    elif token == 'expcount':
        count_df = input_df.applymap(expcount)
    elif token == 'dbgcount':
        count_df = input_df.applymap(dbgcount)
    return count_df

def wordcount (log):
    matched = re.findall(r'(\w+)',log)
    return len(matched)

def expcount (log):
    matched = re.findall(r'exception|error|failure|warning',log,re.IGNORECASE)
    return len(matched)

def dbgcount (log):
    matched = re.findall(r'debug|info',log,re.IGNORECASE)
    return len(matched)


def apply_cv_nb(input_df, label_s):
    '''
    This function will use  Naive Bayes with Count vectorizer
    '''
    from sklearn import metrics
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.cross_validation import train_test_split

    nd_df = input_df.applymap(keepstring)
    X = nd_df
    y = label_s
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    
    vect = CountVectorizer()

    X_train_dtm = vect.fit_transform(X_train)
    X_test_dtm = vect.fit_transform(X_test)

    nb = MultinomialNB()
    nb.fit(X_train_dtm, y_train)
    y_pred_class = nb.predict(X_test_dtm)
    metrics.accuracy_score(y_test, y_pred_class)

def keep_nwords(log):
    e_sw = stopwords.words('english')
    texts = [word for word in word_tokenize(log.lower().decode('utf-8')) if word not in e_sw]
    items = texts[0:500]
    log_begin = ' '.join(map(str, items))
    return log_begin

def keep_impwords(log):
    e_sw = stopwords.words('english')
    texts = [word for word in word_tokenize(log.lower().decode('utf-8')) if word not in e_sw]
    texts = [impword(word) for word in texts if not hasNumbers(word)]
    items = texts[0:]
    log_imp = ''.join(map(str, items))
    return log_imp

def keep_alpha(log):
    e_sw = stopwords.words('english')
    texts = [word for word in word_tokenize(log.lower().decode('utf-8')) if word not in e_sw]
    texts = [word for word in texts if not hasNumbers(word)]
    items = texts[0:]
    log_imp = ' '.join(map(str, items))
    return log_imp

def hasNumbers(str):
    return any(c.isdigit() for c in str)

impwords = ['ProxyDiaConnection','debug']
def impword(w):
    if w in impwords:
        return w+' '
    else:
        return ''

'''
Load the configurations
'''
loader = ConfigLoader()
config = loader.load_config('./config/product_config.json')

'''
Read the logs and convert them into dataframe
'''
df_creator = DFCreator()
case_list = df_creator.get_file_list(config.get_dstdir())
input_df = df_creator.log2_dataframe(case_list, config.get_processlist())

# Replace the NaN with 'empty'
input_df[input_df.isnull()] = 'empty'

wcount_df = feature_wcount('wcount', input_df)
expcount_df = feature_wcount('expcount', input_df)
dbgcount_df = feature_wcount('dbgcount', input_df)
expcount_df = feature_wcount('expcount', input_df)
print wcount_df.head(4)
#print expcount_df
#print dbgcount_df
input_df.applymap(keep_alpha)
