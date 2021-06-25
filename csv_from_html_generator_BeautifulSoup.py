import os
import pandas as pd
import re
from tqdm import tqdm
from bs4 import BeautifulSoup as BS

Reference_details=pd.read_csv('Reference_details.csv')
files=list(Reference_details['fname'])

html_path=r'C:\Users\Saranga\Desktop\Devopedia\Work\articleRefs.v2525\html_output'
csv_file_outputs_dir=r'C:\Users\Saranga\Desktop\Devopedia\Work\Devopedia\csv_outputs_from_HTML'

ignore_tags=['script','meta','link','button','svg','img','style','code','nav','figure']


error_count=0
error_indices=[]

for index,f_name in tqdm(enumerate(files)):
    
    tag_list=[]
    text_list=[]


    try:
        try:
            with open(os.path.join(html_path,f_name), encoding='utf8') as f:
                file=f.read()
                soup=BS(file)
        except:
            with open(os.path.join(html_path,f_name),encoding='iso-8859-1') as f:             #files which can be read using default encoding
                file=f.read()
                soup=BS(file)

        duplicates=set()

        for tag in soup.find_all():

            if tag.name in ignore_tags:
                continue

            text=re.sub('\n',' ',tag.text)
                                 

            text=re.sub('[^\w ]','',text)                   #No special characters allowed (done for authors while encoding also)
            text=text.strip()
            text=re.sub('\s+',' ',text)                       #Long white spaces replaced to single whie space
            
            if len(text)==0 or len(text)>500 or text.isspace():
                continue
            
#             if text_special_char_check.search(text[0]) is not None:
#                 continue


            if text not in duplicates:
                    tag_list.append(tag.name)
                    text_list.append(text)
                    duplicates.add(text)
        



        n_rows=len(tag_list)
        


        YoP=[Reference_details.YoP[index]]*n_rows
        Title=[Reference_details.title[index]]*n_rows
        Author=[Reference_details.Author[index]]*n_rows
        html_fname=[Reference_details.fname[index]]*n_rows

        dataframe=pd.DataFrame(list(zip(YoP,Title,Author,tag_list,text_list,html_fname)),
                               columns=['YoPublishing','Title','Author','Tag','Text','fname'])

        if dataframe.size==0:
            continue

        csv_file=os.path.join(csv_file_outputs_dir,f_name+'.csv')

        dataframe.to_csv(csv_file,index=False)
        
        
    except:
        error_count+=1
        error_indices.append(index)
        pass


print(f"{error_count} errors occurred")

