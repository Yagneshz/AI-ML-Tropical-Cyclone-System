"""Step 12: write reproducible performance summaries for pipeline outputs."""
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score,mean_absolute_error,mean_squared_error,precision_recall_fscore_support
def haversine(lat1,lon1,lat2,lon2):
 r=6371.; p=np.pi/180; a=np.sin((lat2-lat1)*p/2)**2+np.cos(lat1*p)*np.cos(lat2*p)*np.sin((lon2-lon1)*p/2)**2; return 2*r*np.arcsin(np.sqrt(a))
def main():
 p=argparse.ArgumentParser(); p.add_argument('--data',required=True); p.add_argument('--task',choices=['classification','regression','track'],required=True); p.add_argument('--actual',required=True,help='column, or lat,lon for track'); p.add_argument('--predicted',required=True,help='column, or lat,lon for track'); p.add_argument('--output',default='data/processed/evaluation/metrics.json'); a=p.parse_args(); d=pd.read_csv(a.data); actual=a.actual.split(','); predicted=a.predicted.split(',')
 if a.task=='classification':
  pr,re,f1,_=precision_recall_fscore_support(d[actual[0]],d[predicted[0]],average='weighted',zero_division=0); result={'accuracy':accuracy_score(d[actual[0]],d[predicted[0]]),'precision_weighted':pr,'recall_weighted':re,'f1_weighted':f1}
 elif a.task=='regression': result={'mae':mean_absolute_error(d[actual[0]],d[predicted[0]]),'rmse':mean_squared_error(d[actual[0]],d[predicted[0]])**.5}
 else:
  error=haversine(d[actual[0]].to_numpy(),d[actual[1]].to_numpy(),d[predicted[0]].to_numpy(),d[predicted[1]].to_numpy()); result={'mean_track_error_km':float(error.mean()),'median_track_error_km':float(np.median(error))}
 out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)); print(result)
if __name__=='__main__': main()
