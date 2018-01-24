from django.test import TestCase

# Create your tests here.

import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features


natural_language_understanding = NaturalLanguageUnderstandingV1(
                                                                  username="e477af0a-db2f-4753-8b2d-14a084e607cf",
                                                                  password="qbHBxkSPhwPA",
                                                                  version="2017-10-03")


response = natural_language_understanding.analyze(
  text="bmw Serie 1 Pack M Ùnico Dueño (mejor Que Nuevo)   Bmw Serie 1 120i M 2016   Vendo BMW F20 120iM 2016 14000km. En garantía.   Ficha Motor haus.   Patente anual 2017 paga.   Tratamiento protector vitrocerámico en barniz.   Motor y Transmisión:  Motor 1.6 nafta de 4 cilindros con inyección directa Twin Power Turbo.  Potencia máxima 177 HP/130 KW a 4.800 RPM y 250 NM/184 lb-ft de torque entre 1.500 y 4.500 RPM.  Caja de cambios automática / secuencial marca ZF de 8 velocidades, la cual cuenta con 3 opciones de conducción: Automática Drive, Automática Sport y Manual.  Sistema de Start & Stop con recuperación de energía de frenado.  BMW Driving Experience Control, 4 modos de manejo que cambian parámetros del auto, tales como reacción del acelerador, dureza de la dirección y suspensión. Modos: Eco Pro, Confort, Sport y Sport +  Bloqueo eléctrico de diferencial.  Suspensión independiente multi-link trasera.   Performance  0 a 100 km en 7.2 segundos.  225 km/h de velocidad máxima.  Consumo promedio 15 km/lt ",
  features=[
    Features.Entities(
      emotion=True,
      sentiment=True,
      limit=2
    ),
    Features.Keywords(
      emotion=True,
      sentiment=True,
      limit=6
    )
  ]
)



print(json.dumps(response['keywords'], indent=2))



