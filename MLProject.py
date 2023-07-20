import re  #for regular expression.
import streamlit as st #for interface.

#NLTK Packages
import nltk #natural language toolkit - works on the frequency.
from nltk.corpus import stopwords #common words - a, an, the etc.
from nltk.tokenize import word_tokenize, sent_tokenize  #for tokenizing sentences into individual tokens.

#SPACY Packages
import spacy #works with meanings and frequency.
from spacy.lang.en.stop_words import STOP_WORDS #common words - a, an, the etc.

#Function for NLTK
def nltk_summarizer(docx): 
    stopWords = set(stopwords.words("english")) #language is specified as English.
    words = word_tokenize(docx)   #convert sentences into individual tokens.
    freqTable = dict() #map values to the dictionary data structure.

    for word in words:  #iterate through words.
        word = word.lower()   #change into lowercase.
        if word not in stopWords: #check if it a stopword.
            if word in freqTable: #check if it's already added in frequency table.
                freqTable[word] += 1 #add it in.
            else:
                freqTable[word] = 1

    sentence_list= sent_tokenize(docx)   #tokenize the document.
    sentenceValue = dict() #create dictionay that maps each word to its frequency.
    max_freq = max(freqTable.values()) #find maximium frequency in dict().
    for word in freqTable.keys(): #iterate through words
        freqTable[word] = (freqTable[word]/max_freq)  #relative frequency - similar to normalizing.

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()): #tokens in lowercase from above mentioned function.
            if word in freqTable.keys(): #if word exists in frquency table.
                if len(sent.split(' ')) < 30: #if sentence is shorter than 30 words.
                    if sent not in sentence_scores.keys(): #if sentence is in scores dictionary.
                        sentence_scores[sent] = freqTable[word] #add the sentence score to the frequency table.
                    else:
                        sentence_scores[sent] += freqTable[word] #add to the total number of length of words.

    import heapq #heap library.
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get) #nlargest is heapq function that is used to find top n elements in a list. Here we find top 8 sentences with the highest scores.
    summary = ' '.join(summary_sentences) #join sentences together.
    return summary

#Function for SPACY
def spacy_summarizer(article_text):
    nlp=spacy.load('en_core_web_lg') #training model of SpaCy.
    docx = nlp(article_text) #create a document object from input text. nlp() takes string as input and returns a Doc object.

    # Get the text of the Doc object
    text = docx.text
    # Tokenize the text
    words = word_tokenize(text)

    stopWords = list(STOP_WORDS) #creates a list of stop_words.

    # Create a dictionary of words and their frequencies.
    freqTable = dict() #create dictionay that maps each word to its frequency.
    for word in words:
        word = word.lower()
        if word not in stopWords: #If it's a stopword, skip over it.
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

    sentence_list= sent_tokenize(text) 
    sentenceValue = dict()
    max_freq = max(freqTable.values()) #freqTable.values() to find sentences with the highest frqencies.
    for word in freqTable.keys(): #to gwt the word in the sentences.
        freqTable[word] = (freqTable[word]/max_freq) #normalize the frequency.

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freqTable.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = freqTable[word]
                    else:
                        sentence_scores[sent] += freqTable[word] #total number of length of words.

    import heapq
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

def main():
    st.title("Text Summarizer App")
    activities = ["Summarize Via Text"]
    choice = st.sidebar.selectbox("Select Activity", activities)

    if choice == 'Summarize Via Text':
        st.subheader("Summary using NLP")
        article_text = st.text_area("Enter Text Here","Type here")
        #cleaning of input text.
        article_text = re.sub('\\[[0-9]*\\]', ' ',article_text) #any letter enclosed in brackets and is a number.
        article_text = re.sub('[^a-zA-Z.,]', ' ',article_text) #any text that's not a letter.
        article_text = re.sub(r"\b[a-zA-Z]\b",'',article_text) #any character surrounded by whitespace.
        article_text = re.sub("[A-Z]\Z",'',article_text) #any uppercase letter in the end of the text.
        article_text = re.sub(r'\s+', ' ', article_text) #whitespace character.

        summary_choice = st.selectbox("Summary Choice" , ["NLTK","SPACY"])
        if st.button("Summarize Via Text"):
            if summary_choice == 'NLTK':
                summary_result = nltk_summarizer(article_text)
            elif summary_choice == 'SPACY':
                summary_result = spacy_summarizer(article_text)

            st.write(summary_result)


if __name__=='__main__':
	main()
