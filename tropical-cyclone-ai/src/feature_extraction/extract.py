"""Extract pooled CNN features from step-6 detections."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from cyclone_identification.dataset import CycloneImageDataset, load_manifest
from cyclone_identification.model import CycloneCNN
from cyclone_identification.transforms import image_transform

def main():
    p=argparse.ArgumentParser(); p.add_argument('--manifest',required=True); p.add_argument('--checkpoint',required=True); p.add_argument('--output',default='data/processed/features'); p.add_argument('--batch-size',type=int,default=32); a=p.parse_args()
    frame=load_manifest(a.manifest,False); ck=torch.load(a.checkpoint,map_location='cpu',weights_only=True); model=CycloneCNN(); model.load_state_dict(ck['model_state']); model.eval()
    loader=DataLoader(CycloneImageDataset(frame,image_transform(ck.get('image_size',256)),False),batch_size=a.batch_size); vectors=[]
    with torch.no_grad():
        for images,_ in loader: vectors.append(torch.flatten(torch.nn.functional.adaptive_avg_pool2d(model.features(images),1),1).numpy())
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True); np.save(out/'image_features.npy',np.vstack(vectors)); frame.to_csv(out/'feature_metadata.csv',index=False)
if __name__=='__main__': main()
