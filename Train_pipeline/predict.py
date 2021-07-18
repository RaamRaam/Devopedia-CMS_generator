from libraries import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

from tensorflow.keras.models import load_model
from sklearn.metrics import roc_curve,confusion_matrix,classification_report
import matplotlib.pyplot as plt



if __name__ == "__main__":

    print("\npredcit.py running...")
    start_t=time.perf_counter()
    
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    test_path=cmdline_params['df_test']

    X_test=pd.read_csv(test_path)
    X_test=X_test[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper',
                    'Tag_label','Tag_weights','Author_Encoded']]
    y_test=X_test.pop("Author_Encoded")

    model_path=str(sys.argv[2])
    model=load_model(model_path)

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

