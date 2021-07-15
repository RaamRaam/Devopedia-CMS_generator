# Devopedia-CMS_generator

Given a URL, parse the content and generate a reference in Chicago Manual of Style (CMS) format.


### Order of py files exection:

1. dataprep.py
<br>
Command:
python dataprep.py argument_csv_file_name batch_size_for processesing

Eg:<br>
python dataprep.py inputs.csv 100

Pre-requisite:<br>
inputs.csv must contain paths for html_folder, devopediaArticles.v2525.json and meta.v2525.jl

Outputs:
Will generate files_and_references.csv (not very necessary) and raw_dataset.csv.

<hr>

2. encodings.py
<br>
Command:<br>
python encodings.py

Pre-requisite:<br>
Will ask for raw_dataset.csv path.

Output:
Will generate author.csv, title.csv, yop.csv and Author_encoded.csv, Title_encoded.csv and YoP_encoded.csv.
<hr>


3. split.py
<br>
Command:<br>
python split.py

Pre-requisite:<br>
Will ask for author/title/yop encoded csv path.

Output:<br>
Will generate train_author/title/yop_encoded.csv and test_author/title/yop_encoded.csv
<hr>


4. featureprep.py
<br>
Command:<br>
python featureprep.py

Pre-requisite:<br>
Will ask for author/title/yop encoded csv path. (you may enter the train or test file path)

Output:<br>
Will extract features from text column of provided dataset and generate features_train/test_author/title/yop_encoded.csv
<hr>



5. train.py
<br>
Command:<br>
python train.py

Pre-requisite:<br>
(TF_version 2+ needed)
Will ask for train and test (optional) datasets, model hyperparameters.

Output:<br>
Will create and save a model with a name of your choice.
<hr>


6. url2author.py
<br>
Command:<br>
python url2author.py

Pre-requisite:<br>
(TF_version 2+ needed)
Will ask for a URL and model path.

Output:<br>
Will print author (as per the model) and generate features dataset of the parsed url page along with corresponding predictions.

