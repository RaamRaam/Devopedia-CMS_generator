import os
import sys
import time

if sys.argv[1]=='predict':
    url=sys.argv[2]
    model=sys.argv[3]
    py_fname=f"url2ref_string.py {url} {model}"
    path=os.path.join('Prediction_pipeline',py_fname)
    os.system(f"python {path}")

elif sys.argv[1]=='preprocess':

    start_t=time.perf_counter()

    train_or_test=sys.argv[2]
    inputs=sys.argv[3]

    inputs=f"{train_or_test}_{inputs}"
    pipeline_path=(f"{train_or_test}_pipeline")

    if train_or_test=='train':
        files_bs=sys.argv[4]
        py1=os.path.join(pipeline_path,f"dataprep.py {inputs} {files_bs}")
        py2=os.path.join(pipeline_path, f"encodings.py {inputs}")
        py3=os.path.join(pipeline_path, f"featureprep.py {inputs}")
        py4=os.path.join(pipeline_path, f"split.py {inputs}")
        py5=os.path.join(pipeline_path, f"additional_features_prep.py {inputs}")
        py_files=[py1,py2,py3,py4,py5]

    elif train_or_test=='prediction':
        url=sys.argv[4]
        py1=os.path.join(pipeline_path,f"url2file.py {url}")
        py2=os.path.join(pipeline_path,f"dataprep.py {inputs}")
        py3=os.path.join(pipeline_path,f"featureprep.py {inputs}")
        py4=os.path.join(pipeline_path,f"additional_featureprep.py {inputs}")
        py_files=[py1,py2,py3,py4]
    
    else:
        print("Invalid choice!")
        sys.exit() 

    
    for py_fname in py_files:
        os.system(f'python {py_fname}')

    end_t=time.perf_counter()

    print(f"{train_or_test} preprocessing done in {(end_t-start_t)/60} minutes.")


elif sys.argv[1]=='train':
    inputs=sys.argv[2]
    inputs=f"train_{inputs}"

    model_save_choice=sys.argv[3]

    if model_save_choice=='save':
        model_name=sys.argv[4]
        path=os.path.join("train_pipeline",f"train.py {inputs} {model_save_choice} {model_name}")
        os.system(f'python {path}')

    else:
        path=os.path.join("train_pipeline",f"train.py {inputs} {model_save_choice}")
        os.system(f'python {path}')

    

elif sys.argv[1]=='postprocess':

    start_t=time.perf_counter()

    train_or_test=sys.argv[2]
    inputs=sys.argv[3]

    inputs=f"{train_or_test}_{inputs}"
    pipeline_path=(f"{train_or_test}_pipeline")
    model_name=sys.argv[4]

    if train_or_test=='train':
        py1=os.path.join(pipeline_path, f"predict.py {inputs} {model_name}")
        py2=os.path.join(pipeline_path, f"cosine_similarity.py {inputs}")
        py3=os.path.join(pipeline_path, f"aggregated_cosine_similarity.py {inputs}")

        py_files=[py1,py2,py3]

    elif train_or_test=='prediction':
        py1=os.path.join(pipeline_path, f"predict.py {inputs} {model_name}")
        py2=os.path.join(pipeline_path, f"generate_ref_strings.py {inputs}")

        py_files=[py1,py2]


    else:
        print("Invalid choice!!")

    for py_fname in py_files:
        os.system(f'python {py_fname}')


    end_t=time.perf_counter()

    print(f"{train_or_test} postprocessing done in {(end_t-start_t)/60} minutes.")

else:
 	print("Invalid Choice!")
 	sys.exit() 





    



