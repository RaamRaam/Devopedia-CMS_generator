from libraries import *
from data_object import *
from functions import *
import random


#Enter author/title/yop encoded csv path

def train_test_split(df,df_name):
    fnames=list(df.fname.unique())
    test_split=random.sample(fnames,587)

    df_test= df[df.fname.isin(test_split)]
    df_test.reset_index(inplace=True,drop=True)
    df_test=df_test[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper','Author_Encoded']]
    df_test.to_csv(f'test_{df_name}',index=False)
    print('Test dataframe created!')

    df_train=df[~df.fname.isin(test_split)]
    df_train.reset_index(inplace=True,drop=True)
    df_train=df_train[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper','Author_Encoded']]
    df_train.to_csv(f'train_{df_name}',index=False)
    print('Train dataframe created!')

if __name__=='__main__':
    print("Split.py running...\n\n")
    start=time.perf_counter()

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    df_name=cmdline_params['features_author_encoded']
    df=pd.read_csv(df_name)
    train_test_split(df,df_name)

    end=time.perf_counter()

    print(f"Splitting done in {end-start} seconds!\n")
