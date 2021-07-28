# Devopedia-CMS_generator

Given a URL, parse the content and generate a reference in Chicago Manual of Style (CMS) format.


### Train_Pipeline


python dataprep.py inputs.csv <<<batch size for processing files>>>

python encodings.py inputs.csv

python featureprep.py inputs.csv

python split.py inputs.csv

python additional_features_prep.py inputs.csv

python train.py inputs.csv yes author_model

python predict.py inputs.csv author_model

<hr>

### Test_Pipeline

python url2file.py <<<url>>>

python dataprep.py inputs.csv

python featureprep.py inputs.csv

python additional_featureprep.py inputs.csv

python predict.py inputs.csv ANN

python generate_ref_strings.py inputs.csv
