"""Use the temporal model to predict wind speed and central pressure."""
import argparse
import torch
from temporal_model.train import LSTMForecaster

def main():
    p=argparse.ArgumentParser(); p.add_argument('--checkpoint',default='models/temporal_lstm.pt'); p.add_argument('--sequence',required=True,help='Comma-separated latest rows; one row per timestep, values in checkpoint feature order'); a=p.parse_args()
    c=torch.load(a.checkpoint,map_location='cpu',weights_only=True); n=len(c['features']); values=[[float(x) for x in row.split(',')] for row in a.sequence.split(';')]
    if len(values)!=c['lookback'] or any(len(r)!=n for r in values): raise ValueError(f'Provide {c["lookback"]} rows of {n} values')
    m=LSTMForecaster(n); m.load_state_dict(c['state']); m.eval(); x=(torch.tensor(values)-torch.tensor(c['mean']))/torch.tensor(c['std'])
    with torch.no_grad(): prediction=(m(x.unsqueeze(0))[0]*torch.tensor(c['std'])+torch.tensor(c['mean'])).tolist()
    print(dict(zip(c['features'],prediction)))
if __name__=='__main__': main()
