"""Train an LSTM to predict next-step numerical cyclone state."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn

class LSTMForecaster(nn.Module):
    def __init__(self,n): super().__init__(); self.lstm=nn.LSTM(n,64,batch_first=True); self.head=nn.Linear(64,n)
    def forward(self,x): return self.head(self.lstm(x)[0][:,-1])

def main():
    p=argparse.ArgumentParser(); p.add_argument('--data',required=True); p.add_argument('--features',default='LAT_IBTRACS,LON_IBTRACS,USA_WIND,USA_PRES'); p.add_argument('--group',default='SID'); p.add_argument('--time',default='TIME'); p.add_argument('--lookback',type=int,default=4); p.add_argument('--epochs',type=int,default=30); p.add_argument('--output',default='models/temporal_lstm.pt'); a=p.parse_args()
    df=pd.read_csv(a.data); cols=a.features.split(','); df=df.sort_values([a.group,a.time]); values=df[cols].apply(pd.to_numeric,errors='coerce').dropna(); mean,std=values.mean().values,values.std().replace(0,1).values; rows=[]
    for _,g in df.groupby(a.group):
        v=g[cols].apply(pd.to_numeric,errors='coerce').dropna().values
        for i in range(a.lookback,len(v)): rows.append(((v[i-a.lookback:i]-mean)/std,(v[i]-mean)/std))
    if not rows: raise ValueError('Not enough complete sequences')
    x=torch.tensor(np.stack([r[0] for r in rows]),dtype=torch.float32); y=torch.tensor(np.stack([r[1] for r in rows]),dtype=torch.float32); m=LSTMForecaster(len(cols)); opt=torch.optim.Adam(m.parameters(),lr=1e-3)
    for _ in range(a.epochs): opt.zero_grad(); loss=nn.functional.mse_loss(m(x),y); loss.backward(); opt.step()
    Path(a.output).parent.mkdir(parents=True,exist_ok=True); torch.save({'state':m.state_dict(),'features':cols,'lookback':a.lookback,'mean':mean,'std':std},a.output)
if __name__=='__main__': main()
