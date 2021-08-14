from libraries import pd,reader,sys,re,os

def ref_string_generate(author,title,yop):
    return author+'. '+yop+'. "'+title+'"'

def print_entities(field_list,f):
    for i in field_list:
        print(i)
        f.write(i)
        f.write("\n")


def entities_extraction(df_author,df_title,df_yop):
    author_preds=list(df_author.head(3).text)
    title_preds=list(df_title.head(3).text)
    yop_preds=list(df_yop.head(3).text)

    for i in range(len(yop_preds)):
        try:
            yop_preds[i]=re.search(r'\b\d{4}\b',yop_preds[i]).group()    #printing first 4-digit number 
        except:
            pass

    remove_suffix=lambda el: re.search(r'([^|-]+)',el).group().strip()     # Considering part of text before - or |
    title_preds=list(map(remove_suffix,title_preds))

    folder_path='Prediction_outputs'
    f=open(os.path.join(folder_path,'Predicted_results.txt'),'w',encoding='utf-8')
    f.write("Predicted Results:\n\n\n")


    print("\nBased on top 3 indices:\n\n")
    f.write("\nBased on top 3 indices:\n\n")
    print("Authors:\n")
    f.write("Authors:\n\n")
    print_entities(author_preds,f)
    print("\n\nTitles:\n")
    f.write("\n\nTitles:\n\n")
    print_entities(title_preds,f)
    print("\n\nYoPs:\n")
    f.write("\n\nYoPs:\n\n")
    print_entities(yop_preds,f)


    range_top=min(len(author_preds),len(title_preds),len(yop_preds))

    ref_strings_top3_indices=[]
    for i in range(range_top):
        ref_strings_top3_indices.append(ref_string_generate(author_preds[i],title_preds[i],yop_preds[i]))

    print("\n\n Ref_strings from top 3 indices :\n")
    f.write("\n\n Ref_strings from top 3 indices :\n\n")
    print_entities(ref_strings_top3_indices,f)
    print("\n\n")
    f.write("\n\n")

    df_author=df_author.sort_values(by = 'author_pred_probs',ascending=False)
    df_title=df_title.sort_values(by = 'title_pred_probs',ascending=False)
    df_yop=df_yop.sort_values(by = 'yop_pred_probs',ascending=False)

    author_preds=list(df_author.head(3).text)
    title_preds=list(df_title.head(3).text)
    yop_preds=list(df_yop.head(3).text)

    for i in range(len(yop_preds)):
        try:
            yop_preds[i]=re.search(r'\b\d{4}\b',yop_preds[i]).group()  #printing first 4-digit number
        except:
            pass

    remove_suffix=lambda el: re.search(r'([^|-]+)',el).group().strip()     # Considering part of text before - or |
    title_preds=list(map(remove_suffix,title_preds))


    print('-'*200)
    f.write('-'*200)
    print("\n\n")
    f.write('\n\n')
    print("Based on top 3 prediction probabilities:\n\n")
    f.write("Based on top 3 prediction probabilities:\n\n")
    print("Authors:\n")
    f.write("Authors:\n\n")
    print_entities(author_preds,f)
    print("\n\nTitles:\n")
    f.write("\n\nTitles:\n\n")
    print_entities(title_preds,f)
    print("\n\nYoPs:\n")
    f.write("\n\nYoPs:\n\n")
    print_entities(yop_preds,f)

    range_top=min(len(author_preds),len(title_preds),len(yop_preds))

    ref_strings_top3_probs=[]
    for i in range(range_top):
        ref_strings_top3_probs.append(ref_string_generate(author_preds[i],title_preds[i],yop_preds[i]))

    print("\n\n Ref_strings from top 3 predcition_probabilities :\n")
    f.write("\n\n Ref_strings from top 3 predcition_probabilities :\n\n")
    print_entities(ref_strings_top3_probs,f)

    f.close()






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

