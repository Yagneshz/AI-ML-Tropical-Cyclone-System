"""Step 11 train/infer next latitude-longitude track forecasts."""
import argparse
from cyclone_forecasting.core import predict,train
def main():
 p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='command',required=True); t=sub.add_parser('train'); t.add_argument('--data',required=True); t.add_argument('--lookback',type=int,default=4); t.add_argument('--epochs',type=int,default=50); t.add_argument('--output',default='models/track_lstm.pt'); q=sub.add_parser('predict'); q.add_argument('--checkpoint',default='models/track_lstm.pt'); q.add_argument('--history',required=True,help='semicolon-separated feature rows'); a=p.parse_args()
 if a.command=='train': print(train(a.data,['LAT_IBTRACS','LON_IBTRACS','USA_WIND','USA_PRES'],['LAT_IBTRACS','LON_IBTRACS'],a.output,lookback=a.lookback,epochs=a.epochs))
 else: print(predict(a.checkpoint,[[float(v) for v in row.split(',')] for row in a.history.split(';')]))
if __name__=='__main__': main()
