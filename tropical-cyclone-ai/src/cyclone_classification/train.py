"""Train a dense classifier from step-7 features and emit category predictions."""
import argparse
import pickle
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

def main():
    p=argparse.ArgumentParser(); p.add_argument('--features',default='data/processed/features/image_features.npy'); p.add_argument('--metadata',default='data/processed/features/feature_metadata.csv'); p.add_argument('--label-column',required=True); p.add_argument('--model',default='models/cyclone_classifier.pkl'); p.add_argument('--output',default='data/processed/classification/predictions.csv'); a=p.parse_args()
    x=np.load(a.features); meta=pd.read_csv(a.metadata)
    if a.label_column not in meta: raise ValueError(f'Missing label column: {a.label_column}')
    y=meta[a.label_column].astype(str); tr,te=train_test_split(np.arange(len(y)),test_size=.2,random_state=42,stratify=y)
    clf=MLPClassifier(hidden_layer_sizes=(128,64),max_iter=300,early_stopping=True,random_state=42).fit(x[tr],y.iloc[tr])
    print(classification_report(y.iloc[te],clf.predict(x[te]),zero_division=0)); Path(a.model).parent.mkdir(parents=True,exist_ok=True)
    with open(a.model,'wb') as f: pickle.dump(clf,f)
    out=meta.copy(); out['predicted_category']=clf.predict(x); out['category_confidence']=clf.predict_proba(x).max(1); Path(a.output).parent.mkdir(parents=True,exist_ok=True); out.to_csv(a.output,index=False)
if __name__=='__main__': main()
