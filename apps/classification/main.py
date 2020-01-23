# Coded with <3 Razuvitto
# location : apps/classification/main.py
# April 2018

from django.core.files.storage import default_storage

# import library
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from nltk.corpus import stopwords 

news_data = pd.read_csv("apps/classification/news-data.csv") # read data
del news_data['Unnamed: 0'] # delete number of news rows
# print (len(news_data)) # count news
news_data.head(30) 
news_data.count() #count based on attribute

news_data=news_data[~news_data['content'].duplicated()] # remove the duplicate using duplicated() function
news_data=news_data.reset_index(drop=True)
# print (len(news_data)) # count total of news after deleting duplicate data [32602 -> 31572]
# print (news_data.content[0]) # print news in array [0] for example
# news_data.head()

content = news_data.content
new_sentence = [word.lower() for word in content] # lower case process using lower() function
new_sentence

# import library
import string
from string import digits
string.punctuation
new_sentences = []

for words in new_sentence:
    for punctuation in string.punctuation:
        words = words.replace(punctuation, "") # remove punctuation
    for number in '1234567890':
        words = words.replace(number, "") # remove number
    # print (words)
    new_sentences.append(words)

# get Vector Count
count_vect = CountVectorizer(stop_words=stopwords.words('english'))
X_train_counts = count_vect.fit_transform(news_data.content)

# save word vector
pickle.dump(count_vect.vocabulary_, open("count_vector.pkl","wb"))

from sklearn.feature_extraction.text import TfidfTransformer

# transform word vector to tfidf
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# save tfidf
pickle.dump(tfidf_transformer, open("tfidf.pkl","wb"))

# import library for algorithm
from sklearn import svm
from sklearn.model_selection import train_test_split
clf_svm = svm.LinearSVC()
X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, news_data.label, test_size=0.25, random_state=42) # use 0.50% of data for test
clf_svm.fit(X_train_tfidf, news_data.label)

# save model
pickle.dump(clf_svm, open("svm_model.pkl", "wb"))

# import library
import pandas
predicted = clf_svm.predict(X_test)
result_svm = pandas.DataFrame( {'true_labels': y_test,'predicted_labels': predicted}) # compare the actual category and prediction category
result_svm.to_csv('result_svm.csv', sep = ',') # save the result to the file csv
# for predicted_item, result in zip(predicted, y_test):
    # print(category_list[predicted_item], ' - ', category_list[result]) # print the result


def main(input_text):
# import library
    import pickle
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer

    category_list = ["sport", "world", "us", "business", "health", "entertainment", "sci_tech"]

    docs_new = input_text # input news title for classification 
    docs_new = [docs_new]

   # load model
    loaded_vec = CountVectorizer(vocabulary=pickle.load(open("count_vector.pkl", "rb")))
    loaded_tfidf = pickle.load(open("tfidf.pkl","rb"))
    loaded_model_svm = pickle.load(open("svm_model.pkl","rb"))
    loaded_model_nb = pickle.load(open("nb_model.pkl","rb"))

    X_new_counts = loaded_vec.transform(docs_new)
    X_new_tfidf = loaded_tfidf.transform(X_new_counts)
    predicted_svm = loaded_model_svm.predict(X_new_tfidf)
    predicted_nb = loaded_model_nb.predict(X_new_tfidf)

    return category_list[predicted_svm[0]], category_list[predicted_nb[0]]  # print the category based on input
     # print the category based on input
# print(category_list[predicted[0]]) # print the category based on input
                                              
def report_svm():
    # import library
    from sklearn.metrics import confusion_matrix  

    confusion_mat = confusion_matrix(y_test,predicted) # confusion matrix based on actual and predicted
    return confusion_mat                                             
    #print(confusion_mat)   

def score_svm():
   # import library
    from sklearn.metrics import accuracy_score
    y_pred = clf_svm.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred) * 100
    return accuracy