"""
A module to get LDA topic for the years that are in the current nodes group
"""

from pyspark.ml.feature import CountVectorizer, StopWordsRemover
from pyspark.mllib.clustering import LDA
from pyspark.mllib.linalg import Vectors
from pyspark.sql import Row, SparkSession

from regex import I, U, compile as comp

from yaml import load


def do_query(issues, input_file, _log):
    """
    Get the Latent Dirochelet Allocation topics for this group of articles
    """

    # Extract parameters from input_rules
    with open(input_file, 'r') as infile:
        keys = load(infile)
        keyword = keys['keyword']
        optimizer = keys['optimizer']
        if optimizer != 'online' and optimizer != 'em':
            raise ValueError("Optmizer must be 'online' or 'em' but is '{}'"
                             .format(optimizer))
        max_iterations = keys['max_iterations']
        if max_iterations < 1:
            raise ValueError('max_iterations must be at least 1')
        ntopics = keys['ntopics']
        if ntopics < 1:
            raise ValueError('ntopics must be at least 1')
        topic_words = keys['topic_words']
        if topic_words < 1:
            raise ValueError('topic_words must be at least 1')
    keyword_pattern = comp(r'\b{}\b'.format(keyword), U | I)

    # Map each article in each issue to a year of publication
    min_year, max_year = issues \
        .filter(lambda issue: issue.date) \
        .map(lambda issue: (issue.date.year, issue.date.year)) \
        .reduce(find_min_and_max)

    articles_rdd = issues.flatMap(lambda issue: issue.articles) \
        .filter(contains_keyword(keyword_pattern)) \
        .zipWithIndex() \
        .map(to_row_with_words)

    spark = SparkSession \
        .builder \
        .appName('lda') \
        .getOrCreate()

    articles_df = spark.createDataFrame(articles_rdd)

    remover = StopWordsRemover(inputCol='words', outputCol='filtered')
    articles_df = remover.transform(articles_df)

    vectortoriser = CountVectorizer(inputCol='filtered', outputCol='vectors')
    model = vectortoriser.fit(articles_df)
    vocab_array = model.vocabulary
    articles_df = model.transform(articles_df)

    corpus = articles_df \
        .select('idx', 'vectors') \
        .rdd \
        .map(lambda a: [a[0], Vectors.fromML(a[1])]) \
        .cache()

    # Cluster the documents into n topics using LDA
    lda_model = LDA.train(corpus, k=ntopics, maxIterations=max_iterations,
                          optimizer=optimizer)
    # topics = lda_model.topicsMatrix()
    # _log.error(topics)
    topics_final = [topic_render(topic, topic_words, vocab_array) for topic in
                    lda_model.describeTopics(maxTermsPerTopic=topic_words)]

    topics = [('Years', [min_year, max_year])]
    for i, topic in enumerate(topics_final):
        t_words = []
        for term in topic:
            t_words.append(term)
        topics.append((str(i), t_words))

    return topics


def to_row_with_words(idx_article):
    """
    Given a tuple with an idx and an article, return
    a Row with an idx and a list of words
    """
    article, idx = idx_article
    words = []
    non_alpha = comp(r'[^a-z]', U)
    for word in article.words:
        word = word.lower()
        word = non_alpha.sub('', word)
        if len(word) > 2:   # Anything less is a stop word
            words.append(word)
    return Row(idx=idx, words=words)


def find_min_and_max(fst, snd):
    """
    Given to date ranges, expand them to include both.
    Assume that all date in the middle also exist
    """
    low_1, high_1 = fst
    low_2, high_2 = snd
    return (min(low_1, low_2), max(high_1, high_2))


def topic_render(topic, num_words, vocab_array):
    """
    Convert a topic result to a list of words
    """
    terms = topic[0]
    result = []
    for i in range(num_words):
        term = vocab_array[terms[i]]
        result.append(term)
    return result


def contains_keyword(pattern):
    """
    Create a function that filters articles based on whether they have a
    given keyword or not
    """
    def filter_function(article):
        """
        Accept only articles that contain the given keyword pattern
        """
        return pattern.findall(article.words_string)
    return filter_function
