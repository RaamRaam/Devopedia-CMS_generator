# Devopedia-CMS_generator

Given a URL, parse the content and generate a reference string in Chicago Manual of Style (CMS) format.

Master Commands to use pipelines

## To directly input an URL and get predictions

python commands.py (url) (model_name)


## For Preprocessing

### Preprocessing (Train pipeline)

python commands.py preprocess train inputs.csv (files_batch_size)

### Preprocessing (Test pipeline)

python commands.py preprocess test inputs.csv (url)



## For Training

### Save model

python commands.py train inputs.csv yes (model_name)

### Train without saving model

python commands.py train inputs.csv no



## For Postprocessing

### Postprocessing (Train pipeline)

python commands.py postprocess train inputs.csv (model_name)

### Postprocessing (Test pipeline)

python commands.py postprocess test inputs.csv (model_name)




<hr>


### Train_Pipeline


python dataprep.py inputs.csv (batch size for processing files)

python encodings.py inputs.csv

python featureprep.py inputs.csv

python split.py inputs.csv

python additional_features_prep.py inputs.csv

python train.py inputs.csv yes ANN2

python predict.py inputs.csv ANN2

python cosine_similarity.py inputs.csv

python aggregated_cosine_similarity.py inputs.csv



<hr>

### Test_Pipeline

python url2file.py (url)

python dataprep.py inputs.csv

python featureprep.py inputs.csv

python additional_featureprep.py inputs.csv

python predict.py inputs.csv ANN2

python generate_ref_strings.py inputs.csv
