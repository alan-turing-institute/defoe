"""
Gets the Latent Dirochelet Allocation (LDA) topics for words within
articles.
"""

from yaml import load

from pyspark.ml.feature import CountVectorizer, StopWordsRemover
from pyspark.mllib.clustering import LDA
from pyspark.mllib.linalg import Vectors
from pyspark.sql import Row, SparkSession

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word
from defoe.papers.query_utils import PreprocessWordType


def do_query(issues, config_file=None, logger=None):
    """
    Gets the Latent Dirochelet Allocation (LDA) topics for words
    within articles.

    config_file must be the path to a LDA configuration file in YAML
    format. For example:

        keyword: <KEYWORD>
        optimizer: online|em
        max_iterations: <N>
        ntopics: <N>
        topic_words: <N>

    <N> must be >= 1 for each parameter.

    The keyword and words in documents are normalized, by removing all
    non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <0>: [<WORD_0>, ..., <WORD_topicwords>],
          <1>: [<WORD_0>, ..., <WORD_topicwords>],
          <2>: [<WORD_0>, ..., <WORD_topicwords>],
          ...
          <ntopics>: [<WORD_0>, ..., <WORD_topicwords>],
          years:[<MIN_YEAR>, <MAX_YEAR>]
        }

    :param issues: RDD of defoe.papers.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: LDA topics
    :rtype: dict
    """
    with open(config_file, 'r') as f:
        config = load(f)
        keyword = config['keyword']
        optimizer = config['optimizer']
        if optimizer != 'online' and optimizer != 'em':
            raise ValueError("optmizer must be 'online' or 'em' but is '{}'"
                             .format(optimizer))
        max_iterations = config['max_iterations']
        if max_iterations < 1:
            raise ValueError('max_iterations must be at least 1')
        ntopics = config['ntopics']
        if ntopics < 1:
            raise ValueError('ntopics must be at least 1')
        topic_words = config['topic_words']
        if topic_words < 1:
            raise ValueError('topic_words must be at least 1')

    keyword = query_utils.normalize(keyword)

    # [date, ...]
    # =>
    # [(yesr, year), ...]
    # =>
    # (year, year)
    min_year, max_year = issues \
        .filter(lambda issue: issue.date) \
        .map(lambda issue: (issue.date.year, issue.date.year)) \
        .reduce(min_max_tuples)

    # [issue, issue, ...]
    # =>
    # [article, article, ...]
    # =>
    # [(article, 0), (article, 1), ...]
    # =>
    # [Row, Row, ...]
    articles_rdd = issues.flatMap(lambda issue: issue.articles) \
        .filter(lambda article:
                article_contains_word(article,
                                      keyword,
                                      PreprocessWordType.NORMALIZE)) \
        .zipWithIndex() \
        .map(article_idx_to_words_row)

    spark = SparkSession \
        .builder \
        .appName('lda') \
        .getOrCreate()

    articles_df = spark.createDataFrame(articles_rdd)

    remover = StopWordsRemover(inputCol='words', outputCol='filtered')
    articles_df = remover.transform(articles_df)

    vectortoriser = CountVectorizer(inputCol='filtered', outputCol='vectors')
    model = vectortoriser.fit(articles_df)

    vocabulary = model.vocabulary
    articles_df = model.transform(articles_df)

    corpus = articles_df \
        .select('idx', 'vectors') \
        .rdd \
        .map(lambda a: [a[0], Vectors.fromML(a[1])]) \
        .cache()

    # Cluster the documents into N topics using LDA.
    lda_model = LDA.train(corpus,
                          k=ntopics,
                          maxIterations=max_iterations,
                          optimizer=optimizer)
    topics_final = [topic_render(topic, topic_words, vocabulary)
                    for topic in lda_model.describeTopics(maxTermsPerTopic=topic_words)]

    topics = [('years', [min_year, max_year])]
    for i, topic in enumerate(topics_final):
        term_words = []
        for term in topic:
            term_words.append(term)
        topics.append((str(i), term_words))
    return topics


def min_max_tuples(fst, snd):
    """
    Given two tuples (fst_min, fst_max) and (snd_min, snd_max) return
    (min, max) where min is min(fst_min, snd_min) and
    max is max(fst_max, snd_max).

    :param fst: tuple
    :type fst: tuple
    :param fst: tuple
    :type snd: tuple
    :return: tuple
    :rtype: tuple
    """
    fst_min, fst_max = fst
    snd_min, snd_max = snd
    return (min(fst_min, snd_min), max(fst_max, snd_max))


def article_idx_to_words_row(article_idx):
    """
    Given a tuple with an article and an index, return a Row with the
    index ad a list of the words in the article.

    The words in the article are normalized, by removing all
    non-'a-z|A-Z' characters.

    Any stop words (words of less than 2 characters) are ignored.

    :param article_idx: tuple
    :type article_idx: tuple(defoe.papers.article.Article, int)
    :return: Row
    :rtype: pyspark.sql.Row
    """
    article, idx = article_idx
    words = []
    for word in article.words:
        normalized_word = query_utils.normalize(word)
        if len(word) > 2:   # Anything less is a stop word
            words.append(normalized_word)
    return Row(idx=idx, words=words)


def topic_render(topic, num_words, vocabulary):
    """
    Convert a topic result to a list of words

    :param topic: topic data, first element is list of length
    num_words, which contains indices which are used to extract words
    from vocabulary to form the list that is returned
    :type topic: tuple(list(int), list(float))
    :param num_words: number of words, equal to "topic_words"
    specified in query configuration file
    :type num_words: int
    :param vocabulary: vocabulary
    :type vocabulary: list(unicode)
    :return: list of num_words words from vocabulary
    :rtype: list(unicode)
    """
    indices = topic[0]
    terms = []
    for i in range(num_words):
        term = vocabulary[indices[i]]
        terms.append(term)
    return terms
