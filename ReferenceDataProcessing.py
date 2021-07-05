import os
import pandas as pd
import re

articles = pd.read_json('devopediaArticles.v2525.json', orient='index').drop(['alias','version'],axis=1)[['secs']]
secs = articles['secs'].apply(pd.Series)[['References']]
dicto={'url':[],'text':[],'citeas':[]}
for item in secs.References:
    for i in item:
        try:
            dicto['url'].append(i['url'])
            dicto['citeas'].append(i['citeas'])
            dicto['text'].append(i['text'])
        except:
            continue
            
References=pd.DataFrame.from_dict(dicto)

print("Before removing Duplicates")
print(len(References['url']),len(References['url'].unique()))
print(len(References['text']),len(References['text'].unique()))
print(len(References['citeas']),len(References['citeas'].unique()))
References=References.drop_duplicates(subset='url', keep="last")
print("After removing Duplicates")
print(len(References['url']),len(References['url'].unique()))
print(len(References['text']),len(References['text'].unique()))
print(len(References['citeas']),len(References['citeas'].unique()))

#References.to_csv('RefStrings.csv',index=False)

fnames = pd.read_json('meta.v2525.jl', lines=True)
fnames = fnames[fnames['type'].notnull()]
fnames = fnames[fnames['type'].str.contains('html')][['fname','req_url']]
fnames.columns=['fname','url']
df=pd.merge(References,fnames,on='url',how='inner')

raw_labels=[]
for i,v in df.iterrows():
    valid_str=v['text'].split(' Accessed')[0]
    Author=re.split(' \d\d\d\d',valid_str)[0].replace('.','')
    year=re.search('\d\d\d\d',valid_str).group().replace('.','')
    title=re.search(r'\"(.+?)\"',valid_str).group().replace('.','') if re.search(r'\"(.+?)\"',valid_str) else ""
    detail=[x.strip().replace('.','') for x in re.split(r'\"(.+?)\"',valid_str)[-1].split(',')]
    detail1=", ".join(detail[:-1])
    detail2=detail[-1]
    raw_labels.append([v['fname'],Author,year,title.replace('"',''),detail1,detail2])
Reference_details = pd.DataFrame(raw_labels, columns = ['fname','Author', 'YoP', 'title', 'detail1', 'detail2'])    
Reference_details.reset_index(level=0, inplace=True)
Reference_details.drop('index',axis=1,inplace=True)
Reference_details.to_csv('Reference_details.csv',index=False)