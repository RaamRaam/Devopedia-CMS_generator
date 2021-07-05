import os
import pandas as pd
import re
from tqdm import tqdm
from bs4 import BeautifulSoup as BS

Reference_details=pd.read_csv('Reference_details.csv')
files=list(Reference_details['fname'])

html_path=r'C:\Users\Saranga\Desktop\Devopedia\Work\articleRefs.v2525\html_output'
csv_file_outputs_dir=r'C:\Users\Saranga\Desktop\Devopedia\Work\Devopedia\csv_outputs_from_HTML3'


ignore_tags=['script','meta','link','button','svg','img','style','code','nav','figure']



text_special_char_check=re.compile('[^a-zA-Z0-9"]')
tag_special_char_check=re.compile('[^a-zA-Z0-9]')
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
            with open(os.path.join(html_path,f_name),encoding='iso-8859-1') as f:             
                file=f.read()
                soup=BS(file)

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

