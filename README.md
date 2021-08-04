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


##### python dataprep.py inputs.csv (batch size for processing files)
Creates a csv dataframe (raw_dataset.csv) having tags and text extracted along with corresponding author, title and yop labels

##### python encodings.py inputs.csv
Creates 3 dataframes (author, title, yop) from raw_dataset.csv having respective encodings 

##### python featureprep.py inputs.csv
Extracts relevant features from the text column for input into the neural network

##### python split.py inputs.csv
File leverl train-test split (currently 587 files randomly chosen for test set)

##### python additional_features_prep.py inputs.csv
Adding more relevant features (calculating tag_weights, and mathematical operation on index)

##### python train.py inputs.csv yes ANN2
Feeding input features into the neural net and training the 3 separate models (for author, title, yop of course)

##### python predict.py inputs.csv ANN2
Generating prediction diagnostic csv files using the trained models

##### python cosine_similarity.py inputs.csv
Generating csv files having cosine_similarity score between author, title, yop prediction of each file based on
- Top 3 indices
- Top 3 prediction probabilities

##### python aggregated_cosine_similarity.py inputs.csv
Aggregating cosine similarity csv files 



<hr>

### Test_Pipeline

##### python url2file.py (url)
Generatin and saving html file of the input URL 

##### python dataprep.py inputs.csv
Extracting tag and text from html file using BeautifulSoup

##### python featureprep.py inputs.csv
Extracting same features as in Train pipeline for input into the neural network

##### python additional_featureprep.py inputs.csv
Adding more relevant features (using tag_weights calculated in Train pipeline,  and mathematical operation on index)

##### python predict.py inputs.csv ANN2
Feeding features into the trained models and generating predictions

##### python generate_ref_strings.py inputs.csv
Generating top 3 Titles, Authors, YoPs as per predictions based on
- Indices
- Max Probabilties
