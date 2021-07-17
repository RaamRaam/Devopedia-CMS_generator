from libraries import *
from feature_functions import *

def featureprep_func(df_name):
    df=pd.read_csv(df_name)
    df=add_columns(df)
    df=df[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper']]
    df.to_csv(cmdline_params['file_df_features'],index=False)


if __name__ == "__main__":
    print("Featurepre.py running...\n\n")
    start=time.perf_counter()

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    featureprep_func(cmdline_params['file_df'])
        
    end=time.perf_counter()
    
    print(f"Featureprep ran in {end-start} seconds!\n")