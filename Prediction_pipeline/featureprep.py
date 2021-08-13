from libraries import *


#same as in train_pipeline

def token_list_create(text):
    token_list=re.findall(r'\w+', text)
    return token_list


def no_of_tokens(text):
    text=str(text)
    return len(token_list_create(text))


def caps(text):
    text=str(text)
    return len(re.findall(r'[A-Z]',text))

def first_token_upper(text):
    text=str(text)
    try:
        if text.split()[0].isupper():
            return 1
        else:
            return 0
    except:
        return 0

def comma_percent(text):
    text=str(text)
    try:
        return text.count(',')/no_of_tokens(text)
    except:
        return 0


def first_letter_upper(text):
    text=str(text)
    token_list=token_list_create(text)
    no_toks=no_of_tokens(text)
    try:
        return len([x for x in token_list if x[0].isupper()])/no_toks
    except:
        return 0

def year_in_string(text):
    text=str(text)
    x=re.search(r'\b\d{4}\b',str(text))
    if x:
        x=x.group()
        if x[0]=='1' or x[0]=='2':
            return 1
    return 0


def add_columns(df):
    df['caps_count']=df.text.apply(caps)
    df['first_token_upper']=df.text.apply(first_token_upper)
    df['comma_percent']=df.text.apply(comma_percent)
    df['No_of_tokens']=df.text.apply(no_of_tokens)
    df['first_letter_upper']=df.text.apply(first_letter_upper)
    df['year_presence']=df.text.apply(year_in_string)

    return df

def featureprep_func(df_name):
    df=pd.read_csv(df_name)
    df=add_columns(df)
    # df=df[['index','fname','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper','Author_Encoded']]
    df.to_csv(cmdline_params['file_df_features'],index=False)


if __name__ == "__main__":
    
    print("Featurepre.py running...\n\n")
    start=time.perf_counter()
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}

    featureprep_func(cmdline_params['file_df'])
    print("\nFeature columns added!\n")
        
    end=time.perf_counter()
    
    print(f"Featureprep ran in {end-start} seconds!\n")