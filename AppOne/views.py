from django.shortcuts import render
from AppOne.forms import *
import pickle
import os
import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('porter')
from nltk import PorterStemmer
ps=PorterStemmer()
from sklearn.feature_extraction.text import HashingVectorizer
from django.http import HttpResponse
from nltk.corpus import stopwords
# Create your views here.
def transfer(x):
        sw=stopwords.words('english')
        sp=string.punctuation
        x=x.lower()
        x=nltk.word_tokenize(x)
        y=[]
        for i in x:
            if i not in sw and i not in sp and i.isalnum():
                y.append(ps.stem(i))
        y=[" ".join(y)]
        hash_vector = HashingVectorizer(n_features=10000)  # Adjust the number of features as needed

        vector = hash_vector.fit_transform(y).toarray()
        return vector

def index(request): 
    result="  "

    model_path=os.path.join(os.path.dirname(__file__),"model.pkl")
    model=pickle.load(open(model_path,'rb'))
    form=UserForm()
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['Email']

        a=transfer(text)
        val=model.predict(a)
        
        if val==0:
             result="Not Spam its a ham"
        else:
             result="spam"
        
    return render(request,'AppOne/index.html',context={'form':UserForm,'result':result})
