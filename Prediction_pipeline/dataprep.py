from libraries import *
from functions import *
import warnings
warnings.filterwarnings("ignore")

if __name__=="__main__":
    folder_path='Prediction_outputs'
  
    print("Extracting tags and texts from html file...\n")
    get_df=lambda el: create_df(el,filter(check_first_char,
                                          filter(exclude_texts,
                                                filter(exclude_tags,
                                                        extract_bs(el)
                                                    )
                                                )
                                          )
                                ).drop(['fname','text4dup'], axis = 1)

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    test_path=cmdline_params['file']

    file=cmdline_params['file']
    df=get_df(file)
    df_name=cmdline_params['file_df']
    df.to_csv(os.path.join(folder_path,'file_tag_text.csv'),index=False)
    print(f"Dataframe of shape {df.shape} created!")
    

    
