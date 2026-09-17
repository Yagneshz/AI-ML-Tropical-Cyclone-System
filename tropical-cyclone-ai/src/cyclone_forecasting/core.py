"""Leakage-safe sequence preparation and neural next-state forecasting."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

class Forecaster(nn.Module):
    def __init__(self, features:int, targets:int):
        super().__init__(); self.rnn=nn.LSTM(features,96,batch_first=True,dropout=0 if features else .1); self.head=nn.Sequential(nn.Dropout(.2),nn.Linear(96,targets))
    def forward(self,x): return self.head(self.rnn(x)[0][:,-1])

def sequences(data, feature_cols, target_cols, group='SID', time='TIME', lookback=4):
    df=pd.read_csv(data); required=set(feature_cols+target_cols+[group,time]); missing=required-set(df.columns)
    if missing: raise ValueError(f'Missing input columns: {sorted(missing)}')
    df[time]=pd.to_datetime(df[time],errors='coerce'); rows=[]
    for storm,g in df.dropna(subset=[time]).sort_values([group,time]).groupby(group):
        x=g[feature_cols].apply(pd.to_numeric,errors='coerce').to_numpy(float); y=g[target_cols].apply(pd.to_numeric,errors='coerce').to_numpy(float)
        for end in range(lookback,len(g)):
            if np.isfinite(x[end-lookback:end]).all() and np.isfinite(y[end]).all(): rows.append((storm,x[end-lookback:end],y[end],g.iloc[end][time]))
    if not rows: raise ValueError('No complete sequences; verify columns and lookback.')
    return rows

def train(data, feature_cols, target_cols, output, group='SID', time='TIME', lookback=4, epochs=50, batch_size=64, seed=42):
    torch.manual_seed(seed); rows=sequences(data,feature_cols,target_cols,group,time,lookback); storms=np.array([r[0] for r in rows]); unique=np.unique(storms); rng=np.random.default_rng(seed); rng.shuffle(unique); cut=max(1,int(.8*len(unique))); train_storms=set(unique[:cut]); train_ix=np.array([s in train_storms for s in storms])
    raw=np.stack([r[1] for r in rows]); targets=np.stack([r[2] for r in rows]); mean=raw[train_ix].reshape(-1,len(feature_cols)).mean(0); std=raw[train_ix].reshape(-1,len(feature_cols)).std(0); std[std==0]=1
    target_mean=targets[train_ix].mean(0); target_std=targets[train_ix].std(0); target_std[target_std==0]=1
    x=(raw-mean)/std; y=(targets-target_mean)/target_std; model=Forecaster(len(feature_cols),len(target_cols)); opt=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=1e-4); loader=DataLoader(TensorDataset(torch.tensor(x[train_ix],dtype=torch.float32),torch.tensor(y[train_ix],dtype=torch.float32)),batch_size=batch_size,shuffle=True)
    for _ in range(epochs):
        model.train()
        for xb,yb in loader: opt.zero_grad(); loss=nn.functional.mse_loss(model(xb),yb); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad(): prediction=(model(torch.tensor(x,dtype=torch.float32)).numpy()*target_std)+target_mean
    test=~train_ix; metrics={'mae':float(np.abs(prediction[test]-targets[test]).mean()) if test.any() else None,'rmse':float(np.sqrt(((prediction[test]-targets[test])**2).mean())) if test.any() else None,'train_sequences':int(train_ix.sum()),'test_sequences':int(test.sum())}
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True); torch.save({'state':model.state_dict(),'feature_cols':feature_cols,'target_cols':target_cols,'lookback':lookback,'mean':mean,'std':std,'target_mean':target_mean,'target_std':target_std,'metrics':metrics},out)
    predictions=pd.DataFrame(prediction,columns=[f'predicted_{x}' for x in target_cols]); predictions.insert(0,'SID',storms); predictions['TIME']=[r[3] for r in rows]; predictions[[f'actual_{x}' for x in target_cols]]=targets; predictions['split']=np.where(train_ix,'train','test'); predictions.to_csv(out.with_suffix('.predictions.csv'),index=False); return metrics

def predict(checkpoint, history):
    c=torch.load(checkpoint,map_location='cpu',weights_only=True); a=np.asarray(history,dtype=float)
    if a.shape!=(c['lookback'],len(c['feature_cols'])): raise ValueError(f'Expected history shape ({c["lookback"]}, {len(c["feature_cols"])})')
    model=Forecaster(len(c['feature_cols']),len(c['target_cols'])); model.load_state_dict(c['state']); model.eval()
    with torch.no_grad(): result=model(torch.tensor(((a-c['mean'])/c['std'])[None],dtype=torch.float32)).numpy()[0]*c['target_std']+c['target_mean']
    return dict(zip(c['target_cols'],map(float,result)))
