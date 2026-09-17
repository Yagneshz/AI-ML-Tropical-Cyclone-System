"""Step 7: extract features only from positive step-6 detections."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from cyclone_identification.dataset import CycloneImageDataset,load_manifest
from cyclone_identification.model import CycloneCNN
from cyclone_identification.transforms import image_transform
def main():
 p=argparse.ArgumentParser(); p.add_argument('--detections',required=True); p.add_argument('--checkpoint',required=True); p.add_argument('--output',default='data/processed/features'); p.add_argument('--threshold',type=float,default=.5); a=p.parse_args()
 frame=load_manifest(a.detections,False)
 if 'cyclone_probability' in frame: frame=frame[frame.cyclone_probability>=a.threshold].copy()
 if frame.empty: raise ValueError('No detections meet threshold.')
 c=torch.load(a.checkpoint,map_location='cpu',weights_only=True); m=CycloneCNN(); m.load_state_dict(c['model_state']); m.eval(); loader=DataLoader(CycloneImageDataset(frame,image_transform(c.get('image_size',256)),False),batch_size=32); result=[]
 with torch.no_grad():
  for x,_ in loader: result.append(torch.flatten(torch.nn.functional.adaptive_avg_pool2d(m.features(x),1),1).numpy())
 out=Path(a.output); out.mkdir(parents=True,exist_ok=True); np.save(out/'image_features.npy',np.vstack(result)); frame.to_csv(out/'feature_metadata.csv',index=False); print(f'Wrote {len(frame)} 256-dimensional feature vectors to {out}')
if __name__=='__main__': main()
