"""Step 8 train or score cyclone categories from deep features."""
import argparse,pickle
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
def categories(wind):
 return pd.cut(pd.to_numeric(wind,errors='coerce'),[-1,33,63,82,95,112,float('inf')],labels=['disturbance','tropical_storm','cat_1','cat_2','cat_3','cat_4_plus']).astype(str)
def main():
 p=argparse.ArgumentParser(); s=p.add_subparsers(dest='command',required=True); t=s.add_parser('train'); t.add_argument('--features',default='data/processed/features/image_features.npy'); t.add_argument('--metadata',default='data/processed/features/feature_metadata.csv'); t.add_argument('--label-column'); t.add_argument('--model',default='models/cyclone_category_mlp.pkl'); q=s.add_parser('predict'); q.add_argument('--features',default='data/processed/features/image_features.npy'); q.add_argument('--metadata',default='data/processed/features/feature_metadata.csv'); q.add_argument('--model',default='models/cyclone_category_mlp.pkl'); q.add_argument('--output',default='data/processed/classification/cyclone_categories.csv'); a=p.parse_args(); x=np.load(a.features); m=pd.read_csv(a.metadata)
 if a.command=='train':
  y=m[a.label_column].astype(str) if a.label_column else categories(m['USA_WIND'])
  if y.isna().any() or y.nunique()<2: raise ValueError('Provide a complete multi-class label column or USA_WIND.')
  tr,te=train_test_split(np.arange(len(y)),test_size=.2,random_state=42,stratify=y); model=MLPClassifier((128,64),max_iter=300,early_stopping=True,random_state=42).fit(x[tr],y.iloc[tr]); print(classification_report(y.iloc[te],model.predict(x[te]),zero_division=0)); Path(a.model).parent.mkdir(parents=True,exist_ok=True); pickle.dump(model,open(a.model,'wb'))
 else:
  model=pickle.load(open(a.model,'rb')); out=m.copy(); out['predicted_category']=model.predict(x); out['category_confidence']=model.predict_proba(x).max(1); Path(a.output).parent.mkdir(parents=True,exist_ok=True); out.to_csv(a.output,index=False)
if __name__=='__main__': main()
