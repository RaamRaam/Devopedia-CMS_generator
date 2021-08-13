from libraries import *
from data_object import *
from functions import *
import random


#Enter author/title/yop encoded csv path

def train_test_split(df,field):
    folder_path='Train_preprocess'
    fnames=list(df.fname.unique())
    test_split=random.sample(fnames,587)           # Randomly choose 587 files 

    df_test= df[df.fname.isin(test_split)]         # Create subset of dataframe w.r.t to test_split having 587 random files
    df_test.reset_index(inplace=True,drop=True)
    
    df_test.to_csv(os.path.join(folder_path,f'test_features_{field}_encoded.csv'),index=False)
    print('Test dataframe created!')

    df_train=df[~df.fname.isin(test_split)]          #Dataframe with rest of the files
    df_train.reset_index(inplace=True,drop=True)
    df_train.to_csv(os.path.join(folder_path,f'train_features_{field}_encoded.csv'),index=False)
    print('Train dataframe created!')

if __name__=='__main__':
    print("Split.py running...\n\n")
    start=time.perf_counter()

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    df_name=cmdline_params['features_author_encoded']
    df=pd.read_csv(df_name)
    train_test_split(df,'Author')
    print('Author split done!')

    df_name=cmdline_params['features_title_encoded']
    df=pd.read_csv(df_name)
    train_test_split(df,'Title')
    print('Title split done!')

    df_name=cmdline_params['features_yop_encoded']
    df=pd.read_csv(df_name)
    train_test_split(df,'YoP')
    print('YoP split done!')

    end=time.perf_counter()

    print(f"Splitting done in {end-start} seconds!\n")
