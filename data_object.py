from libraries import *

class dataprep(object):
    def __init__(self,cmdline_params):
        self.html_path=cmdline_params['html_path']
        self.articles=cmdline_params['articles']
        self.meta_data=cmdline_params['meta_data']
        
    def get_ref_strings(self):
        articles = pd.read_json(self.articles, orient='index').drop(['alias','version'],axis=1)[['secs']]
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
        return pd.DataFrame.from_dict(dicto).drop_duplicates(subset='url', keep="last")
    
    def get_meta_data(self):
        fnames = pd.read_json(self.meta_data, lines=True)
        fnames.rename(columns = {'req_url':'url'}, inplace = True)
        return fnames[(fnames['type'].notnull()) & (fnames['type'].str.contains('html'))][['fname','url']]
    
        
