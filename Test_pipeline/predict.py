from libraries import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from tensorflow.keras.models import load_model


if __name__ == "__main__":

    print("\npredcit.py running...\n\n")
    start_t=time.perf_counter()
    
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    test_path=cmdline_params['file_df_features']

    data=pd.read_csv(test_path)
    data=data[['index','first_token_upper','comma_percent','No_of_tokens','first_letter_upper','Tag_weights']]
    model_path=str(sys.argv[2])

    model=load_model(model_path)

    y_preds = model.predict(data)

    df=pd.read_csv(cmdline_params['file_df_features'])
    df['preds']=y_preds
    x=np.argmax(y_preds)
    print(df.text[x])

    df.to_csv('predictions.csv',index=False)
    

    end_t=time.perf_counter()
    print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")

