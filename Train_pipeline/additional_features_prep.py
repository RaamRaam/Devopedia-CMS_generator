from libraries import *
import pickle


def check_tag_encoded(tag,ae,tags_with_field,tags_without_field_temp,tag_field_count_dict):
    if ae==1:
        tags_with_field.add(tag)
        if tag not in tag_field_count_dict:
            tag_field_count_dict[tag]= tag_field_count_dict.get(tag, 0) + 1
        else:
            tag_field_count_dict[tag]+=1
    else:
        tags_without_field_temp.add(tag)


log_index_weightage=lambda x: 1/(math.exp(math.log(x+1,100)))


def additional_feature_columns(field):

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}

    df_train=pd.read_csv(cmdline_params[f'df_train_{field}'])
    df_test=pd.read_csv(cmdline_params[f'df_test_{field}'])


    tags_with_field=set()
    tags_without_field_temp=set()
    tag_field_count_dict=dict()

    if field=='yop':
        field_encoding=field[0].upper()+field[1]+field[2].upper()+'_Encoded'  #from title/author to Title/Author_Encoded
    else:
        field_encoding=field[0].upper()+field[1:]+'_Encoded'            #from yop to YoP_Encoded

    


    for i in range(len(df_train)):
        check_tag_encoded(df_train.tag[i],df_train[f'{field_encoding}'][i],
                             tags_with_field,tags_without_field_temp,tag_field_count_dict)

    tags_without_field=tags_without_field_temp-tags_with_field

    
    total_tags_having_field_encoded=len(df_train[df_train[f'{field_encoding}']==1])

    tag_weights=dict()
 
    for key,item in tag_field_count_dict.items(): 
        tag_weights[key]=item/total_tags_having_field_encoded

    tags_info={
        f'tags_with_{field}':tags_with_field,
        f'tags_without_{field}':tags_without_field,
        f'tag_weights_{field}':tag_weights
    }
    with open(cmdline_params[f'tags_info_{field}'], 'wb') as f: 
        pickle.dump(tags_info, f)
    print(f"{field} Tag_info stored!")

    tag_weights_update=lambda x: ((x*100)**2)/100

    df_train['index']=df_train['index'].apply(log_index_weightage)
    df_train['Tag_label']=df_train.tag.apply(lambda x: 1 if x in tags_with_field else 0)
    df_train['Tag_weights']=df_train.tag.apply(lambda x: tag_weights[x] if x in tag_weights else 0.0001)
    df_train['Tag_weights']=df_train.Tag_weights.apply(tag_weights_update)

    df_test['index']=df_test['index'].apply(log_index_weightage)
    df_test['Tag_label']=df_test.tag.apply(lambda x: 1 if x in tags_with_field else( 0 if x in tags_without_field else -1))
    df_test['Tag_weights']=df_test.tag.apply(lambda x: tag_weights[x] if x in tag_weights else 0.0001)
    df_test['Tag_weights']=df_test.Tag_weights.apply(tag_weights_update)

    

    df_train.to_csv(cmdline_params[f'df_train_{field}'],index=False)
    df_test.to_csv(cmdline_params[f'df_test_{field}'],index=False)







if __name__=='__main__':

    print("additional_features_prep.py running...")
    start_t=time.perf_counter()


    fields=['author','yop','title']

    with concurrent.futures.ProcessPoolExecutor() as executor:
        _=list(executor.map(additional_feature_columns,fields))

    
    end_t=time.perf_counter()
    print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")

    


    
    

