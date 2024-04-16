import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from snowballstemmer import stemmer
import random

class PeriChatbot:
    def __init__(self, data_file):
        self.stemmer = stemmer('turkish')
        self.corpus, self.responses = self.load_data(data_file)
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def preprocess_text(self, text):
        text = text.lower()
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('turkish'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        stemmed_tokens = [self.stemmer.stemWord(word) for word in filtered_tokens]
        return " ".join(stemmed_tokens)

    def load_data(self, data_file):
        with open(data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        corpus = []
        responses = []
        for item in data:
            corpus.append(self.preprocess_text(item['user_input']))
            responses.append(item['bot_response'])
        return corpus, responses

    def get_response(self, input_text, threshold=0.6):
        input_text = self.preprocess_text(input_text)
        input_vector = self.vectorizer.transform([input_text])
        similarities = cosine_similarity(input_vector, self.tfidf_matrix)

        # En yüksek benzerlik skoruna sahip olan endeksi bulun
        max_index = np.argmax(similarities)

        # Eğer belirtilen eşik değerinden yüksek olan bir skor varsa, o skora karşılık gelen yanıtı döndürün
        if similarities[0][max_index] >= threshold:
            return self.responses[max_index]

        # Eğer belirtilen eşik değerinden yüksek bir skor yoksa, en yakın metne karşılık gelen yanıtı döndürün
        return self.responses[max_index]

    def welcome_message(self):
        ascii_sanat = """
        
        oooo    oooo            .o88o.                ooooooooo.                       o8o  
        `888   .8P'             888 `"                `888   `Y88.                     `"'  
        888  d8'     .oooo.   o888oo   .ooooo.        888   .d88'  .ooooo.  oooo d8b oooo  
        88888[      `P  )88b   888    d88' `88b       888ooo88P'  d88' `88b `888""8P `888  
        888`88b.     .oP"888   888    888ooo888       888         888ooo888  888      888  
        888  `88b.  d8(  888   888    888    .o       888         888    .o  888      888  
        o888o  o888o `Y888""8o o888o   `Y8bod8P'      o888o        `Y8bod8P' d888b    o888o 

        """
        print(ascii_sanat)
        
        welcome_responses = [
            "Kafe Peri' ye Hoşgeldiniz! \nMenüyü görmek için 'menü' yazabilir veya 'kahveler' gibi bir arama yapabilirsiniz.\n",
        ]
        return random.choice(welcome_responses)


# JSON dosyasından veri okuyun
data_file = "veriler.json"

# Chatbot'u başlat
chatbot = PeriChatbot(data_file)

# Hoş geldiniz mesajı göster
print(chatbot.welcome_message())

# Örnek bir kullanıcı etkileşimi
while True:
    user_input = input("Sen: ")
    response = chatbot.get_response(user_input)
    print("Peri:", response)