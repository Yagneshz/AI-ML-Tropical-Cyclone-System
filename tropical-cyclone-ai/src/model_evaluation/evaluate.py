"""Evaluate classification, intensity, or geographic track predictions."""
import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, mean_squared_error

def main():
    p=argparse.ArgumentParser(); p.add_argument('--data',required=True); p.add_argument('--actual',required=True); p.add_argument('--predicted',required=True); p.add_argument('--task',choices=['classification','regression','track'],required=True); a=p.parse_args(); d=pd.read_csv(a.data)
    if a.task=='classification': print(classification_report(d[a.actual],d[a.predicted],zero_division=0)); print('accuracy=',accuracy_score(d[a.actual],d[a.predicted])); return
    actual=d[a.actual].to_numpy(); predicted=d[a.predicted].to_numpy(); print('mae=',mean_absolute_error(actual,predicted),'rmse=',mean_squared_error(actual,predicted)**.5)
    if a.task=='track': print('Mean coordinate error (degrees)=',np.mean(np.linalg.norm(actual-predicted,axis=1)))
if __name__=='__main__': main()
