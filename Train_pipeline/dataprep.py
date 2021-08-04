from libraries import *
from data_object import *
from functions import *
import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":

    start_time=time.perf_counter()
    
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    dp=dataprep(cmdline_params)
    print('Processing Reference Strings ...')
    ref_strings=dp.get_ref_strings()
    meta_data=dp.get_meta_data()
    df=pd.merge(ref_strings,meta_data,on='url',how='inner')
    

    df['Author']=df['text'].apply(extract_author)
    df['YoP']=df['text'].apply(extract_year)
    df['Title']=df['text'].apply(extract_title)
    df['detail1']=df['text'].apply(detail1)
    df['detail2']=df['text'].apply(detail2)
    df=df[['fname','Author', 'YoP', 'Title', 'detail1', 'detail2']]

    df.to_csv('files_and_references.csv',index=False)
    print('Files and references dataset created!\n\n')
    

    batch_size = int(sys.argv[2])
    f_names=list(df['fname'])
    exclude_files=['2042bf742d6213f92eef06fef3bb92c7d6c78f8e546c37fb3f40ee922f6227af.htm',
                    'ae6c80683b52548619110b550f05c2803bb815ed2df57bc6ec732957ebc43329.htm',
                    'fe9c6a1bed67fa8fba9eaeca060077bca0d15b219f19adabb49c500a6eb8c77f.htm',
                    'fb64b9b6dc6a507b292702202601d216a737a3110e266effba5f17ef9512094e.htm']
    f_names=[x for x in f_names if x not in exclude_files]
    batches=[f_names[i:i + batch_size] for i in range(0, len(f_names), batch_size)]
    get_df=lambda el: create_df(el,filter(check_first_char,
                                          filter(exclude_texts,
                                                filter(exclude_tags,
                                                        extract_bs(os.path.join(cmdline_params['html_path'],el))
                                                    )
                                                )
                                          )
                                ).drop(['text4dup'], axis = 1)
    print('processing batches ...')
    for k,i in enumerate(batches):
        print('Batch: ',k+1, 'Run time:', end='')
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor() as exc:
                tmp_df=pd.merge(pd.concat(list(exc.map(get_df,i))),df,on='fname',how="left")
        final_df= tmp_df if k==0 else pd.concat([final_df,tmp_df])
        end = time.perf_counter()
        print(end - start)
        
    final_df=final_df[final_df.text.notnull()]

    final_df.to_csv('raw_dataset.csv',index=False)

    print(final_df.info())

    end_time=time.perf_counter()

    print(f"Program ran for {(end_time-start_time)/60} minutes")

