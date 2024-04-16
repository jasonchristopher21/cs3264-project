# Meteoblue Extractor

This program scrapes off images from Meteoblue's public API and processes each coordinate. 

## CAUTION

1. The output file may contain **coordinates outside of Singapore**, i.e. Johor Bahru, Singapore waters and Singapore nearby islands. Please keep this in mind when designing the models

2. It processes at batches of 10 x 10 pixels (i.e. stride = 10). 

3. Data is taken to be the closest out of a scale of ~ 15 temperature gaps, considering runtime. Linear interpolation was not implemented yet, so it is currently kind of "quantised". A bit rushed to form a working model first

## Running the Extractor

To run the extractor, you can simply run 

```bash
python image_extractor_script_copy.py
```

The output will be written as a csv file called `output.csv` in this same directory
