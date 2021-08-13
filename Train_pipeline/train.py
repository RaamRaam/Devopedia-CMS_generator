import warnings
warnings.filterwarnings("ignore")
from libraries import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Model
import io

add_layer=lambda units: layers.Dense(units,activation='relu')

def get_model_summary(model):               #function to convert none type model.sunnmary() to string to store in external file
    stream = io.StringIO()
    model.summary(print_fn=lambda x: stream.write(x + '\n'))
    summary_string = stream.getvalue()
    stream.close()
    return summary_string


def train_model(field):
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    train_path=cmdline_params[f'df_train_{field}']

    if field=='yop':
        field_encoding=field[0].upper()+field[1]+field[2].upper()+'_Encoded'  #title/author => Title/Author_Encoded
    else:
        field_encoding=field[0].upper()+field[1:]+'_Encoded'            # yop => YoP_Encoded

    X_train=pd.read_csv(train_path)

    X_train=X_train[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper',
                    'year_presence','Tag_weights',f'{field_encoding}']]

    print(X_train.info())

    #Under/over sampling

    X_train0=X_train[X_train[f'{field_encoding}']==0]
    X_train1=X_train[X_train[f'{field_encoding}']==1]

    print(f"0s : {len(X_train0)}")
    print(f"1s : {len(X_train1)}\n\n")


    X_train1=pd.concat([X_train1]*20, ignore_index=True)     #Oversampling by 20 times the number of rows having encoding 1
    X_train0=X_train0.sample(frac=0.4,random_state=7)         #Undersampling by taking only 40% of rows having encoding 0

    print(f"0s after undersampling: {len(X_train0)}")
    print(f"1s after undersampling: {len(X_train1)}")


    X_train=pd.concat([X_train0,X_train1],ignore_index=True)           #Concatenating 0-label rows and 1-label rows
    X_train = X_train.sample(frac=1).reset_index(drop=True)             #randomizing whole dataframe 

    
    negs=len(X_train[X_train[f'{field_encoding}']==0])
    pos=len(X_train[X_train[f'{field_encoding}']==1])
    print ('Total Negatives:',negs )
    print ('Total Positives:', pos)
    total=negs+pos

    weight_for_0 = (1 / negs) * (total / 2.0)
    weight_for_1 = (1 / pos) * (total / 2.0)

    class_weight = {0: weight_for_0, 1: weight_for_1}


    print(f"Class Weights:{class_weight}")

    y_train=X_train.pop(f'{field_encoding}')


    #------------------------------------------------------Model creation--------------------------------------------------------
    inputs=keras.Input(shape=(X_train.shape[1]))
    x=inputs

    no_of_layers=int(cmdline_params['hidden_layers'])
    
    for i in range(0,no_of_layers):
        units=int(cmdline_params[f'units_{i+1}'])
        x=add_layer(units)(x)
        x=layers.BatchNormalization()(x)

    outputs=layers.Dense(1,activation="sigmoid")(x)

    model=Model(inputs=inputs,outputs=outputs,name="Basic_ANN")

    print(model.summary())
    model_summary_string = get_model_summary(model)

    folder_path='Models'
    with open(os.path.join(folder_path,"Model_summary.txt"),"w") as f:
        f.write(model_summary_string)

    #-------------------------------------------------------Model training--------------------------------------------------------

    lr=float(cmdline_params['learning_rate'])
    EPOCHS=int(cmdline_params['EPOCHS'])
    BS=int(cmdline_params['batch_size'])

    model.compile(loss=tf.keras.losses.BinaryCrossentropy(),optimizer=keras.optimizers.Adam(learning_rate=lr),metrics=["accuracy"])

    history=model.fit(X_train,y_train,batch_size=BS,epochs=EPOCHS,verbose=1,class_weight=class_weight)  #training with class_weights to counteract class imbalance further

    model_save_choice = str(sys.argv[2])

    if model_save_choice=='save':

        model_name=str(sys.argv[3])
        model_name=f"{field}_{model_name}"
        model.save(os.path.join(folder_path,model_name),save_format='tf')    #for tf version > 2

        print(f"Model Saved as {model_name}")

    else:
        print("Model not saved..")

    return model
    

if __name__ == "__main__":

    start_t=time.perf_counter()

    try:
        os.mkdir('Models')
    except:
        pass

    fields=['author','title','yop']
    for field in fields:
        train_model(field)

    end_t=time.perf_counter()

    print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")
