import pandas as pd 
import numpy as np
import yake
from wordcloud import WordCloud
import matplotlib.pyplot as plt

text_in=pd.DataFrame()

text_in = pd.read_csv('C:/Users/Nicolas/Documents/Python/Projects/Python Project/Text - Cooling Pad/Cooling_Pad_NLP_document.csv')

text_in['Description']=text_in['Description'].astype(str)

descript =' '.join(text_in['Description'])

print(len(descript))


wordcloud_raw = WordCloud(background_color='white').generate(descript)
plt.imshow(wordcloud_raw, interpolation='bilinear')
plt.axis("off")
plt.title("Frequency of Words in Cooling Pad Description")
plt.show()

##Now let's try to use a keyword extractor, YAKE, to have a better understanding of what we are dealing with

language = "en"
max_ngram_size = 3
deduplication_threshold = 0.3
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 30


custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
keywords = custom_kw_extractor.extract_keywords(descript)

keywords = pd.DataFrame(keywords)

keywords.columns = ["Words","Freq"]


print(keywords['Words'])


plt.barh(keywords['Words'], keywords['Freq'])
plt.title('Keywords From Cooling Pad Descriptions')
plt.gca().invert_yaxis()
plt.show()


new_kw = ' '.join(keywords['Words'])


#now let's make a new wordcloud with these keywords extracted


wordcloud_finish = WordCloud(background_color='white').generate(new_kw)
plt.imshow(wordcloud_finish, interpolation='bilinear')
plt.title('Keywords From Cooling Pad Descriptions')
plt.show()





