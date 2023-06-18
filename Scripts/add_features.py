import pandas as pd

def insert_column(dataframe, new_column, column_name, dummies=False, label_prefix=None):
    '''
    Função auxiliar para inserção de colunas em dataset
    '''
    indexes = list(dataframe.index.values)
    dataframe[column_name] = pd.Series(new_column, index=indexes)
    if dummies:
        df_dummies = pd.get_dummies(dataframe[column_name], prefix = label_prefix)
        dataframe = pd.concat([dataframe.drop(column_name, axis = 1), df_dummies], axis = 1)
    return dataframe


def medication_score(dataframe, filename):
    '''
    Função para atribuir um score (contagem) a cada tweet, dependendo se possui ou não medicamentos na lista 'filename'
    '''
    res = []
    for tweet_list in dataframe.tweet:
        score = 0
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            for word in tweet_list:
                if word in lines:
                    score += 1
            res.append(score)
    dataframe = insert_column(dataframe, res, 'medication_score')
    return dataframe

def add_tweet_info(df):
    '''
    Função para retirar informações adicionais quanto à estrutura do tweet (tamanho, nº de palavras, nº de hashtags, etc.)
    '''
    df['tweet_length'] = df['tweet'].str.len()
    df['num_hashtags'] = df['tweet'].str.count('#')
    df['num_exclamation_marks'] = df['tweet'].str.count('\!')
    df['num_question_marks'] = df['tweet'].str.count('\?')
    df['total_tags'] = df['tweet'].str.count('@')
    df['num_punctuations'] = df['tweet'].str.count('[.,:;]')
    df['num_words'] = df['tweet'].apply(lambda x: len(x.split()))
