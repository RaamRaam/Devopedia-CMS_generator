from libraries import *
from functions import *
from featureprep import add_columns
from additional_featureprep import add_features,log_index_weightage
from predict import preds
from generate_ref_strings import entities_extraction
import warnings
warnings.filterwarnings("ignore")

if __name__=="__main__":

    start_t=time.perf_counter()
    folder_path="Prediction_outputs"
    try:
        os.mkdir(folder_path)
    except:
        pass
    #---------------------------------------------url2file---------------------------------------------

    url=str(sys.argv[1])
    source=requests.get(url).text
    try:
        with open(os.path.join(folder_path,'file.htm'),'w',encoding='utf8') as f:
            f.write(source)
    except:
        with open('file.htm','w',encoding='iso-8859-1') as f:
            f.write(source)

    
    
    #------------------------------------------dataprep---------------------------------------------------

    print("Extracting tags and texts from html file...\n")
    get_df=lambda el: create_df(el,filter(check_first_char,
                                          filter(exclude_texts,
                                                filter(exclude_tags,
                                                        extract_bs(el)
                                                    )
                                                )
                                          )
                                ).drop(['fname','text4dup'], axis = 1)

    file=os.path.join(folder_path,'file.htm')
    df=get_df(file)
    print(f"Dataframe of shape {df.shape} created.")

    #------------------------------------------featureaprep and additional_featureprep---------------------------------------------------

    df=add_columns(df)
    df['index']=df['index'].apply(log_index_weightage)
    fields=['author','title','yop']
    for field in fields:
        add_features(field,df)

    #------------------------------------------------prediction and ref_string generation----------------------------------------------

    _=[preds(field,df) for field in fields]

    df.to_csv(os.path.join(folder_path,"Prediction_diagnostics.csv"),index=False)

    df=df[['index','tag','text',
            'author_preds','author_pred_probs',
            'title_preds','title_pred_probs',
            'yop_preds','yop_pred_probs']]

    df_author=df[['index','tag','text','author_preds','author_pred_probs']][df.author_preds==1]
    df_title=df[['index','tag','text','title_preds','title_pred_probs']][df.title_preds==1]
    df_yop=df[['index','tag','text','yop_preds','yop_pred_probs']][df.yop_preds==1]

    entities_extraction(df_author,df_title,df_yop)

    end_t=time.perf_counter()
    print(f"\n\nPipeline ran in {end_t-start_t} seconds!\n")


    
        