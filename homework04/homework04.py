import jieba
import gensim
import logging
import time
from functools import wraps
import os
import re
import pickle
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib
from opencc import OpenCC



# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
# rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/Logs/'
# log_name = log_path + rq + '.log'
# logfile = log_name
# fh = logging.FileHandler(logfile, mode='w')
fh = logging.FileHandler('word2vec.log', mode='w')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
# 日志
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')


def stopwords(line):
    # 处理停止词
    with open(STOP_WORD, 'r') as fr:
        words = fr.read()
    res = [x for x in line if x not in words]
    return res


def decorator(func):
    @wraps(func)
    def wrap():
        start_time = time.time()
        logger.info('进入{}函数，开始时间：{}'.format(func.__name__, start_time))
        func()
        logger.info('{}函数执行结束，总用时时间：{}'.format(func.__name__ ,str(time.time() - start_time)))
        logger.info('*'*50 + '分割线' + '*'*50)
    return wrap


@decorator
def cut_word():
    cc = OpenCC('hk2s')
    for file_name in os.listdir(CORPUS):
        res = re.search('^\.', file_name)
        if file_name == 'cut_result':
            break
        if file_name not in  ['.DS_Store', 'cut_result', 'cut_result_bak'] and not res:
            with open(CORPUS+file_name, 'r') as fr:
                rds = fr.readlines()
                logger.info('当前文件行数: {}'.format(len(rds)))
                with open(CUT_RESULT, 'a') as fw:
                    for r in rds:
                        re_filter = re.findall('<doc id=.*>|</doc>', r)
                        if not re_filter:
                            clean_word = ' '.join(stopwords(jieba.lcut(cc.convert(r))))
                            if clean_word:
                                fw.write(clean_word)
                        else:
                            logger.info('过滤字符: {}'.format(re_filter[0]))


@decorator
def train_model():
    sentences = gensim.models.word2vec.LineSentence(CUT_RESULT)
    model = gensim.models.word2vec.Word2Vec(sentences, size=100, hs=1, min_count=200, window=3)
    model.save(MODEL_OBJECT)
    try:
        sim1 = model.similarity('初等数学', '代数')
    except KeyError:
        sim1 = 0
    print(sim1)


@decorator
def predict_model():
    model = gensim.models.Word2Vec.load(MODEL_OBJECT)
    try:
        sim1 = model.similarity('爱情', '友情')
        sim2 = model.most_similar(['世界杯'])

    except KeyError:
        sim1 = 0
    print(sim1)
    print(sim2)
    print(model['世界杯'])


def main(flag):
    cut_word()
    if flag == '1':
        if 'model_object' not in os.listdir('../static/'):
            train_model()
    else:
        if 'cut_result_bak' not in os.listdir('../../wikiex/'):
            train_model()
    # predict_model()


def tsne_plot(model):
    labels = []
    tokens = []
    print(model['民族'])
    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []

    for value in new_values:

        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


if __name__ == '__main__':
    flag = input('本地输入0，服务器输入1, 其他值仅仅获取训练结果做图形可视化---> ：')
    if flag == '1':
        STOP_WORD = '../static/stopwords'
        CORPUS = '../corpus/'
        CUT_RESULT = '../static/cut_result'
        MODEL_OBJECT = '../static/model_object'
        main(flag)
    elif flag == '0':
        STOP_WORD = 'stopwords'
        CORPUS = '../../wikiex/'
        CUT_RESULT = '../../wikiex/cut_result'
        MODEL_OBJECT = '../../wikiex/cut_result_bak'
        main(flag)
        model = gensim.models.Word2Vec.load(MODEL_OBJECT)
        tsne_plot(model)
    elif flag=='2':
        MODEL_OBJECT = '../../wikiex/cut_result_bak'
        predict_model()
    else:
        MODEL_OBJECT = '../../wikiex/cut_result_bak'
        model = gensim.models.Word2Vec.load(MODEL_OBJECT)
        tsne_plot(model)
