
# Pneumonia Chest Radiography Diagnoser
> A suite of **CRUDE** software apps for diagnosing and detecting pneumonia symptoms

[![prog-status](https://img.shields.io/badge/status-submit%20for%20final-bright?style=plastic)](https://shields.io/)


[![Python](https://img.shields.io/badge/Python-FFD43B?style=plastic&logo=python&logoColor=blue)](https://www.python.org/)
[![Pytorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=plastic&logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=plastic&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=plastic&logo=Kaggle&logoColor=white)](https://www.kaggle.com/)


## API Description
The repo has two mini apps (both with tkinter GUI as the front end) dealing with pneumonia chest radiography diagnoser image data.

### **Detector**:  
This app loads a Fast R-CNN object detection neural network in the background. After the user upload a *.jpg file through the file dialog, it will pop up the image and mark inferred inflamation areas with a confidence probability. The terminal will also display information about result.  
For details about the training, please check the `colab-training` folder. [`Detecto`](https://detecto.readthedocs.io/en/latest/), a higher-level compact package writen in Pytorch is used.

### **Diagnoser**:
This app connect to a MongDB in the background. It can provide information about a CRX record after the user input the corresponding patinet ID in the entry box. The app can display the original image, mark the symptom areas, and segment them.

*(The reason for not combining them: after I combine the two set of functionalities, the Pytorch deep learning model and PyMongo client will cause a segmentation fault.)*


## Setup
### Installation
```sh
git clone https://github.com/scotsun/biostat821final_project.git
```

### Download the data from `Kaggle API`

To use the Kaggle API, we must authenticate it by using our own API token.

*Steps to generate and configure it:*  
1. Under the profile page, click Account tab
2. Scroll down to the API section and download the token, which is named `kaggle.json`
3. For Linux and macOS, move the file at `~/.kaggle/kaggle.json`

```sh
pip install kaggle
kaggle datasets download -d sovitrath/rsna-pneumonia-detection-2018
mv input/stage_2_train_labels.csv input/annot.csv
mv input pneumonia
```

### DB Configuration
Check [MongDB](https://www.mongodb.com/docs/manual/introduction/) for installation and basic setup.
```sh
python build_db.py
```
## Contributing
1. Fork it
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -m 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request