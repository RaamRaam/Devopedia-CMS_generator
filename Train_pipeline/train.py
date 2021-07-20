import warnings
warnings.filterwarnings("ignore")
from libraries import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Model


# def add_layer(units):
#     return layers.Dense(units,activation="relu")

add_layer=lambda units: layers.Dense(units,activation='relu')
    

if __name__ == "__main__":

    start_t=time.perf_counter()

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    train_path=cmdline_params['df_train']

    X_train=pd.read_csv(train_path)

    X_train=X_train[['index','first_token_upper','comma_percent','No_of_tokens','first_letter_upper',
                    'Tag_weights','Author_Encoded']]

    print(X_train.info())

    #Under/over sampling

    # X_train0=X_train[X_train.Author_Encoded==0]
    # X_train1=X_train[X_train.Author_Encoded==1]


    # X_train1=pd.concat([X_train1]*10, ignore_index=True)
    # X_train0=X_train0.sample(frac=0.4,random_state=7)


    # X_train=pd.concat([X_train0,X_train1],ignore_index=True)
    # X_train = X_train.sample(frac=1).reset_index(drop=True)

    
    negs=len(X_train[X_train.Author_Encoded==0])
    pos=len(X_train[X_train.Author_Encoded==1])
    print ('Total Negatives:',negs )
    print ('Total Positives:', pos)
    total=negs+pos

    weight_for_0 = (1 / negs) * (total / 2.0)
    weight_for_1 = (1 / pos) * (total / 2.0)

    class_weight = {0: weight_for_0, 1: weight_for_1}

    print(f"Class Weights:{class_weight}")

    y_train=X_train.pop("Author_Encoded")


    #------------------------------------------------------Model creation--------------------------------------------------------
    inputs=keras.Input(shape=(X_train.shape[1]))
    x=inputs

    no_of_layers=int(cmdline_params['hidden_layers'])
    
    for i in range(0,no_of_layers):
        units=int(cmdline_params[f'units_{i+1}'])

        x=add_layer(units)(x)

    outputs=layers.Dense(1,activation="sigmoid")(x)

    model=Model(inputs=inputs,outputs=outputs,name="Basic_ANN")

    print(model.summary())

    #-------------------------------------------------------Model training--------------------------------------------------------

    lr=float(cmdline_params['learning_rate'])
    EPOCHS=int(cmdline_params['EPOCHS'])
    BS=int(cmdline_params['batch_size'])

    model.compile(loss=tf.keras.losses.BinaryCrossentropy(),optimizer=keras.optimizers.Adam(learning_rate=lr),metrics=["accuracy"])

    history=model.fit(X_train,y_train,batch_size=BS,epochs=EPOCHS,verbose=1,class_weight=class_weight)

    model_save_choice = str(sys.argv[2])

    if model_save_choice=='yes':

        model_name=str(sys.argv[3])
        model.save(model_name,save_format='tf')

        print(f"Model Saved as {model_name}")

    else:
        print("Model not saved..")

    end_t=time.perf_counter()

    print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")
