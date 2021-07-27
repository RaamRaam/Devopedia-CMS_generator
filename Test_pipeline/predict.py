from libraries import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from tensorflow.keras.models import load_model


def preds(field):
    data=df[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper',f'Tag_weights_{field}']]
    model_path=str(sys.argv[2])
    model=load_model(f'{field}_{model_path}')
    y_preds = model.predict(data)
    df[f'{field}_preds']=y_preds



if __name__ == "__main__":

    print("\npredcit.py running...\n\n")
    start_t=time.perf_counter()
    
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    df_path=cmdline_params['file_df_features']

    df=pd.read_csv(df_path)
    
    
    fields=['author','title','yop']

    with concurrent.futures.ThreadPoolExecutor() as exc:
        exc.map(preds,fields)
    


    

    # df=pd.read_csv(cmdline_params['file_df_features'])
    # df['preds']=y_preds
    # x=np.argmax(y_preds)
    # print(df.text[x])

    df.to_csv('Predictions.csv',index=False)
    

    end_t=time.perf_counter()
    print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")

