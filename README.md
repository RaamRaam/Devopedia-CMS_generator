# Devopedia-CMS_generator

Given a URL, parse the content and generate a reference in Chicago Manual of Style (CMS) format.


### Train_Pipeline


python dataprep.py inputs.csv 100

python encodings.py inputs.csv

python featureprep.py inputs.csv

python split.py inputs.csv

python train.py inputs.csv yes author_model

python predict.py inputs.csv author_model
