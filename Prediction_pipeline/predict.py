from libraries import *
import pickle
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

from tensorflow.keras.models import load_model
# import en_core_web_sm
# nlp = en_core_web_sm.load()


# def spacy_ner(text):
#     doc = nlp(str(text))
#     return doc.ents


def preds(field,df):
    data=df[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper',
            'year_presence',f'Tag_weights_{field}']]
    model_path=str(sys.argv[2])
    models_folder_path='Models'
    model=load_model(os.path.join(models_folder_path,f'{field}_{model_path}'))           
    y_preds = model.predict(data)
    
    with open('train_thresholds.pkl','rb') as f:
        thresholds=pickle.load(f)                            #using best thresholds generated during Train Pipeline predictions
    predicted_categories = np.where(y_preds > thresholds[f'{field}'], 1, 0)
    
    df[f'{field}_preds']=predicted_categories
    df[f'{field}_pred_probs']=y_preds

    if field=='author':
        with open('author_stopwords.pkl','rb') as f:
            stopwords=pickle.load(f)

        text_to_vector = lambda el: re.compile(r'[^\W]+\b').findall(str(el).lower())

        for index,i in df.iterrows():
            token_list=text_to_vector(i['text'])
            if any(item in stopwords for item in token_list) or re.sub(' ','',i['text']).isdigit():
                df.loc[index,f'{field}_preds']=0
                df.loc[index,f'{field}_pred_probs']=0

    # if field=='author':
    #     df_ner=df[df.author_preds==1]
    #     x=df_ner['text'].apply(lambda x : 1 if spacy_ner(x) else 0)
    #     df['Preds_ner']=x
    #     df.Preds_ner.fillna(df.author_preds, inplace=True)
    #     df['Preds_ner']=df['Preds_ner'].astype('int')
    #     df['author_preds']=df['Preds_ner']
    #     del df['Preds_ner']


if __name__ == "__main__":

    print("\npredcit.py running...\n\n")
    start_t=time.perf_counter()
    
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    df_path=cmdline_params['file_df_features']
    df=pd.read_csv(df_path)
    
    fields=['author','title','yop']
    
    _=[preds(field,df) for field in fields]
    
    folder_path='Prediction_outputs'
    df.to_csv(os.path.join(folder_path,'Predictions.csv'),index=False)

    end_t=time.perf_counter()
    print(f"Program completed running in {end_t-start_t} seconds!\n")

