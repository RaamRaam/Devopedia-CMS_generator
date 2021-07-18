from libraries import *
import pickle


def check_tag_author_encoded(tag,ae,tags_with_author,tags_without_author_temp,tag_author_count_dict):
    if ae==1:
        tags_with_author.add(tag)
        if tag not in tag_author_count_dict:
            tag_author_count_dict[tag]= tag_author_count_dict.get(tag, 0) + 1
        else:
            tag_author_count_dict[tag]+=1
    else:
        tags_without_author_temp.add(tag)

log100=lambda x: math.log(x,100) if x!=0 else 0


if __name__=='__main__':

    print("additional_features_prep.py running...")
    start_t=time.perf_counter()

    tags_with_author=set()
    tags_without_author_temp=set()
    tag_author_count_dict=dict()

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    df_train=pd.read_csv(cmdline_params['df_train'])
    df_test=pd.read_csv(cmdline_params['df_test'])

    for i in range(len(df_train)):
        check_tag_author_encoded(df_train.tag[i],df_train.Author_Encoded[i],
                             tags_with_author,tags_without_author_temp,tag_author_count_dict)

    tags_without_author=tags_without_author_temp-tags_with_author

    tag_counts=Counter(df_train.tag)

    tag_weights=dict()
 
    for key,item in tag_author_count_dict.items(): 
        tag_weights[key]=item/tag_counts[key]

    tags_info={
        'tags_with_author':tags_with_author,
        'tags_without_author':tags_without_author,
        'tag_weights':tag_weights
    }
    with open(cmdline_params['tags_info'], 'wb') as f: 
        pickle.dump(tags_info, f)
    print("Tag_info stored!")

    df_train['index']=list(map(log100,(df_train['index'])))
    df_train['Tag_label']=df_train.tag.apply(lambda x: 1 if x in tags_with_author else 0)
    df_train['Tag_weights']=df_train.tag.apply(lambda x: tag_weights[x] if x in tag_weights else 0.0007)

    df_test['index']=list(map(log100,(df_test['index'])))
    df_test['Tag_label']=df_test.tag.apply(lambda x: 1 if x in tags_with_author else( 0 if x in tags_without_author else -1))
    df_test['Tag_weights']=df_test.tag.apply(lambda x: tag_weights[x] if x in tag_weights else 0.0007)

    df_train.to_csv(cmdline_params['df_train'],index=False)
    print("\nMore features added to train set!")
    df_test.to_csv(cmdline_params['df_test'],index=False)
    print("More features added to test set!")

    end_t=time.perf_counter()
    print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")

    


    
    

