import warnings
warnings.filterwarnings("ignore")
import re
import concurrent.futures
import functools
import time
import numpy as np


def tag_text_extractor(soup):

    start_t=time.perf_counter()

    tag_list=[]
    text_list=[]
    text_special_char_check=re.compile('[^a-zA-Z0-9"]')
    tag_special_char_check=re.compile('[^a-zA-Z0-9]')   
    ignore_tags=['script','meta','link','button','svg','img','style','code','nav','figure']

    duplicates=set()

    for tag in soup.find_all():

        name=tag.name
        
        if name in ignore_tags or (tag_special_char_check.search(name)!=None): #exclude tags having special characters 
            continue

        text=tag.text
        
        
        text=text.strip() 

        if text=='':
            continue

        if text.startswith('https') or text.startswith('http') or text.startswith('Fig'):
            continue

        if text[0].isdigit():
            continue
        
        if text_special_char_check.search(text[0]) is not None: #exclude texts starting with a special char (except ")") 
                continue
                
        text=re.sub('\n',' ',tag.text)
                                            
        text=text.strip()
        text=re.sub('\s+',' ',text)                       #Long white spaces replaced to single whie space
        
        if len(text)==0 or len(text)>500 or text.isspace():
            continue
        
#             if text_special_char_check.search(text[0]) is not None:
#                 continue

        if text not in duplicates:
                tag_list.append(name)
                text_list.append(text)
                duplicates.add(text)

    end_t=time.perf_counter()
    print(f"Tags and text extracted in {end_t-start_t} seconds.")
    return tag_list,text_list
    

def extract_features(text,caps,first_token_upper,comma_percent,no_of_tokens,first_letter_upper):
    text=str(text)
    token_list=re.findall(r'\w+', text)
    no_toks = len(token_list)

    try:
      first_letter_upper.append(len([x for x in token_list if x[0].isupper()])/no_toks)
    except:
      first_letter_upper.append(0)

    x=len(re.findall(r'[A-Z]',text))
    caps.append(x)

    no_of_tokens.append(no_toks)
    
    try:
      comma_percent.append(text.count(',')/no_toks)
    except:
      comma_percent.append(0)
    
    try:
        if text.split()[0].isupper():
            first_token_upper.append(1)
        else:
            first_token_upper.append(0)
    except:
        first_token_upper.append(0)

def add_columns(df):
    print("Adding feature columns...`")

    caps=[]
    first_token_upper=[]
    comma_percent=[]
    no_of_tokens=[]
    first_letter_upper=[]

    t_start=time.perf_counter()

    add_feature_columns=functools.partial(extract_features,caps=caps,first_token_upper=first_token_upper,
                                         comma_percent=comma_percent,no_of_tokens=no_of_tokens,
                                         first_letter_upper=first_letter_upper)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(add_feature_columns, df.text)

    df['caps_count']=np.array(caps)
    df['first_token_upper']=np.array(first_token_upper)
    df['comma_percent']=np.array(comma_percent)
    df['No_of_tokens']=np.array(no_of_tokens)
    df['first_letter_upper']=np.array(first_letter_upper)

    t_end=time.perf_counter()

    print(f"Added columns in {t_end-t_start} seconds..")

    return df