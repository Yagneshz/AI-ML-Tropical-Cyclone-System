"""Step 9 production temporal-state model."""
import argparse
from cyclone_forecasting.core import train
def main():
 p=argparse.ArgumentParser(); p.add_argument('--data',required=True); p.add_argument('--features',default='LAT_IBTRACS,LON_IBTRACS,USA_WIND,USA_PRES'); p.add_argument('--targets',default='LAT_IBTRACS,LON_IBTRACS,USA_WIND,USA_PRES'); p.add_argument('--lookback',type=int,default=4); p.add_argument('--epochs',type=int,default=50); p.add_argument('--output',default='models/temporal_state_lstm.pt'); a=p.parse_args(); print(train(a.data,a.features.split(','),a.targets.split(','),a.output,lookback=a.lookback,epochs=a.epochs))
if __name__=='__main__': main()
