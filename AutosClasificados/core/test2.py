import json


#json = {{"watsonVisualRecognition":{"vAPIKey": "868b9f7ba1beb9cd3ef77236760fea74bac9af26", "vAPIVersion": "2016-05-20", "vIdClasificador": "vehiculos_260725218", "vUmbralMinScore_WVR": 0.5}, "watsonNLU":{"preprocessing_queue":{"vAPIUser": "e477af0a-db2f-4753-8b2d-14a084e607cf", "vAPIPass": "qbHBxkSPhwPA","vAPIVersion": "2017-10-03", "vUmbralMinScore_WNLU": 0.1}, "otros":{"vUmbralMinDescripcion": 10}}}}

with open('AutosClasificados\core\config.json') as json_data_file:
    vConfig = json.load(json_data_file)
    vAPIVersion = vConfig["watsonVisualRecognition"]["vAPIVersion"]
    vAPIKey = vConfig["watsonVisualRecognition"]["vAPIKey"]
    vAPIClasificador = vConfig["watsonVisualRecognition"]["vIdClasificador"]
