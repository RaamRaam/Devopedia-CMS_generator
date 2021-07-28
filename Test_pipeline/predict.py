from libraries import *
import pickle
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import en_core_web_sm
nlp = en_core_web_sm.load()
from tensorflow.keras.models import load_model

def spacy_ner(text):
    doc = nlp(str(text))
    return doc.ents


def preds(field,df):
    data=df[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper',f'Tag_weights_{field}']]
    model_path=str(sys.argv[2])
    model=load_model(f'{field}_{model_path}')
    y_preds = model.predict(data)
    
    with open('train_thresholds.pkl','rb') as f:
        thresholds=pickle.load(f)
    predicted_categories = np.where(y_preds > thresholds[f'{field}'], 1, 0)
    
    df[f'{field}_preds']=predicted_categories
    df[f'{field}_pred_probs']=y_preds

    if field=='author':
        df_ner=df[df.author_preds==1]
        x=df_ner['text'].apply(lambda x : 1 if spacy_ner(x) else 0)
        df['Preds_ner']=x
        df.Preds_ner.fillna(df.author_preds, inplace=True)
        df['Preds_ner']=df['Preds_ner'].astype('int')
        df['author_preds']=df['Preds_ner']
        del df['Preds_ner']


if __name__ == "__main__":

    print("\npredcit.py running...\n\n")
    start_t=time.perf_counter()
    
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    df_path=cmdline_params['file_df_features']
    df=pd.read_csv(df_path)
    
    fields=['author','title','yop']
    
    _=[preds(field,df) for field in fields]
    

    df.to_csv('Predictions.csv',index=False)

    end_t=time.perf_counter()
    print(f"Program completed running in {end_t-start_t} seconds!\n")

