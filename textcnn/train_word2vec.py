#encoding:utf-8
import logging
import time
import codecs
import sys
import re
import jieba
from gensim.models import word2vec
from textcnn.text_model import TextConfig


re_han= re.compile(u"([\u4E00-\u9FD5a-zA-Z]+)") # 用标点符号来切割文本你的方法

class Get_Sentences(object):
    '''

    Args:
         filenames: a list of train_filename,test_filename,val_filename
    Yield:
        word:a list of word cut by jieba

    '''

    def __init__(self,filenames):
        self.filenames= filenames

    def __iter__(self):
        for filename in self.filenames:
            with codecs.open(filename, 'r', encoding='utf-8') as f:
                for _,line in enumerate(f):
                    try:
                        line=line.strip()
                        line=line.split('\t')
                        assert len(line)==2
                        blocks=re_han.split(line[1])
                        word=[]
                        for blk in blocks:
                            if re_han.match(blk):
                                word.extend(jieba.lcut(blk))
                        yield word
                    except:
                        pass

def train_word2vec(filenames):
    '''
    use word2vec train word vector
    argv:
        filenames: a list of train_filename,test_filename,val_filename
    return: 
        save word vector to config.vector_word_filename

    '''
    t1 = time.time()
    sentences = Get_Sentences(filenames)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = word2vec.Word2Vec(sentences, size=100, window=5, min_count=1, workers=6)
    #sentences：可以是一个list，对于大语料集，建议使用BrownCorpus,Text8Corpus或lineSentence构建。
    #corpora: 待处理的文本集 workers: 训练模型的线程数
    #size: 特征向量的维度
    #min_count: 若单词出现次数低于该阈值，则这个单词会被忽略
    #window: 窗口大小
    #sample: 频率高于此阈值，单词才会被采样，取值范围是(0 - 1e-3)
    model.wv.save_word2vec_format(config.vector_word_filename, binary=False)
    print('-------------------------------------------')
    print("Training word2vec model cost %.3f seconds...\n" % (time.time() - t1))

if __name__ == '__main__':
    config=TextConfig()
    filenames=[config.train_filename,config.test_filename,config.val_filename]
    train_word2vec(filenames)

