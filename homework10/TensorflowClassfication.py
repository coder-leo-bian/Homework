import tensorflow as tf
import numpy as np
import pandas as pd
import jieba
import gensim


comments = pd.read_csv('../../datasource/movie_comments.csv')
data, target = [], []


def stopword(sentence):
    with open("../../datasource/chinese_stopwords.txt", 'r') as f:
        stopwords = [line.replace('\n', '') for line in f.readlines() if line != '\n']
    return [sen for sen in sentence if sen not in stopwords]


def reformat():
    global data, target
    for i, comm in enumerate(comments.values):
        try:
            cm = stopword(jieba.lcut(comm[3]))
            star = int(comm[4])
            if cm and len(cm) > 3 and star in [1, 2, 3, 4, 5]:
                with open('data.txt', 'a') as fw:
                    fw.write(' '.join(cm) + '\n')
                with open('target.txt', 'a') as fw:
                    fw.write(str(1 if star > 2 else 0) + '\n')
                # target.append(1 if star > 2 else 0)
        except Exception as e:
            print(e)
            continue
        if i%100000 == 0:
            print(i, comm)

reformat()

with open('data.txt', 'r') as f:
    print(len(f.readlines()))

with open('target.txt', 'r') as f:
    print(len(f.readlines()))

sentences = gensim.models.word2vec.LineSentence(source='data.txt')

model = gensim.models.Word2Vec(sentences=sentences, size=100, min_count=1)
model.save('word2vec.model')


