from feature_functions import *
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import os
import re
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from tensorflow.keras.models import load_model


def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


if __name__=="__main__":

    url=input("Enter URL:\t")
    r = requests.get(url, allow_redirects=True)
    # filename = getFilename_fromCd(r.headers.get('content-disposition'))
    open('LOL.html', 'wb').write(r.content)

    source=requests.get(url).text
    soup=BeautifulSoup(source)
    tag_list,text_list=tag_text_extractor(soup)
    SerialNo_col=np.arange(1,len(tag_list)+1)
    df = pd.DataFrame(list(zip(SerialNo_col,tag_list, text_list)),columns =['index','Tag', 'text'])

    df=add_columns(df)
    X=df[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper']]

    model=load_model('ANN_author')
    y_preds = model.predict(X)

    df['preds']=y_preds
    x=np.argmax(y_preds)
    print(df.text[x])

    df.to_csv('lol2.csv',index=False)



