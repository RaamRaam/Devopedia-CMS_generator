from libraries import *
from datetime import datetime
import pickle
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

from tensorflow.keras.models import load_model
from sklearn.metrics import roc_curve,confusion_matrix,classification_report
import matplotlib.pyplot as plt
import swifter
import spacy
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()

def spacy_ner(text):
    doc = nlp(str(text))
    return doc.ents


def prediction_stats(field,train_or_test):
    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}
    path=cmdline_params[f'df_{train_or_test}_{field}']
    
    if field=='yop':
        field_encoding=field[0].upper()+field[1]+field[2].upper()+'_Encoded' 
    else:
        field_encoding=field[0].upper()+field[1:]+'_Encoded'

    df=pd.read_csv(path)
    X_test=df[['index','caps_count','first_token_upper','comma_percent','No_of_tokens','first_letter_upper',
                    'Tag_weights',f'{field_encoding}']]
    y_test=X_test.pop(f'{field_encoding}')

    model_path=str(sys.argv[2])
    model=load_model(f'{field}_{model_path}')

    print(f"Evaluation on {train_or_test} set:")
    model.evaluate(X_test,y_test)
    y_preds = model.predict(X_test)


    #ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, y_preds)
    gmeans = np.sqrt(tpr * (1-fpr))
    # locate the index of the largest g-mean
    ix = np.argmax(gmeans)
    print('Best Threshold=%f, G-Mean=%.3f' % (thresholds[ix], gmeans[ix]))
    # plot the roc curve for the model
    # plt.plot([0,1], [0,1], linestyle='--', label='No Skill')
    # plt.plot(fpr, tpr, marker='.', label='ANN')
    # plt.scatter(fpr[ix], tpr[ix], marker='o', color='black', label='Best')
    # # axis labels
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.legend()
    # # show the plot
    # plt.show()

    best_thresh=thresholds[ix]
    predicted_categories = np.where(y_preds > best_thresh, 1, 0)

    df_preds=df
    df_preds.drop(f'{field_encoding}',axis=1,inplace=True)
    df_preds['Ground_truths']=y_test
    df_preds['Predictions']=predicted_categories
    df_preds['Pred_proba']=y_preds

    print(df_preds.shape)
    

    if field=='author':
        
        df_preds2=df_preds.loc[(df_preds.Predictions==1)]
        print(df_preds2.shape)

        x=df_preds2['text'].swifter.apply(lambda x : 1 if spacy_ner(x) else 0)
        df_preds['Preds_ner']=x
        df_preds.Preds_ner.fillna(df_preds.Predictions, inplace=True)
        df_preds['Preds_ner']=df_preds['Preds_ner'].astype('int')
        df_preds['Predictions']=df_preds['Preds_ner']
        del df_preds['Preds_ner']

    df_preds2=df_preds.loc[(df_preds.Ground_truths==1) | (df_preds.Predictions==1)]  
    df_preds2.to_csv(f"{field}_{train_or_test}_Prediction_diagnostics.csv",index=False)
    print(f"\n{field}_{train_or_test}_Prediction diagnostics created and saved!\n")


    print("Confusion Matrix:\n")
    conf_matrix=confusion_matrix(df_preds['Predictions'], df_preds['Ground_truths'])
    print(conf_matrix)

    print("Classification Report:\n")
    class_report=classification_report(df_preds['Predictions'], df_preds['Ground_truths'])
    print(class_report)

    print(f"Best threshold obtained at:{best_thresh}")

    return best_thresh,str(conf_matrix),class_report


def logs(fields,train_or_test,thresholds,conf_matrices,class_reports,datetime):

    f=open(f'{train_or_test} {datetime}.txt','w')
   
    for field in fields:
        f.write(field)
        f.write("\n") 
        f.write(conf_matrices[field])
        f.write("\n")
        f.write(class_reports[field])
        f.write("\n")
        f.write(f"Best threshold for {field}:{str(thresholds[field])}\n")
        f.write("-"*69+"\n\n")

    f.close()

    with open(f'{field}_thresholds.pkl', 'wb') as f: 
        pickle.dump(thresholds, f)




if __name__ == "__main__":

    print("\npredcit.py running...")
    start_t=time.perf_counter()

    now=datetime.now()
    now = now.strftime("%d-%m-%Y %H-%M")
    
    fields=['author','title','yop']
    thresholds={'author':0,'title':0,'yop':0}
    conf_matrices={'author':"",'title':"",'yop':""}
    class_reports={'author':"",'title':"",'yop':""}

    for field in fields:
        thresholds[f'{field}'],conf_matrices[f'{field}'],class_reports[f'{field}']=prediction_stats(field,'test')

    logs(fields,'test',thresholds,conf_matrices,class_reports,now)
    print(thresholds)

    
    for field in fields:
        thresholds[f'{field}'],conf_matrices[f'{field}'],class_reports[f'{field}']=prediction_stats(field,'train')

    logs(fields,'train',thresholds,conf_matrices,class_reports,now)
    print(thresholds)


    print(f"\n\nBest threshold values stored!")
    end_t=time.perf_counter()
    print(f"Program completed running in {(end_t-start_t)/60} minutes!\n")

