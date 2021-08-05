import pickle
from libraries import *

log_index_weightage=lambda x: 1/(math.exp(math.log(x+1,100)))
tag_weights_update=lambda x: ((x*100)**2)/10000

def add_features(field,df):
    with open(f'{field}_tags_info.pkl','rb') as f:  
        tags_info = pickle.load(f)                   #using tag_weights already calculated in Train Pipeline
    tag_weights=tags_info[f'tag_weights_{field}']

    df[f'Tag_weights_{field}']=df.tag.apply(lambda x: tag_weights[x] if x in tag_weights else 0.0001)
    df[f'Tag_weights_{field}']=df[f'Tag_weights_{field}'].apply(tag_weights_update)



if __name__=='__main__':

    start_t=time.perf_counter()

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    df=pd.read_csv(cmdline_params['file_df_features'])
    df['index']=df['index'].apply(log_index_weightage)
    
    fields=['author','title','yop']
    for field in fields:
        add_features(field,df)

    print("Tag_weight columns added!")

    df.to_csv(cmdline_params['file_df_features'],index=False)

    end_t=time.perf_counter()
    print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")

