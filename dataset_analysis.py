def wordcloud(df, tweet_column, label_column, plot_title, background_color):
    '''
    Construção de duas wordclouds para tweets positivos e negativos
    '''
    from wordcloud import STOPWORDS, WordCloud
    import matplotlib.pyplot as plt

    # Plotting wordclouds for both negative and positive tweets
    stopwords = set(STOPWORDS)

    # Removing 'user' word as it does not hold any importance in our context
    stopwords.add('user')        

    negative_tweets = df[tweet_column][df[label_column]==0].to_string()
    wordcloud_negative = WordCloud(width = 800, height = 800, 
                                background_color =background_color, stopwords = stopwords,
                                min_font_size = 10).generate(negative_tweets)

    positive_tweets = df[tweet_column][df[label_column]==1].to_string()
    wordcloud_positive = WordCloud(width = 800, height = 800, 
                                background_color =background_color, stopwords = stopwords,
                                min_font_size = 10).generate(positive_tweets)
    
    # Plotting the WordCloud images
    print(plot_title)                     
    plt.figure(figsize=(14, 6), facecolor = None)

    plt.subplot(1, 2, 1)
    plt.imshow(wordcloud_negative)
    plt.axis("off")
    plt.title('Negative Tweets', fontdict={'fontsize': 20})

    plt.subplot(1, 2, 2)
    plt.imshow(wordcloud_positive)
    plt.axis("off")
    plt.title('Positive Tweets', fontdict={'fontsize': 20})

    plt.tight_layout() 
    plt.show()


def get_top_n_words(corpus, n=None, n_grams = 1, stopwords_removal = True):
    '''
    Obter os n-gramas mais comuns no dataset
    '''
    from sklearn.feature_extraction.text import CountVectorizer

    if stopwords_removal:
        vec = CountVectorizer(ngram_range=(n_grams,n_grams), stop_words='english').fit(corpus)
    else:
        vec = CountVectorizer(ngram_range=(n_grams,n_grams)).fit(corpus)
        
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

def n_gram_analysis(df, dataset_title, label_column, stopwords_removal, n_grams = 1):
    '''
    Análise gráfica dos n-gramas mais comuns
    '''
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    #unigrams before stopwords
    common_words_train_pos = get_top_n_words(df.tweet[df[label_column] == 1], 20, n_grams, stopwords_removal= stopwords_removal)
    common_words_train_neg = get_top_n_words(df.tweet[df[label_column] == 0], 20, n_grams, stopwords_removal= stopwords_removal)


    df1 = pd.DataFrame(common_words_train_pos, columns = ['ReviewText' , 'count'])
    grouped_data_pos = df1.groupby('ReviewText').sum()['count'].sort_values(ascending=False)

    df2 = pd.DataFrame(common_words_train_neg, columns = ['ReviewText' , 'count'])
    grouped_data_neg = df2.groupby('ReviewText').sum()['count'].sort_values(ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))


    # Plotting the first DataFrame
    sns.barplot(x=grouped_data_pos.values, y=grouped_data_pos.index, ax=ax1, color='lightblue')
    ax1.set_xlabel('Counts')
    ax1.set_ylabel('n-grams')
    if not stopwords_removal:
        ax1.set_title('Positive tweets - ' +  dataset_title + ' - with stopwords')
    else:
        ax1.set_title('Positive tweets - ' +  dataset_title + ' - without stopwords')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
    # Plotting the second DataFrame
    sns.barplot(x=grouped_data_neg.values, y=grouped_data_neg.index, ax=ax2, color='lightblue')
    ax2.set_xlabel('Counts')
    ax2.set_ylabel('n-grams')
    if not stopwords_removal:
        ax2.set_title('Negative tweets - ' +  dataset_title + ' - with stopwords')
    else:
        ax2.set_title('Negative tweets - ' +  dataset_title + ' - without stopwords')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)

    # Adjusting the layout
    plt.tight_layout()

    # Displaying the plots
    plt.show()