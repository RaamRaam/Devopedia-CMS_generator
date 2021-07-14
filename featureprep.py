from libraries import *
from data_object import *
from functions import *
from feature_functions import *


#Enter train/test author/title/yop csv path

if __name__ == "__main__":
    df_name=input("Enter dataset path:\t")
    df=pd.read_csv(df_name)
    print(len(df),df.columns)
    df=add_columns(df)
    df=df[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper','Author_Encoded']]
    df.to_csv(f'features_{df_name}',index=False)