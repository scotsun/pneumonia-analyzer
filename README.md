
# Pneumonia Chest Radiography Diagnoser


[![prog-status](https://img.shields.io/badge/status-in%20progress-orange?style=plastic)](https://shields.io/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

## Setup
### Installation
```sh
git clone https://github.com/scotsun/biostat821final_project.git
```

### Download the data and rename `dir` and file
```sh
pip install kaggle
kaggle datasets download -d sovitrath/rsna-pneumonia-detection-2018
mv input/stage_2_train_labels.csv input/annot.csv
mv input pneumonia
```