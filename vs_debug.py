import os
os.environ['CUDA_VISIBLE_DEVICES'] = "-1"
os.system("python3 AD_Invert.py --settings_file swat_test")