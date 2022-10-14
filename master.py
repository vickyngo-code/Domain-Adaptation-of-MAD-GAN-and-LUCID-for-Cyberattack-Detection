import tensorflow as tf
import numpy as np
import os

class master():
  # constructor
  
 # window time interval mechanism process in (pcap/json/csv) format, so live/offline prediction is both fine
 def train_fresh():
    #skip
 
 def re_train():
    
 def detect_offline():
    # input file + model -> results
    
 def detect_live():
    # call data receiving on chosen ports.
    # call method to collect data for storage.
    
 def 
  
 def main(argv):
  # syntax [must] (optional)
  # Assume name is 'anon'
  # anon [start/stop] [source model] [active time] [port/ip] (window interval)
  help_string = 'Usage: python3 lucid_cnn.py --train <dataset_folder> -e <epocs>'

    parser = argparse.ArgumentParser(
        description='DDoS attacks detection',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   
    
    # training param
    parser.add_argument('-a', '--action', nargs='+', type=str,
                        help='train/retrain/detect')

    parser.add_argument('-e', '--epochs', default=0, type=int,
                        help='Training iterations')

    parser.add_argument('-i', '--interval', default=1, type=int,
                        help='window interval length (seconds)')

    parser.add_argument('-m', '--model', type=str,
                        help='trained model')

    args = parser.parse_args()
    
    if args.train is 'train':
      # set default directory for model.
  
  # how to modify parameters while running?
  
