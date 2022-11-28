# Domain Adaptation of MAD-GAN and LUCID for Cyberattack Detection
LUCID: https://github.com/doriguzzi/lucid-ddos  <br />
MAD-GAN (based on RGAN): https://github.com/LiDan456/MAD-GANs  <br />
RGAN: https://github.com/ratschlab/RGAN  <br />

Unfortunately, I will not be distributing the SWaT dataset or the CICICD2017 or CICDDoS2019 datasets. Please refer to their respective websites. <br />
CICID2017: https://www.unb.ca/cic/datasets/ids-2017.html <br />
CICDDoS2019: https://www.unb.ca/cic/datasets/ddos-2019.html <br />
SWaT: https://itrust.sutd.edu.sg/itrust-labs_datasets/dataset_info/ <br />

This GitHub repo stores the project I did for my Master of Philosophy thesis at Auckland University of Technology, and for the following publication:
(upcoming) <br />
Please cite the publication and this repo if you are using it for academia purposes.

MAD-GAN is an anomaly detection model for cyber-physical systems, trained using the SWaT dataset. LUCID is a DDoS detection model for network, IoT, edge computing, trained with datasets from University of New Brunswick (incl. CICIDS2017 at the time of publication). In this research, I attempted to perform domain adaptation (transfer learning) on both models, i.e.
- Train LUCID on CICIDS2017 + CICDDoS2019 and test it on SWaT dataset, and vice versa.
- Train MAD-GAN on CICIDS2017 + CICDDoS2019 and test it on SWaT dataset, and vice versa.

More information on the results can be found in the preprint version of my publication attached here as a pdf (to avoid copyright infringements). After all, research has to be reproducible! For the script I used to measure computational overhead as described in the paper (CPU & RAM usage), see `monitor_v2.ipynb`.

## Technical Information
**CPU**
HP Z4 G4 Workstation  
Processor: Xeon W-2265 3.5 12C 24T 3.5~4.8 GHZ 19.25 MB cache  
RAM: 128 GB  
Storage: 1TB SSD + 4TB HDD  
OS: Ubuntu 22.04.01  

**Core Dependencies**
| LUCID  | MAD-GAN (training) | MAD-GAN (testing)|
| ------------- | ------------- | ------------- |
| Python v3.9.13  | Python v3.6.13 | Python v3.10.6 |
| numpy v1.23.3 | numpy v1.19.2  | numpy v1.23.5 |
| scipy v1.9.1 | scipy v1.1.0 | scipy v1.9.3 |
| tensorflow v2.4.1 | tensorflow v1.15.1 | tensorflow v2.11.0 |
| scikit-learn v1.1.3 | scikit-learn v0.19.1 | scikit-learn v1.1.3 |
| tshark v3.6.2 | pandas v0.22.0 | pandas v1.5.2 |
|pyshark v0.5.3 | matplotlib v2.1.1| matplotlib v5.0.1 |
| | keras v2.1.2| keras v2.11.0 |
| | bleach v1.5.0| bleach v5.0.1 |

LUCID is easy to set up. As long as you install the latest version of Tensorflow, Pyshark, and Tshark, then the model should run just fine. I left the other dependencies in for the sake of completeness.<br />

The dependencies needed for MAD-GAN were rather complicated. During training, I set up an environment with exact dependencies as shown in the table above. These requirements can't be satisfied however when using the model on a Raspberry Pi 4 (possibly because they are unsupported by the OS?), which is why I used a different environment and modified the anomaly detection script (AD.py) so it will work on the newer depedencies. I can't guarantee that the training script will work as that is not tested yet.<br />

## How MAD-GAN & LUCID works
Dr. Doriguzzi-Corin did a fantastic job at explaining this in his repo (link above), so please refer to that if you would like to run LUCID :D  <br />

As for MAD-GAN, it is a bit more complicated. Normally, MAD-GAN use .csv inputs for both training and testing. In a nutshell, you would normally run the following (example with swat dataset):  <br />
Training: `python3 RGAN.py swat` <br />
Anomaly detection with discriminator: `python3 AD.py swat_test`  <br />
Anomaly detection with discriminator & generator `python3 AD_Invert.py swat_test`  <br />

For some reason AD_Invert.py would keep running for hours without converging, so I recommend that you don't use in the meantime. It's an ongoing issue which you can find here https://github.com/LiDan456/MAD-GANs/issues/3.<br />

Both the `swat` and `swat_test` are referring to the `data` parameter in text files that have the training/testing parameters that MAD-GAN is going to use. Essentially, MAD-GAN will look for `data: swat` or `data: swat_test` in `experiments/settings/\*.txt` to run the models on its own after. This is done through `def get_data()` in `data_utils.py`.<br />

Once MAD-GAN found the corresponding "data" name, it will trigger the training and testing function accordingly. Below is a snippet of that.
`    elif data_type == 'swat':` <br />
        `samples, labels = swat(seq_length, seq_step, num_signals)`<br />
    `elif data_type == 'swat_test':`<br />
        `samples, labels, index = swat_test(seq_length, seq_step, num_signals)`<br />

The training process will leave multiple `.npy` files in the `experiments/parameters` directory. When using the `AD.py`, the scripts will use these `.npy` files to perform anomaly detection. This leads us to the next trick on adapting MAD-GAN to other datasets.<br />

## Adapting MAD-GAN to other datasets (e.g. CICIDS2017 & CICDDoS2019)
Since I changed MAD-GAN scripts so that it will work on CICIDS2017 & CICDDoS2019, I've uploaded both MAD-GAN (training) and MAD-GAN (testing) here for your convenience (as dependencies can be annoying some times). Luckily, dataset shapes do not seem to be a problem.<br />

There are two main things if you want to train and test any dataset:<br />
- You need a settings file (.txt) for training, and testing. To be fair, just copy it from the existing files and change a few things which I will talk about.
- You need to add two functions, one for training and one for testing in `data_utils.py`. In my case, I added cicddos() and cicddos_test() to train on CICIDS2017 and test on CICDDoS2019 datasets.
- You need to add the selection into `def get_data()` in `data_utils.py` so that `AD.py` can call your new functions.

Truthfully speaking, the cicddos() and cicddos_test() functions are exact copy of the existing swat() and swat_test() functions. You can use kdd99() and kdd99_test() functions as references also. The only changes are the file path to training & testing data. I do think that we can optimize this part of the script to generalize it for multiple datasets, so other users don't have to add new functions every time.<br />

Here's my snippet of `def get_data()`:<br />
`    elif data_type == 'cicddos2017':`<br />
        `samples, labels = swat(seq_length, seq_step, num_signals)`<br />
    `elif data_type == 'cicddos2019'`:<br />
        `samples, labels, index = swat_test(seq_length, seq_step, num_signals)`<br />
 
And here's my snippet of `cicddos()`. You shouldn't need to care about anything else written after this bit. <br />
`def cicddos(seq_length, seq_step, num_signals, randomize=False):`<br />
    `train = np.loadtxt(open('./data/cicddos2017_benign.csv'), delimiter=',')`<br />
    `print('Loaded CICDDoS2017 from .csv')` <br />

This is straightforward. After I copy the `swat()` function, I changed the name to `cicddos()`, and then changed the directory of data in `train = np.loadtxt()`. <br />

The trick to adapting MAD-GAN for training other model is to modify the following parameters of the settings file (e.g. cicddos.txt)<br />
- "data": This has to match with what `def get_data()` is looking for. E.g. "data": cicddos2017
- "sub_id": This refer to what model to use when perform anomaly detection. If `sub_id = swat`, the `AD.py` script will look for swat_x_x.npy from `experiments/parameters/` to perform anomaly detection. If it was `sub_id = cicddos`, the `AD.py` script will look for cicddos_x_x.npy instead. 
- "identifier": This one doesn't really matter, but more often than not it's the same as "data" parameter. 

From the above, I can easily train MAD-GAN with the SWaT dataset and then test it on the CICDDoS2019 dataset by adding the following changes to cicddos_test.txt settings file:<br />
- "data": cicddos2017
- "sub_id": swat
- "identifier": cicddos_test

You should be able to do the same with other datasets.

## Adapting LUCID to other datasets
I made no changes to the LUCID model, however note that it is tightly implemented for the TCP/IP protocol. As long as LUCID can correctly label data as benign or traffic using the 5-tuple (source IP, source port, destination IP, destination port, protocol), LUCID should works with any dataset. See this issue here for more information:<br />
https://github.com/doriguzzi/lucid-ddos/issues/7
