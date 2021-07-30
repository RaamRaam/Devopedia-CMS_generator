from libraries import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cosine_similarity_value(string1,string2):
    documents=(string1,string2)
    tfidf_vectorizer=TfidfVectorizer()
    tfidf_matrix=tfidf_vectorizer.fit_transform(documents)

    cs=cosine_similarity(tfidf_matrix[0:1],tfidf_matrix)
    return cs[0][1]

def cosine_simi(df,field):
    scores=[]
    for i in tqdm(df.iterrows()):         
        scores.append(cosine_similarity_value(str(i[1][f'{field}']),str(i[1][f'pred_{field}'])))
    df[f'{field}_simi']=scores
    return df



def top_three_preds_indices(field,train_or_test):

    columns= ['index','fname','tag','text',f'{field}','Ground_truths','Predictions','Pred_proba']

    df=pd.read_csv(cmdline_params[f'{train_or_test}_{field}_pred'])[columns]
    columns.append(f'pred_{field}')

    df_all= pd.DataFrame(columns=columns)
    fnames=df.fname.unique()

    for i in tqdm(fnames):
        df_temp=df[df.fname==i][df.Predictions==1]
        field_preds=list(df_temp.head(3).text)
        
        df_temp=df_temp.head(3)
        df_temp[f'pred_{field}']=field_preds


        df_all=df_all.append(df_temp[columns],ignore_index=True)

    df_all=cosine_simi(df_all,field)

    df_all.to_csv(f'{field}_{train_or_test}_indices_similarities.csv',index=False)


def top_three_preds_probs(field,train_or_test):

    columns= ['index','fname','tag','text',f'{field}','Ground_truths','Predictions','Pred_proba']

    df=pd.read_csv(cmdline_params[f'{train_or_test}_{field}_pred'])[columns]
    columns.append(f'pred_{field}')

    df_all= pd.DataFrame(columns=columns)
    fnames=df.fname.unique()

    for i in tqdm(fnames):
        df_temp=df[df.fname==i]
        df_temp=df_temp.sort_values(by = 'Pred_proba',ascending=False)
        field_preds=list(df_temp.head(3).text)
        df_temp=df_temp.head(3)
        df_temp[f'pred_{field}']=field_preds
        df_all=df_all.append(df_temp[columns],ignore_index=True)


    df_all=cosine_simi(df_all,field)

    df_all.to_csv(f'{field}_{train_or_test}_probs_similarities.csv',index=False)

    


if __name__=="__main__":

    start_t=time.perf_counter()

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}

    fields=['Author','Title','YoP']

    print("Based on top 3 indices:\n")

    for field in fields:
        top_three_preds_indices(field,'train')
        top_three_preds_indices(field,'test')

    print("-------------------------------------------------------------------------------------------------")

    print("Based on top 3 probabilites:\n")
    for field in fields:
        top_three_preds_probs(field,'train')
        top_three_preds_probs(field,'test')


    end_t=time.perf_counter()

    print(f"Program ran in {(end_t-start_t)/60} minutes.")


    
