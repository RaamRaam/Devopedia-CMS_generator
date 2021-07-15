import warnings
warnings.filterwarnings("ignore")
from libraries import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Model
from sklearn.metrics import roc_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt


def add_layer(units):
    return layers.Dense(units,activation="relu")
    

if __name__ == "__main__":

    start_t=time.perf_counter()

    print("\nRunning train.py...\n")

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}

    train_path=cmdline_params['df_train']
    

    X_train=pd.read_csv(train_path)

    try:    
        test_path=cmdline_params['df_test']
        X_test=pd.read_csv(test_path)
        y_test=X_test.pop("Author_Encoded")
    except:
        test_path=None

    
    negs=len(X_train[X_train.Author_Encoded==0])
    pos=len(X_train[X_train.Author_Encoded==1])
    print ('Total Negatives:',negs )
    print ('Total Positives:', pos)
    total=negs+pos

    weight_for_0 = (1 / negs) * (total / 2.0)
    weight_for_1 = (1 / pos) * (total / 2.0)

    class_weight = {0: weight_for_0, 1: weight_for_1}

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

    try:
        model_save_choice=cmdline_params['model_save_choice']

        if model_save_choice=='yes':
            model_name=cmdline_params['model_name']
            model.save(model_name,save_format='tf')

            print(f"Model Saved as {model_name}")

        else:
            print("Model not saved..")
    except:
        print("Model not saved..")

    end_t=time.perf_counter()

    #--------------------------------------------------------Model evaluation--------------------------------------------------------
    if test_path is not None: 
        print("Evaluation on test set:")
        model.evaluate(X_test,y_test)
        y_preds = model.predict(X_test)


        #ROC curve
        fpr, tpr, thresholds = roc_curve(y_test, y_preds)
        gmeans = np.sqrt(tpr * (1-fpr))
        # locate the index of the largest g-mean
        ix = np.argmax(gmeans)
        print('Best Threshold=%f, G-Mean=%.3f' % (thresholds[ix], gmeans[ix]))
        # plot the roc curve for the model
        plt.plot([0,1], [0,1], linestyle='--', label='No Skill')
        plt.plot(fpr, tpr, marker='.', label='ANN')
        plt.scatter(fpr[ix], tpr[ix], marker='o', color='black', label='Best')
        # axis labels
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.legend()
        # show the plot
        plt.show()

        best_thresh=thresholds[ix]
        predicted_categories = np.where(y_preds > best_thresh, 1, 0)
        
        true_categories = y_test

        print("Confusion Matrix:\n")
        print(confusion_matrix(predicted_categories, true_categories))

        print("Classification Report:\n")
        print(classification_report(predicted_categories, true_categories))
        print(f"Best threshold obtained at:{best_thresh}")

        end_t=time.perf_counter()
        print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")

    else:
        print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")




  



    



        