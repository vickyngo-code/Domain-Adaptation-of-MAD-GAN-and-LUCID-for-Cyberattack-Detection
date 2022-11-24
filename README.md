# MPhil-AUT
LUCID: https://github.com/doriguzzi/lucid-ddos
MAD-GAN (based on RGAN): https://github.com/LiDan456/MAD-GANs
RGAN: https://github.com/ratschlab/RGAN

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
| Python v3.9.13  | Python v3.6.13 |
| numpy 1.23.3 | numpy 1.19.2  |
| scipy 1.9.1 | scipy 1.1.0 |
| tensorflow 2.4.1 | tensorflow 1.15.1 |
| scikit-learn v1.1.3 | scikit-learn 0.19.1|
| tshark v3.6.2 | pandas 0.22.0 |
|pyshark v0.5.3 | matplotlib 2.1.1|
| | keras 2.1.2| 
| | bleach 1.5.0|


LUCID is easier to set up, so as long as you install the latest version of Tensorflow, Pyshark, and Tshark, then the model should run just fine. I left the other dependencies in for the sake of completeness.

The dependencies needed for MAD-GAN were rather complicated. During training, I set up an environment with exact dependencies as shown in the table above. These requirements can't be satisfied however when using the model on a Raspberry Pi 4 (possibly because they are unsupported by the OS?), which is why I used a different environment and modified the anomaly detection script (AD.py) so it will work on the newer depedencies. I can't guarantee that the training script will work as that is not tested yet.

## How MAD-GAN & LUCID works
Dr. Doriguzzi-Corin did a fantastic job at explaining this in his repo (link above), so please refer to that if you would like to run LUCID :D

As for MAD-GAN, it is a bit more complicated. In a nutshell, you would normally run the following:
Training: `python3 RGAN.py swat_test`

## Adapting MAD-GAN to other datasets
Since I changed MAD-GAN scripts so that it will work on CICDDoS2017 & CICDDoS2019, I've uploaded both MAD-GAN (training) and MAD-GAN (testing) here for your convenience. 


The trick to adapting MAD-GAN for training other model is to modify the 

## Adapting LUCID to other datasets
I made no changes to the LUCID model, however note that it is tightly implemented for the TCP/IP protocol. As long as LUCID can correctly label data as benign or traffic using the 5-tuple (source IP, source port, destination IP, destination port, protocol), LUCID should works with any dataset. See this issue here for more information:
https://github.com/doriguzzi/lucid-ddos/issues/7
