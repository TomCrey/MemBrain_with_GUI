#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate MemBrain
python MemBrain_pipeline.py
conda deactivate

