# Steps 7–12

Set `$env:PYTHONPATH='src'`. Run 7 after step-6 inference, then 8. Train 9 on `data/processed/fused_dataset/tcir_ibtracs_fused.csv`; steps 10 and 11 use its checkpoint. Step 12 evaluates output CSV columns.

```powershell
python -m feature_extraction.extract --manifest <image_manifest.csv> --checkpoint models/cyclone_cnn.pt
python -m cyclone_classification.train --label-column <category_column>
python -m temporal_model.train --data data/processed/fused_dataset/tcir_ibtracs_fused.csv
python -m intensity_prediction.predict --sequence "lat,lon,wind,pres;lat,lon,wind,pres;lat,lon,wind,pres;lat,lon,wind,pres"
python -m model_evaluation.evaluate --data <results.csv> --actual <actual_column> --predicted <prediction_column> --task classification
```
