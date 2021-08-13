from os import startfile
from libraries import *
from cosine_similarity import cosine_similarity_value

def cosine_simi(df,field):       #return key of a dictionary having a certain value
    def get_key(val,dicto):
        for key, value in dicto.items():
             if val == value:
                return key
            
    max_score_pred=[]
    max_score_text=[]
    
    for _,i in tqdm(df.iterrows()):
        scores_dict={'p1':0,'p2':0,'p3':0}
        
        for j in range(1,4):
            try:
                scores_dict[f'p{j}']=cosine_similarity_value(i[f'p{j}'],i[f'{field}'])
            except:
                continue
        max_score=max(scores_dict.values())
        max_index=get_key(max_score,scores_dict)
                
        max_score_pred.append(max_score)
        max_score_text.append(i[max_index])
        
    df['max_similarity_score']=max_score_pred
    df['max_similarity_pred']=max_score_text

    return df


def aggregate(field,train_or_test,criterion):
    df=pd.read_csv(cmdline_params[f'{field}_{train_or_test}_{criterion}_similarities'])

    
    columns=['fname',f'{field}','p1','p2','p3']
    df_all=pd.DataFrame(columns=columns)
    fnames=df.fname.unique()

    for i in tqdm(fnames):
        df_temp=df[df.fname==i]
        dicto={'fname':None,f'{field}':None,'p1':None,'p2':None,'p3':None}

        preds=list(df_temp[f'pred_{field}'])
        dicto['fname']=i
        dicto[f'{field}']=df_temp.iloc[0][f'{field}']

        for j in range(1,4):
            try:
                dicto[f'p{j}']=preds[j-1]
            except:
                dicto[f'p{j}']=None

        df_all=df_all.append(dicto,ignore_index=True)

    df_all=cosine_simi(df_all,field)

    df_all.to_csv(os.path.join(folder_path,f"Aggregated_{field}_{train_or_test}_{criterion}.csv"),index=False)


    

if __name__=='__main__':
    print("Running aggregated_cosine_similarity.py...")
    start_t=time.perf_counter()
    folder_path='Train_diagnostics'
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    fields=['Author','Title','YoP']
    for field in fields:
        aggregate(field,'test','indices')
        aggregate(field,'test','probs')
        aggregate(field,'train','indices')
        aggregate(field,'train','probs')

    end_t=time.perf_counter()

    print(f"Program ran in {(end_t-start_t)/60} minutes.")


    


