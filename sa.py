import nltk
import os.path
import random
import pickle
from nltk.corpus import movie_reviews
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
import demjson
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
class JAM:
    def __init__(self):
        self.data_set_dir = "./dataset/"
        self.feature_words_path = "./trainedset/feature_words.pickle"
        self.stop_words = "./dataset/stop_words.pickle"
        self.naive_base_model = "./trainedset/naive_base_model.pickle"


    def clean_words(self, words):
            lemmatizer = WordNetLemmatizer()
            stopwords = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours',
                         u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers',
                         u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves',
                         u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are',
                         u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does',
                         u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as',
                         u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between',
                         u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up',
                         u'down', u'in', u'out', u'on', u'off', u'over', u'again', u'further', u'then', u'once',
                         u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each',
                         u'other', u'such', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't',
                         u'can', u'will', u'just', u'should', u'now', u'd', u'll', u'm', u'o', u're', u've', u'y']
            filtered = []
            for word in words:
                word = word.lower()
                if word.isalpha() and word not in stopwords:
                    word = lemmatizer.lemmatize(word)
                    filtered.append(word)
            return filtered

    def create_feature_words_pickle(self):

                all_words = []
                file_name="dataset"
                data_set_file = open(self.data_set_dir + file_name + ".txt", 'r')
                for line in data_set_file:

                    all_words = all_words + self.clean_words(wordpunct_tokenize(line))
                all_words_freq_dist = nltk.FreqDist(all_words)
                feature_words_dist = all_words_freq_dist.most_common()[:4000]


                feature_words = []
                for word in feature_words_dist:
                    feature_words.append((word[0], False))
                self.feature_words = dict(feature_words)
                print (len(self.feature_words))
                file = open(self.feature_words_path, 'wb');
                pickle.dump(feature_words, file)
                file.close()
    def create_feature_set(self,tokens):

        def antonym(word):
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    if l.antonyms():
                        if(l.antonyms()[0].name().isalpha()):
                            return l.antonyms()[0].name()
            return word

        def reverse_text(words):
            remove_neg_words = ['no','nor','not','don','ain','aren','couldn','didn','doesn','hadn','hasn','haven', 'isn',  'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']

            skip = 0;
            rev = []
            for word in words:
                if word not in remove_neg_words:
                    if skip == 0:
                        rev.append(antonym(word))
                    else:
                        if word == 't':
                            skip = 1;
                        elif word == 'a':
                            skip = 1;
                        else:
                            skip = 0;
                            rev.append(word)
                else:
                    skip = 1
            return rev

        r = []
        feature_set_1 = dict(self.feature_words)
        feature_set_2 = dict(self.feature_words)
        for word in tokens:
            if word in feature_set_1.keys():
                feature_set_1[word] = True
        r.append(feature_set_1)
        reverse = reverse_text(tokens)
        for word in reverse:
            if word in feature_set_2.keys():
                feature_set_2[word] = True
        r.append(feature_set_2)
        return r

    def create_naive_bayes_model_pickle(self):
        feature_set = []
        print "Feature set creating. !"
        #for i in range(1, 4, 1):
        file_name = "dataset"+ ".txt"
        file = open(self.data_set_dir + file_name, 'r')
        j = 0
        for line in file:
        # print "txt%s%s" % (i, j)
        #     print line
            j += 1
            words = wordpunct_tokenize(line)
            if words[len(words) - 1] == "1":
                label = "pos"
                reverse_label = "neg"
            elif words[len(words) - 1] == "0":
                label = "neg"
                reverse_label = "neg"
            else:
                label = "neu"
                reverse_label = "neu"
            del words[len(words) - 1]
            words = self.clean_words(words)
            feature_set.append((self.create_feature_set(words)[0], label))
            feature_set.append((self.create_feature_set(words)[1], reverse_label))
        print (len(feature_set))
        #
        print "Feature set created. !"
        random.shuffle(feature_set)
        #feature_set += self.twitter_data_training()
        # feature_set += self.moviereview_data_training()
        training_set = feature_set[:3500]
        testing_set = feature_set[3500:]
        testing_set = training_set;
        print "Training..."
        print (training_set)
        print feature_set

        classifier = nltk.classify.NaiveBayesClassifier.train(training_set)

        file = open(self.naive_base_model, 'wb')
        pickle.dump(classifier, file)
        file.close()


        # print "Accuracy:" + str(nltk.classify.accuracy(classifier, testing_set))
        words = wordpunct_tokenize("hi, it bad is a very  very bad")
        print classifier.classify(self.create_feature_set(words)[0])
jam = JAM()

jam.create_feature_words_pickle()

jam.create_naive_bayes_model_pickle()
#jam.create_feature_set()