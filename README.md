# Devopedia-CMS_generator

Given a URL, parse the content and generate a reference in Chicago Manual of Style (CMS) format.


### Train_Pipeline


python dataprep.py inputs.csv 100

python encodings.py inputs.csv

python featureprep.py inputs.csv

python split.py inputs.csv

python train.py inputs.csv yes author_model

python predict.py inputs.csv author_model

<hr>

### Test_Pipeline

python url2file.py https://medium.com/analytics-vidhya/seq2seq-abstractive-summarization-using-lstm-and-attention-mechanism-code-da2e9c439711

python tag_text_extract.py inputs.csv

python featureprep.py inputs.csv

python predict.py inputs.csv Author_ANN
