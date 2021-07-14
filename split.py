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
    df_test.to_csv(f'test_{df_name}',index=False)
    print('Test dataframe created!')

    df_train=df[~df.fname.isin(test_split)]
    df_train.reset_index(inplace=True,drop=True)
    df_train.to_csv(f'train_{df_name}',index=False)
    print('Train dataframe created!')

if __name__=='__main__':
    df_name=input("Enter df path:\t")
    df=pd.read_csv(df_name)
    train_test_split(df,df_name)
