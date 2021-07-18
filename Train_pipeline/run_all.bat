python dataprep.py inputs.csv 100
python encodings.py inputs.csv
python featureprep.py inputs.csv
python split.py inputs.csv
python additional_features_prep.py inputs.csv
python train.py inputs.csv yes author_model
python predict.py inputs.csv author_model