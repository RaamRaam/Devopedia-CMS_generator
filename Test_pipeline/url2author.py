from feature_functions import *
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import os
import re
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
# from tensorflow.keras.models import load_model
# import urllib.request   
from functions import *
from libraries import * 







if __name__=="__main__":

    url=input("Enter URL:\t")
    # r = requests.get(url, allow_redirects=True)
    # # with open('file.txt', 'w') as file:
    # #     file.write(r.text)

    # urllib.request.urlretrieve(url, "file.htm")      

    source=requests.get(url).text
 
    try:
        with open('file.htm','w',encoding='utf8') as f:
            f.write(source)
    except:
        with open('file.htm','w',encoding='iso-8859-1') as f:
            f.write(source)


    # soup=BeautifulSoup(source)
    
    # tag_list,text_list=tag_text_extractor(soup)
    # SerialNo_col=np.arange(1,len(tag_list)+1)
    # df = pd.DataFrame(list(zip(SerialNo_col,tag_list, text_list)),columns =['index','Tag', 'text'])

    # df=add_columns(df)
    # X=df[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper']]

    # model_path=input("Enter model path:\t")
    # model=load_model(model_path)
    # y_preds = model.predict(X)

    # df['preds']=y_preds
    # x=np.argmax(y_preds)
    # print(df.text[x])

    # df.to_csv('url_tags_texts_preds.csv',index=False)



