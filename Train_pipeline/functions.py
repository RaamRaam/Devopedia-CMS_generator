from libraries import *
from functions import *


valid_str = lambda text: text.split(' Accessed')[0]
extract_author = lambda text: re.split(' \d\d\d\d',valid_str(text))[0].replace('.','')
extract_year = lambda text: re.search('\d\d\d\d',valid_str(text)).group().replace('.','')
extract_title=lambda text: re.search(r'\"(.+?)\"',valid_str(text)).group().replace('\"','') if re.search(r'\"(.+?)\"',valid_str(text)) else ""
other_details=lambda text: [x.strip().replace('.','') for x in re.split(r'\"(.+?)\"',text)[-1].split(',')]
detail1=lambda text: ", ".join(other_details(valid_str(text))[:-1])
detail2=lambda text: other_details(valid_str(text))[-1]

ignore_tags=['script','meta','link','button','svg','img','style','code','nav','figure']    
text_special_char_check=re.compile('[^a-zA-Z0-9"]')
tag_special_char_check=re.compile('[^a-zA-Z0-9]')

exclude_tags=lambda el: not any([el.name in ignore_tags, tag_special_char_check.search(el.name)!=None])
exclude_texts=lambda el: not any([ el.text.startswith(('http','Fig')),el.text.strip()=='', len(el.text)==0])
check_first_char=lambda el: not any([el.text[0].isdigit(), text_special_char_check.search(el.text[0]) is not None])
create_df=lambda f_name, el: pd.DataFrame([[index,f_name,i.name,
                   re.sub('\"','',re.sub('\s+',' ',re.sub('\n',' ',i.text.strip())))[:1000],
                   re.sub('\s+',' ',re.sub('\n',' ',i.text.lower().strip()))[:1000]] 
                  for index,i in enumerate(el)], 
                 columns=['index','fname','tag','text','text4dup']).drop_duplicates(subset='text4dup', keep="first")

text_to_vector = lambda el: re.compile(r'[^\W]+\b').findall(str(el).lower())
encoded_files = lambda el: list(el[el['Author_Encoded']!=0].fname.unique())
exact_match = lambda el: 1 if all([set(text_to_vector(el[0])).issubset(text_to_vector(el[1])),set(text_to_vector(el[1])).issubset(text_to_vector(el[0]))]) else 0
exact_text = lambda el: 1 if set(text_to_vector(el[0])).issubset(text_to_vector(el[1])) else 0
exact_label = lambda el: 1 if set(text_to_vector(el[1])).issubset(text_to_vector(el[0])) else 0
partial_match = lambda el: 1 if len(set(text_to_vector(el[1])).intersection(set(text_to_vector(el[0]))))/len(set(text_to_vector(el[0])))>0.5 else 0


def get_encoded_df(df,field):
    df0=df
    df0[field+'_Encoded']=df0[['text',field]].apply(exact_match, axis=1)
    df1=df0[~df0['fname'].isin(list(df0[df0[field+'_Encoded']==1].fname.unique()))]
    df1[field+'_Encoded']=df1[['text',field]].apply(exact_text, axis=1)
    df2=df1[~df1['fname'].isin(list(df1[df1[field+'_Encoded']==1].fname.unique()))]
    df2[field+'_Encoded']=df2[['text',field]].apply(exact_label, axis=1)
    df3=df2[~df2['fname'].isin(list(df2[df2[field+'_Encoded']==1].fname.unique()))]
    df3[field+'_Encoded']=df3[['text',field]].apply(partial_match, axis=1)
    return pd.concat([df0[df0['fname'].isin(list(df0[df0[field+'_Encoded']==1].fname.unique()))],
             df1[df1['fname'].isin(list(df1[df1[field+'_Encoded']==1].fname.unique()))],
             df2[df2['fname'].isin(list(df2[df2[field+'_Encoded']==1].fname.unique()))],
             df3[df3['fname'].isin(list(df3[df3[field+'_Encoded']==1].fname.unique()))]])[['index','fname',field+'_Encoded']]


def extract_bs(file):
    try:
        return BS(open(file,encoding='utf8').read()).find_all()
    except:
        return BS(open(file,encoding='iso-8859-1').read()).find_all()
