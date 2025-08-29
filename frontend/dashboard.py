import pandas as pd 
import sys
sys.path.append('/Users/aarontang/Desktop/Projects/Video Game Rating Forecast ')
from backend.model import feature_engineer, init_model, model_predict

model = init_model()
model_predict(['Shooter'], ['Drama'],"Electronic Arts", model)
