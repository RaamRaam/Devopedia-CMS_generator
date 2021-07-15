# Devopedia-CMS_generator

Given a URL, parse the content and generate a reference in Chicago Manual of Style (CMS) format.


### Order of py files exection:

1. dataprep.py
Command:
python dataprep.py <<argument_csv_file_name>> <<batch_size_for processesing>>

Eg:
python dataprep.py inputs.csv 100

Pre-requisite:
inputs.csv must contain paths for html_folder, devopediaArticles.v2525.json and meta.v2525.jl

Outputs:
Will generate files_and_references.csv (not very necessary) and raw_dataset.csv.

<hr>

2. encodings.py

Command:
python encodings.py

Pre-requisite:
Will ask for raw_dataset.csv path.

Output:
Will generate author.csv, title.csv, yop.csv and Author_encoded.csv, Title_encoded.csv and YoP_encoded.csv.

3. split.py

Command:
python split.py

Pre-requisite:
Will ask for author/title/yop encoded csv path.

Output:
Will generate train_author/title/yop_encoded.csv and test_author/title/yop_encoded.csv

4. featureprep.py

Command:
python featureprep.py

Pre-requisite:
Will ask for author/title/yop encoded csv path. (you may enter the train or test file path)

Output:
Will extract features from text column of provided dataset and generate features_train/test_author/title/yop_encoded.csv


5. train.py

Command:
python train.py

Pre-requisite:
(TF_version 2+ needed)
Will ask for train and test (optional) datasets, model hyperparameters.

Output:
Will create and save a model with a name of your choice.

6. url2author.py

Command:
python url2author.py

Pre-requisite:
(TF_version 2+ needed)
Will ask for a URL and model path.

Output:
Will print author (as per the model) and generate features dataset of the parsed url page along with corresponding predictions.

