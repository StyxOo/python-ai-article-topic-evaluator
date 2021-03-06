import parameterization

_topics = None
_words_per_topic = None


def _get_percent(part, whole):
    """
    Calculate a percent value
    :param part: part
    :param whole: whole
    :return: percent
    """
    return (part / whole) * 100


def _data_total_to_percent(data, total):
    """
    Turn total data to percents
    :param data: data to convert
    :param total: total to use for conversion
    :return: data in percent
    """
    for entry in data:
        data[entry] = _get_percent(data[entry], total)
    return data


def _get_topic_data(articles):
    """
    Get topic data
    :param articles: trin articles
    :return: topic data and total topic count
    """
    data = {}
    total_topics = 0
    for article in articles:
        for topic in article['topics']:
            total_topics += 1
            if topic in data:
                data[topic] += 1
            else:
                data[topic] = 1
    return data, total_topics


def _get_topic_percent_data(articles):
    """
    Get topic data in percent
    :param articles: train articles
    :return: topic data in percent
    """
    data, total_topics = _get_topic_data(articles)
    return _data_total_to_percent(data, total_topics)


def _add_vectors(a, b):
    c = a
    for i in range(len(a)):
        c[i] = a[i] + b[i]
    return c


def _get_topic_word_data(articles):
    """
    Get word data for each topic
    :param articles: train articles
    :return: topic word data
    """
    data = {}
    for article in articles:
        vector = parameterization.get_vector_for(article)
        for topic in article['topics']:
            if topic not in data:
                data[topic] = vector
            else:
                data[topic] = _add_vectors(data[topic], vector)
    return data


def _get_topic_word_percent_data(articles):
    """
    Get topic word data in percent
    :param articles: train articles
    :return: topic word data in percent
    """
    data = _get_topic_word_data(articles)
    for topic in data:
        total_words = 0
        for i in range(len(data[topic])):
            total_words += data[topic][i]
        for i in range(len(data[topic])):
            data[topic][i] = _get_percent(data[topic][i], total_words)
    return data


def evaluate(articles, text):
    """
    Evaluates a text with given train articles
    :param articles: train articles
    :param text: text to evaluate
    :return: topic of text
    """
    global _topics, _words_per_topic
    _topics = _get_topic_percent_data(articles)
    _words_per_topic = _get_topic_word_percent_data(articles)

    text_vector = parameterization.generate_vector_for(text)

    highest_probability = 0
    highest_probability_topic = None

    for topic in _topics.keys():
        product = 1
        for i in range(len(text_vector)):
            multipy = _words_per_topic[topic][i] * text_vector[i]
            if multipy > 0:
                product *= multipy * 100
            else:
                product *= 1
        product *= _topics[topic]

        # unique_text = []
        # for word in text:
        #     if word not in unique_text:
        #         unique_text.append(word)

        #
        # for topic in _topics.keys():
        #     product = 1
        #     for word in unique_text:
        #         if word in _words_per_topic[topic].keys():
        #             product *= _words_per_topic[topic][word]
        #         else:
        #             product *= 1e-15
        #     product *= _topics[topic]

        if product > highest_probability:
            highest_probability = product
            highest_probability_topic = topic
    return highest_probability_topic