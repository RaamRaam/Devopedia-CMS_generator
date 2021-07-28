python url2file.py https://medium.com/analytics-vidhya/seq2seq-abstractive-summarization-using-lstm-and-attention-mechanism-code-da2e9c439711
python dataprep.py inputs.csv
python featureprep.py inputs.csv
python additional_featureprep.py inputs.csv
python predict.py inputs.csv ANN
python generate_ref_strings.py inputs.csv