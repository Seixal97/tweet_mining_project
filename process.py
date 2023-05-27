import re
import logging as log
import pandas as pd


class BasicPreprocessor(object):
    '''
    Classe para pré-processamento do dataset
    '''

    def __init__(self):
        '''
        Construtor
        '''
        
    def preprocess(self, df: pd.DataFrame, column_name:str):
        """
        Processa todo o dataset (com todos os métodos), de uma só vez

        :param df: dataframe
        :param column_name: nome da coluna com os tweets
        """
        self.lowercase(df, column_name)
        self.remove_usernames(df, column_name)
        self.remove_urls(df, column_name)
        self.split_slash(df, column_name)
        self.remove_repeated_ponctuation(df, column_name)
        self.expand_contractions(df, column_name)
        self.remove_misc(df, column_name)
        self.remove_hashtags(df, column_name)
        self.remove_numbers(df, column_name)
        self.remove_elongated_words(df, column_name)
        self.remove_emoticons(df, column_name)


    
    def lowercase(self, df: pd.DataFrame, column_name:str):
        """
        Passar tweets para letras minúsculas
        """
        df[column_name] = df[column_name].apply(str.lower)


    
    def remove_urls(self, df, column_name:str, replacement=''):
        """
        Remover urls
        """
        df[column_name] = df[column_name].apply(lambda tweet_text: re.sub(r'https?://([A-Za-z.0-9/])*', replacement, tweet_text))


                     
    def remove_usernames(self, df:pd.DataFrame, column_name:str, replacement=''):
        """
        Remover usernames
        """
        df[column_name] = df[column_name].apply(lambda tweet_text: re.sub(r'@(\w)+', replacement, tweet_text))
        
        
    
    def split_slash(self, df, column_name:str):
        """
        Acresentar espaçoes entre '/'. Realizar apenas depois de remover os urls
        """
        df[column_name] = df[column_name].apply(lambda tweet_text: re.sub(r'/', ' / ', tweet_text))
        
        
    
    
    def remove_numbers(self, df, column_name:str, replacement=''):
        """
        Remover números, exceto os presentes nos hashtags
        """
        def replaceNumbers(text, replacement):
            replaced_sentence = []
            for word in text.split(' '):
                if not word.startswith('#'):
                    word = re.sub(r'[-+]?[.\d]*[\d]+[:,.\d]*', replacement, word)
                    replaced_sentence.append(' ')
                    replaced_sentence.append(word)
                else:
                    replaced_sentence.append(' ')
                    replaced_sentence.append(word)
            return ''.join(replaced_sentence)
        
        df[column_name] = df[column_name].apply(lambda tweet_text: replaceNumbers(tweet_text, replacement))
    
    
    
    
    def remove_hashtags(self, df, column_name:str):
        df[column_name] = df[column_name].apply(lambda tweet_text: re.sub(r'#(\S+)', '', tweet_text))
    
    

        
    def remove_repeated_ponctuation(self, df, column_name:str, replacement=''):          
        """
        Short all repetitions of punctuations and insert the signal _PUNCT_REPEATED_ (default)
        Ex. hoooo! my God!????? becomes hoooo! my God!? _PUNCT_REPEATED_
        """
        df[column_name] = df[column_name].apply(lambda tweet_text: re.sub(r'([!?.]){2,}', r'\g<1>'+replacement, tweet_text))
    
    
    def remove_elongated_words(self, df, column_name:str):
        '''
        Remoção de palavras alongadas. Exemplo: 'Helloooooo' -> 'Hello'
        '''
        #elongated words
        def remove_elongated_words_aux(original_sentence):
            ''' Função auxiliar'''
            normalized_sentence = list()

            for word in original_sentence.split():
                normalized_word = re.sub(r'(\w)\1{2,}', r'\1', word)
                normalized_sentence.append(normalized_word)

            return ' '.join(normalized_sentence)

        df[column_name] = df[column_name].apply(remove_elongated_words_aux)



    def remove_misc (self, df, column_name: str):
        '''
        Remover vários caracteres de ruído. Exemplo: •‘’“”~… &amp &lt &gt
        '''
        df[column_name] = df[column_name].apply(lambda text: re.sub(r'(\w)\.(\w)', r'\1 . \2', text)) #split dot
        df[column_name] = df[column_name].apply(lambda text: re.sub(r'(\w)\-(\w)', r'\1 - \2', text)) #split hifen
        df[column_name] = df[column_name].apply(lambda text: re.sub(r'\|', '', text)) #remove pipe
        df[column_name] = df[column_name].apply(lambda text: re.sub(r"\'", '', text))
        df[column_name] = df[column_name].apply(lambda text: re.sub(r'\-', '', text)) #remove pipe
        df[column_name] = df[column_name].apply(lambda text: re.sub(r"\'", '', text))
        df[column_name] = df[column_name].apply(lambda text: re.sub(r'•', '', text)) #remove •
        df[column_name] = df[column_name].apply(lambda text: re.sub(r"[‘’“”~…¿°⌓¬_]", "", text)) #remove ‘’“”~…
        df[column_name] = df[column_name].apply(lambda text: re.sub(r'&amp;', 'and', text)) #remove &amp
        df[column_name] = df[column_name].apply(lambda text: re.sub(r'&lt;', '<', text)) #remove &lt
        df[column_name] = df[column_name].apply(lambda text: re.sub(r'&gt;', '>', text)) #remove  

    def expand_contractions(self, df, column_name:str):
        '''
        Expansão de contrações.
        Exemplo: "It's" -> "It is"
        '''
        import contractions

        def expand_contractions_aux(text):
            expanded_words = list()

            for word in text.split():
                expanded_words.append(contractions.fix(word))
            expanded_text = ' '.join(expanded_words)

            return expanded_text

        df[column_name] = df[column_name].apply(expand_contractions_aux)


    
    def remove_emoticons(self, df, column_name:str):
        '''
        Remoção de emojis (package emoji + expressões regulares)
        '''
        import emoji
        def remove_emoticons_aux(text):
            emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    u"\U00002500-\U00002BEF"  # chinese char
                    u"\U00002702-\U000027B0"
                    u"\U00002702-\U000027B0"
                    u"\U000024C2-\U0001F251"
                    u"\U0001f926-\U0001f937"
                    u"\U00010000-\U0010ffff"
                    u"\u2640-\u2642"
                    u"\u2600-\u2B55"
                    u"\u200d"
                    u"\u23cf"
                    u"\u23e9"
                    u"\u231a"
                    u"\u20E3"
                    u"\ufe0f"  # dingbats
                    u"\u3030"
                    u"\U000feb13-\U000feb18"
                    u"\U000fe040"
                                    "]+", flags=re.UNICODE)
            
            return emoji_pattern.sub(r'', text)

        df[column_name] = df[column_name].apply(remove_emoticons_aux)
        df[column_name] = df[column_name].apply(lambda x: emoji.replace_emoji(x, replace = ''))


    def correct_spelling(self, df, column_name: str):
        '''
        Correção de erros de escrita
        '''
        from textblob import TextBlob

        def correct_spelling_aux(sentence):
            checker = TextBlob(sentence)
            correct_sentence = checker.correct()
            return str(correct_sentence)

        df[column_name] = df[column_name].apply(correct_spelling_aux)
