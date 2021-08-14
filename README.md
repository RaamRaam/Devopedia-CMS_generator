# Devopedia.org

# Chicago Manual Style Citation String

For Devopedia Articles the citation adapted is Chicago style.  More on the style is in the following link

https://www.citationmachine.net/chicago



## Objective

In this project we have aimed to construct the citation for website given the URL.  The examples are in the following link

https://www.chicagomanualofstyle.org/tools_citationguide/citation-guide-1.html#cg-website

The standard format is as follows

**Author, year_of_publishing, Title**, granular time details, granular content details

We attempt to predict the content in bold given URL



## Data

- Total Devopedia Articles -  About 10K

- Web Site Referenced Articles - About 7K

- Used Articles

  -For Authors- 5064 files
  -For Titles- 6220 files
  -For YoPs- 3532 files

- Train Articles

  -For Authors- 4477 files
  -For Titles- 5633 files 
  -For YoPs- 2945 files

- Test Articles -587 files for each

- Challenges:

  - Plenty of .htm files had no relevant content (for example, just script and meta tags)

  - Some .htm files did not support 'utf-8' or 'iso' encodings (perhaps in another language script)

  - Those .htm files which did not contain even a single Title/Author/YoP encoding label as 1 for all its extracted tag-text rows were not used in their respective field datasets

    

## Methodology

1. Crawl the URL

2. Extract Tag and Content

3. Label the Tag and Content with Author/YoP/Title if the content has Author/YoP/Title respectively

4. Build Features

   1. Number of tokens in text
   2. Weights for Tags, say, if title appears in 'h1' tag 10% of the times, the weight for 'h1' is 0.10
   3. number of commas as percentage of number of tokens - this is useful to find Author
   4. number of tokens have first letter as Capital letter
   5. index(position) weightage of Tag/content.  the earlier the tag/content, the higher weightage is assigned
   6. if the text contains year(4 digit number with first digit either 1 or 0)

5. Split the URLs(and its content) into Train and Test

6. Train distinct models for Author/Title/YoP by up-sampling/down-sampling

7. Since the probable tags are predicted some post processing is done to extract Author/Title/YoP

8. The dataset is imbalanced because only fewer tags can be labelled as Author/Title/YoP.  

   Hence False negatives are minimized and False positives are compromised. The idea is to increase recall and compromise on precision

   We publish top 3 predictions and expect the exact predictions to be part of the top 3

   Reference string is constructed

   



# Process Document

## Install requirements

```
pip install -r requirements.txt
```

## Training

- Modify the train_inputs.csv file to configure 
- html_path - location where crawled html files are present
- articles - location where train data is made available in json format
- meta_data - location where meta data is present
- you can also configure number of layers, number of nodes in each layer, learning rate, number of epoch and batch size towards the end of the file
- The output files are named in the configuration.  please leave them as it is to avoid errors

```
python commands.py preprocess train inputs.csv (files_batch_size)
python commands.py train inputs.csv save (model_name)
python commands.py postprocess train inputs.csv (model_name)
```
- The preprocess will generate files in Train_preprocess folder
- The model files  will be generated in the root folder as .pkl files
- The postprocess will generate files Train_diagnostics folder



## Diagnostics

Since we ignore false positives on purpose and depend on top 3 predictions post processing a custom metric(based on similarity with original ref string) is worked out to arrive at accuracy 

This needs further attention





## To get predictions by giving URL as input

```
python commands.py predict (url) (model_name)
```

- The URL inputted is crawled and saved as file.htm in the Prediction_outputs folder (which is created if not already present in the root direcotry)
- This results are displayed in screen and files will be present in Prediction_outputs folder
- The results are also stored in Prediction_results.txt file in the Prediction_outputs folder

#### Example

```
python commands.py predict https://sunscrapers.com/blog/10-django-packages-you-should-know/ ANN
```

# Further Scope

- Reference String construction for PDFs/Text files
- Eliminate redundant code for train and predict
- A robust mechanism to define accuracy
- Model file is big and takes long time to load at the time of prediction
- Exploring NER's to narrow down predictions yielding accuracy. 
  - We attempted, but it slows down training/prediction
- Improve features - Tag Weight and index Weight - investigate data and innovate math to represent tag and index with appropriate weights
- Constructing Reference String in case of multiple authors
