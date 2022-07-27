from tensorflow.keras.models import load_model
import pickle
import re
import numpy as np
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Lambda
from sklearn.metrics.pairwise import cosine_similarity
from .models import Book
# Create your views here.

def preprocess(description):
	stop_words = set(stopwords.words('english'))
	desc = re.sub('[^A-Za-z]+',' ',description)
	desc = desc.lower()
	#remove newlines and whitelines
	desc = re.sub('\n|\r',' ',desc)
	desc = ' '.join([i for i in desc.split(' ') if i not in stop_words])
	with open('blog/utils/tokenizer.pkl','rb') as f:
		tokenizer = pickle.load(f)
	sequences = tokenizer.texts_to_sequences([desc])
	x = pad_sequences(sequences,maxlen=100,padding='post')
	return x
def EmbeddModel(maxlen,emb_matrix_path):
	with open(emb_matrix_path,'rb') as f:
		emb_matrix = pickle.load(f)
	model = Sequential()
	model.add(Embedding(input_dim=emb_matrix.shape[0], output_dim=emb_matrix.shape[1], input_length=maxlen , weights=[emb_matrix]))
	# Average the output of the Embedding layer over the word dimension
	model.add(Lambda(lambda x: tf.keras.backend.mean(x, axis=1)))
	return model

def predict(description):
	x = preprocess(description)
	classifier = load_model('blog/utils/classifier.h5')
	embedder = EmbeddModel(100,'blog/utils/emb_matrix.pkl')
	embedding = list(embedder.predict(x)[0])
	prediction = classifier.predict(x)
	it_or_not = ['IT','Not']
	prediction = it_or_not[np.argmax(prediction)]
	return prediction,embedding

def similars(embedding):

	isbns = np.asarray([i.ISBN for i in Book.objects.all()])
	all_embeddings = np.array([i.embedding for i in Book.objects.all()])
	indices =  np.argsort(cosine_similarity(np.asarray(embedding, dtype=float).reshape(1,-1), all_embeddings))[0][::-1]
	similar = ' '.join([i for i in isbns[indices[1:9]]])

	return similar

