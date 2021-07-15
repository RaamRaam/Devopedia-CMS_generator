from libraries import *
from data_object import *
from functions import *
import warnings
warnings.filterwarnings('ignore')


def encoding_creation(temp_df,name):
    z_df=get_encoded_df(temp_df,name)
    z_df.to_csv(f'{name}.csv',index=False)
    print(f'{name} encodings completed!\n')
    return z_df


if __name__=="__main__":

    print("Running encodings.py...\n\n")
    start_t=time.perf_counter()

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    # df=input("Enter df path:\t")
    df=pd.read_csv(cmdline_params['raw_dataset'])
    

    temp_df = df.copy(deep=True)

    names=['Author','Title','YoP']

    create_encodings=functools.partial(encoding_creation,temp_df=temp_df)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        result_dfs=[executor.submit(encoding_creation,temp_df,name) for name in names]

    print(result_dfs)

    # print('processing Author Encodings ...')
    # author_df=get_encoded_df(temp_df,'Author')
    # author_df.to_csv('author.csv',index=False)

    # print('processing Title Encodings ...')
    # title_df=get_encoded_df(temp_df,'Title')
    # title_df.to_csv('title.csv',index=False)

    # print('processing YoP Encodings ...')
    # yop_df=get_encoded_df(temp_df,'YoP')
    # yop_df.to_csv('yop.csv',index=False)

    author_df=pd.read_csv("Author.csv")
    title_df=pd.read_csv("Title.csv")
    yop_df=pd.read_csv("YoP.csv")

 
  
    author_encoded=pd.merge(author_df,df, on=['index', 'fname'],how='left')
    author_encoded.to_csv('Author_encoded.csv',index=False)


    title_encoded=pd.merge(title_df,temp_df,on=['index', 'fname'],how='left')
    title_encoded.to_csv('Title_encoded.csv',index=False)
 
    yop_encoded=pd.merge(yop_df,temp_df, on=['index', 'fname'],how='left')
    yop_encoded.to_csv('YoP_encoded.csv',index=False)

    end_t=time.perf_counter()

    print(f"Encodings done in {(end_t-start_t)/60} minutes")







