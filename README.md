## A preprocessing script to generate meta data for the healthcare images

### input:
records.csv and the iamge folder.

### output:
a file containing path, label  with space as the delimiter(for training).
a file containing path, label, IID, gender, with space as the delimiter(for intepretation).
a log file


### dependency
`pip install pydicom`
