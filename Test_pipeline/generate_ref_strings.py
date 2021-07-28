from libraries import pd,reader,sys

def ref_string_generate(author,title,yop):
    return author+'. '+yop+'. "'+title+'"'

def print_entities(field_list):
    for i in field_list:
        print(i)


def entities_extraction(df_author,df_title,df_yop):
    author_preds=list(df_author.head(3).text)
    title_preds=list(df_title.head(3).text)
    yop_preds=list(df_yop.head(3).text)

    print("\nBased on top 3 indices:\n\n")
    print("Authors:\n")
    print_entities(author_preds)
    print("\n\nTitles:\n")
    print_entities(title_preds)
    print("\n\nYoPs:\n")
    print_entities(yop_preds)

    ref_strings_top3_indices=[]
    for i in range(3):
        ref_strings_top3_indices.append(ref_string_generate(author_preds[i],title_preds[i],yop_preds[i]))

    print("\n\n Ref_strings from top 3 indices :\n")
    print_entities(ref_strings_top3_indices)

    df_author=df_author.sort_values(by = 'author_pred_probs',ascending=False)
    df_title=df_title.sort_values(by = 'title_pred_probs',ascending=False)
    df_yop=df_yop.sort_values(by = 'yop_pred_probs',ascending=False)

    author_preds=list(df_author.head(3).text)
    title_preds=list(df_title.head(3).text)
    yop_preds=list(df_yop.head(3).text)

    print('-'*200)

    print("Based on top 3 prediction probabilities:\n\n")
    print("Authors:\n")
    print_entities(author_preds)
    print("\n\nTitles:\n")
    print_entities(title_preds)
    print("\n\nYoPs:\n")
    print_entities(yop_preds)

    ref_strings_top3_probs=[]
    for i in range(3):
        ref_strings_top3_probs.append(ref_string_generate(author_preds[i],title_preds[i],yop_preds[i]))

    print("\n\n Ref_strings from top 3 predcition_probabilities :\n")
    print_entities(ref_strings_top3_probs)






if __name__=="__main__":
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    df_path=cmdline_params['preds_file']
    df=pd.read_csv(df_path)[['index','tag','text',
                                  'author_preds','author_pred_probs',
                                  'title_preds','title_pred_probs',
                                  'yop_preds','yop_pred_probs']]

    df_author=df[['index','tag','text','author_preds','author_pred_probs']][df.author_preds==1]
    df_title=df[['index','tag','text','title_preds','title_pred_probs']][df.title_preds==1]
    df_yop=df[['index','tag','text','yop_preds','yop_pred_probs']][df.yop_preds==1]

    entities_extraction(df_author,df_title,df_yop)

