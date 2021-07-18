import pickle
from libraries import *

if __name__=='__main__':

    start_t=time.perf_counter()

    with open('tags_info.pkl','rb') as f:  
        tags_info = pickle.load(f)
    tags_with_author=tags_info['tags_with_author']
    tags_without_author=tags_info['tags_without_author']
    tag_weights=tags_info['tag_weights']

    log100=lambda x: math.log(x,100) if x!=0 else 0

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    df=pd.read_csv(cmdline_params['file_df_features'])
    


    df['index']=list(map(log100,(df['index'])))
    df['Tag_label']=df.tag.apply(lambda x: 1 if x in tags_with_author else( 0 if x in tags_without_author else -1))
    df['Tag_weights']=df.tag.apply(lambda x: tag_weights[x] if x in tag_weights else 0.0007)

    df.to_csv(cmdline_params['file_df_features'],index=False)

    end_t=time.perf_counter()
    print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")

