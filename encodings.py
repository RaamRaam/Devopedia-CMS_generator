from libraries import *
from data_object import *
from functions import *
import warnings
warnings.filterwarnings('ignore')

start_t=time.perf_counter()

# Enter the raw dataset path
df=input("Enter df path:\t")
df=pd.read_csv(df)

print('processing Author Encodings ...')
author_df=get_encoded_df(df,'Author')
author_df.to_csv('author.csv',index=False)

print('processing Title Encodings ...')
title_df=get_encoded_df(df,'Title')
title_df.to_csv('title.csv',index=False)

print('processing YoP Encodings ...')
yop_df=get_encoded_df(df,'YoP')
yop_df.to_csv('yop.csv',index=False)

#If I don't load the following dataframes again, the _encoded.csv s will contain duplicate label columns. Quite fascinating

author_df=pd.read_csv('author.csv')
title_df=pd.read_csv('title.csv')
yop_df=pd.read_csv('yop.csv')


author_encoded=pd.merge(df, author_df, on=['index', 'fname'],how='inner')
author_encoded.to_csv('Author_encoded.csv',index=False)

title_encoded=pd.merge(df, title_df, on=['index', 'fname'],how='inner')
title_encoded.to_csv('Title_encoded.csv',index=False)

yop_encoded=pd.merge(df, yop_df, on=['index', 'fname'],how='inner')
yop_encoded.to_csv('YoP_encoded.csv',index=False)

end_t=time.perf_counter()

print(f"Encodings done in {(end_t-start_t)/60} minutes")





