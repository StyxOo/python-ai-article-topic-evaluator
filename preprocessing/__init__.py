from . import sgm_reader
from . import rewrite

import os
import json


def process():
    """
    Performs all preprocessing steps
    :return:
    """
    sgm_reader.main()
    rewrite.main()


def get_train_set():
    """
    get all articles of the training set
    :return: training articles
    """
    articles_path = os.path.join(os.path.dirname(__file__), 'articles_rewritten.json')
    if not os.path.isfile(articles_path):
        print("'articles_rewritten.json' does not exist. Make sure to run 'sgm_reader.py' first.")
        exit(1)
    with open(articles_path) as json_file:
        return json.load(json_file)['train']


def get_test_set():
    articles_path = os.path.join(os.path.dirname(__file__), 'articles_rewritten.json')
    if not os.path.isfile(articles_path):
        print("'articles_rewritten.json' does not exist. Make sure to run 'sgm_reader.py' first.")
        exit(1)
    with open(articles_path) as json_file:
        test_arts = json.load(json_file)['test']

    test_with_topic = []
    for a in test_arts:
        if len(a['topics']) > 0:
            test_with_topic.append(a)
    return test_with_topic
