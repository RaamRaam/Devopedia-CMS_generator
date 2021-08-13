from libraries import *
import pickle
import swifter



# with open('wordlist.pkl','rb') as f:
#         wordlist=pickle.load(f)
# print(f"Wordlist length:{len(wordlist)}")

# common_words=lambda word: 1 if word in wordlist else 0
# text_to_vector = lambda el: re.compile(r'[^\W]+\b').findall(str(el).lower())

# def common_words_count(text):
#     text=str(text)
#     tokens=text_to_vector(text)
#     count=list(map(common_words,tokens))
#     return sum(count)


def token_list_create(text):
    token_list=re.findall(r'\w+', text)        
    return token_list              #returns list of tokens from text


def no_of_tokens(text):
    text=str(text)
    return len(token_list_create(text))       #returns length of token list


def caps(text):
    text=str(text)
    return len(re.findall(r'[A-Z]',text))           #returns the total number of capital letters in the text (A-Z)

def first_token_upper(text):
    text=str(text)
    try:
        if text.split()[0].isupper():            #Returns 1 if first token of text are all capital letters else 0
            return 1
        else:
            return 0
    except:
        return 0

def comma_percent(text):
    text=str(text)
    try:
        return text.count(',')/no_of_tokens(text)    #Returns the number of commas  in the text
    except:
        return 0


def first_letter_upper(text):
    text=str(text)
    token_list=token_list_create(text)
    no_toks=no_of_tokens(text)
    try:
        return len([x for x in token_list if x[0].isupper()])/no_toks   #Returns number of tokens in text having 1st letter uppercase
    except:
        return 0

def year_in_string(text):
    text=str(text)
    x=re.search(r'\b\d{4}\b',str(text))                 #Returns 1 if a 4-digit number starting with 1 or 2 is detected in the text else 0
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
    # df['common_words_count']=df.text.swifter.apply(common_words_count) #too slow
    df['year_presence']=df.text.apply(year_in_string)

    return df             # returns dataframe having all features

def featureprep_func(field):
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    print(f"{field}")
    df=pd.read_csv(cmdline_params[f'{field}_encoded'])
    df=add_columns(df)
    folder_path='Train_preprocess'
    df.to_csv(os.path.join(folder_path,f'features_{field}_encoded.csv'),index=False)
    print(f"\nFeature columns added for {field}!\n")


if __name__ == "__main__":
    print("Featureprep.py running...\n\n")
    start=time.perf_counter()
    

    fields=['author','title','yop']
    with concurrent.futures.ProcessPoolExecutor() as exc:    #parallel processing
        _=[exc.submit(featureprep_func,field) for field in fields]

    print(_)

    end=time.perf_counter()
    
    print(f"Featureprep ran in {end-start} seconds!\n")