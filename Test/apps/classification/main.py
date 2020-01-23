# Coded with <3 Razuvitto
# location : Test/apps/classification/main.py
# April 2018

from django.core.files.storage import default_storage

f = default_storage.open('apps/classification/news','r')
text = f.read()
news = text.split("\n\n")
count = {'sport': 0, 'world': 0, "us": 0, "business": 0, "health": 0, "entertainment": 0, "sci_tech": 0}


import pandas
import glob

category_list = ["sport", "world", "us", "business", "health", "entertainment", "sci_tech"]
directory_list = ["apps/classification/data/sport/*.txt", "apps/classification/data/world/*.txt", "apps/classification/data/us/*.txt", "apps/classification/data/business/*.txt", "apps/classification/data/health/*.txt",
                  "apps/classification/data/entertainment/*.txt", "apps/classification/data/sci_tech/*.txt", ]

text_files = list(map(lambda x: glob.glob(x), directory_list))
text_files = [item for sublist in text_files for item in sublist]

training_data = []

for t in text_files:
    f = default_storage.open(t, 'r')
    f = f.read()
    t = f.split('\n')
    training_data.append({'data': t[0] + ' ' + t[1], 'flag': category_list.index(t[6])})

training_data[0]
training_data = pandas.DataFrame(training_data, columns=['data', 'flag'])
training_data.to_csv("train_data.csv", sep=',', encoding='utf-8')
#print(training_data.data.shape)

import pickle
from sklearn.feature_extraction.text import CountVectorizer


#GET VECTOR COUNT
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(training_data.data)

#SAVE WORD VECTOR
pickle.dump(count_vect.vocabulary_, default_storage.open("apps/classification/count_vector.pkl","wb"))

from sklearn.feature_extraction.text import TfidfTransformer

#TRANSFORM WORD VECTOR TO TF IDF
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

#SAVE TF-IDF
pickle.dump(tfidf_transformer, default_storage.open("apps/classification/tfidf.pkl","wb"))

from sklearn import svm
from sklearn.model_selection import train_test_split

clf_svm = svm.LinearSVC()
X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, training_data.flag, test_size=0.25, random_state=42)
clf_svm.fit(X_train_tfidf, training_data.flag)
pickle.dump(clf_svm, default_storage.open("apps/classification/svm.pkl", "wb"))

predicted = clf_svm.predict(X_test)
result_svm = pandas.DataFrame( {'true_labels': y_test,'predicted_labels': predicted})
result_svm.to_csv('res_svm.csv', sep = ',')

#for predicted_item, result in zip(predicted, y_test):
    #print(category_list[predicted_item], ' - ', category_list[result])

def main(input_text):
    import pickle
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer

    category_list = ["sport", "world", "us", "business", "health", "entertainment", "sci_tech"]

    docs_new = input_text
    docs_new = [docs_new]

    # LOAD MODEL
    loaded_vec = CountVectorizer(vocabulary=pickle.load(default_storage.open("apps/classification/count_vector.pkl", "rb")))
    loaded_tfidf = pickle.load(default_storage.open("apps/classification/tfidf.pkl", "rb"))
    loaded_model = pickle.load(default_storage.open("apps/classification/svm.pkl", "rb"))

    X_new_counts = loaded_vec.transform(docs_new)
    X_new_tfidf = loaded_tfidf.transform(X_new_counts)
    predicted = loaded_model.predict(X_new_tfidf)
    return category_list[predicted[0]]