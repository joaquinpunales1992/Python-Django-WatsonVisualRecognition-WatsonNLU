from django.shortcuts import render, redirect
from .models import Articulo
from .forms import FormularioArticulo
import json
from watson_developer_cloud import VisualRecognitionV3, NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features



def home(request):
    vArticulos = Articulo.objects.order_by('-fechaPublicacion')
    form = FormularioArticulo()
    return render(request, 'core/inicio.html', {'articulos': vArticulos, 'form': form})


def publicarArticulo(request):
    if request.method == 'POST':
        form = FormularioArticulo(request.POST, request.FILES)
        if form.is_valid():
            vFormTemporal = form.save(commit=False)
            vClaseWatsonVR, vScoreWatsonVR = clasificarImagen(request.FILES['imagen'])
            vMarcaSelecccionada = request.POST.get('marca')
            vResultadoValidacionMarca = validarObjetoDetectado(vClaseWatsonVR, vMarcaSelecccionada)
            vFormTemporal.resWatsonClase = vClaseWatsonVR
            vFormTemporal.resWatsonScore = vScoreWatsonVR
            vFormTemporal.resWatsonValidacionMarca = vResultadoValidacionMarca
            vResultadoClasificacionDescripcion = clasificarDescripcion(request.POST.get('descripcion'))
            vFormTemporal.resWatsonClasificacionDescripcion = vResultadoClasificacionDescripcion
            vFormTemporal.save()
            return redirect('home')
    else:
        form = FormularioArticulo()
    return render(request, 'core/publicar_articulo_form.html', {'form': form })

##Watson VR
def clasificarImagen(pUrlImagen):
    # if 'VCAP_SERVICES' in os.environ:
    #     services = json.loads(os.getenv('VCAP_SERVICES'))

    with open('AutosClasificados\core\config.json') as json_data_file:
        vConfig = json.load(json_data_file)
        vAPIVersion = vConfig["watsonVisualRecognition"]["vAPIVersion"]
        vAPIKey = vConfig["watsonVisualRecognition"]["vAPIKey"]
        vAPIClasificador = vConfig["watsonVisualRecognition"]["vIdClasificador"]

    vVisualRecognition = VisualRecognitionV3(vAPIVersion, api_key=vAPIKey)
    vResultado = json.loads(json.dumps(vVisualRecognition.classify(images_file=pUrlImagen, classifier_ids=vAPIClasificador), indent=2))
    vClase = 'Imagen No detectada'
    vScore = -1
    try:
        for vImagen in vResultado['images']:
            for vClasificador in vImagen['classifiers']:
                for vClases in vClasificador['classes']:
                    if vClases['score'] > vScore:
                        vClase = vClases['class']
                        vScore = vClases['score']

        return vClase, vScore
    except:
        vClase = 'Imagen No detectada'
        vScore = -1
        return vClase, vScore


def validarObjetoDetectado(pClase, pMarcaSeleccionada):
    if str(pClase).lower() == str(pMarcaSeleccionada).lower():
        return True
    else:
        return False


#Watson NLC
def clasificarDescripcion(pDescripcion):
    # if 'VCAP_SERVICES' in os.environ:
    #     services = json.loads(os.getenv('VCAP_SERVICES'))
    with open('AutosClasificados\core\config.json') as json_data_file:
        vConfig = json.load(json_data_file)
        vAPIUserNLU= vConfig["watsonNLU"]["vAPIUser"]
        vAPIPassNLU = vConfig["watsonNLU"]["vAPIPass"]
        vAPIVersionNLU = vConfig["watsonNLU"]["vAPIVersion"]
        vUmbralMinScore_WNLU = vConfig["watsonNLU"]["vUmbralMinScore_WNLU"]
        vUmbralMinDescripcion = vConfig["otros"]["vUmbralMinDescripcion"]
    vResultado_NLU = ''
    vWatson_NLU = NaturalLanguageUnderstandingV1(username=vAPIUserNLU, password=vAPIPassNLU, version=vAPIVersionNLU)
    vListaKeywords = list()
    try:
        if len(pDescripcion) > vUmbralMinDescripcion:
            vResultado_NLU = vWatson_NLU.analyze(
                                          text=pDescripcion,
                                          features=[
                                             Features.Entities(
                                                               emotion=True,
                                                               sentiment=True,
                                                               limit=6
                                                               ),
                                             Features.Keywords(
                                                              emotion=True,
                                                              sentiment=True,
                                                              limit=6
                                                             )
                                          ],
                                          language="en"
                                        )

            vResultado_NLU = json.loads(json.dumps(vResultado_NLU, indent=2))

            if vResultado_NLU['keywords']:
                for entitien in vResultado_NLU['entities']:
                    print(entitien)
                for vResultado in vResultado_NLU['keywords']:
                    print(vResultado)
                    if vResultado['relevance'] > vUmbralMinScore_WNLU:
                        vListaKeywords.append(vResultado['text'])
                return vListaKeywords
    except:
            vListaKeywords.append('No hay Keywords disponibles')
            return vListaKeywords


