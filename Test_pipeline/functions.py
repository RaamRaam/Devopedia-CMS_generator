from libraries import *
from functions import *


valid_str = lambda text: text.split(' Accessed')[0]

ignore_tags=['script','meta','link','button','svg','img','style','code','nav','figure']    
text_special_char_check=re.compile('[^a-zA-Z0-9"]')
tag_special_char_check=re.compile('[^a-zA-Z0-9]')

exclude_tags=lambda el: not any([el.name in ignore_tags, tag_special_char_check.search(el.name)!=None])
exclude_texts=lambda el: not any([ el.text.startswith(('http','Fig')),el.text.strip()=='', len(el.text)==0,len(el.text)>500])
check_first_char=lambda el: not any([el.text[0].isdigit(), text_special_char_check.search(el.text[0]) is not None])

create_df=lambda f_name, el: pd.DataFrame([[index,f_name,i.name,
                   re.sub('\"','',re.sub('\s+',' ',re.sub('\n',' ',i.text.strip()))),
                   re.sub('\s+',' ',re.sub('\n',' ',i.text.lower().strip()))] 
                  for index,i in enumerate(el)], 
                 columns=['index','fname','tag','text','text4dup']).drop_duplicates(subset='text4dup', keep="first")

def extract_bs(file):
    try:
        return BS(open(file,encoding='utf8').read()).find_all()
    except:
        return BS(open(file,encoding='iso-8859-1').read()).find_all()
