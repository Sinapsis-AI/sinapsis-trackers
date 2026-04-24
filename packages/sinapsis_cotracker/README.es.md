<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis CoTracker
<br/></h1>
<h4 align="center">Plantillas para seguimiento y visualización multiobjeto utilizando el modelo CoTracker</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features"> 🚀 Características</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#license"> 🔍 Licencia </a>


El <code>siinapsis-cotracker</code> proporciona una aplicación robusta y flexible para el seguimiento multiobjeto utilizando el <a href="https://cotracker3.github.io/"><strong>CoTracker</strong></a> modelo. Permite a los usuarios configurar y ejecutar fácilmente <strong>oleoductos de seguimiento</strong> para tareas de procesamiento y visualización de entradas de vídeo.

<h2 id="installation"> 🐍 Instalación </h2>

Instala el administrador de paquetes de tu elección. Alentamos el uso de <code>uv</code>



<blockquote>

[!IMPORTANT]
 <code>cotracker</code> la dependencia es necesaria para instalar <code>sinapsis-cotracker</code>

</blockquote>
<h4> Instrucciones UV</h4>
Instale cotracker en su entorno de trabajo como sigue:

```bash
uv pip install git+https://github.com/facebookresearch/co-tracker.git
```

entonces instalar sinapsis-cotracker

```bash
uv pip install sinapsis-cotracker --extra-index-url https://pypi.sinapsis.tech
```
<h4> Instrucciones de pip crudas</h4>
Instale cotracker en su entorno de trabajo como sigue:

```bash
pip install git+https://github.com/facebookresearch/co-tracker.git
```

entonces instalar sinapsis-cotracker

```bash
pip install sinapsis-cotracker --extra-index-url https://pypi.sinapsis.tech
```
<h2 id="features">🚀 Características</h2><h3> Plantillas soportadas</h3>
El <strong>Sinapsis CoTracker</strong> módulo ofrece un conjunto de plantillas para seguimiento y visualización de múltiples objetos utilizando el <strong>CoTracker</strong> modelo. Estas plantillas permiten a los usuarios realizar un seguimiento tanto en línea como fuera de línea, procesar entradas de vídeo y visualizar resultados de seguimiento en marcos de vídeo. Las plantillas en este paquete incluyen funcionalidad para:
<ul>
<li><strong>CoTrackerOffline</strong>: Maneja el seguimiento multiobjeto sin conexión para videos cortos. Carga todo el vídeo en memoria para el procesamiento y es el método más simple para tareas offline.</li>

<li><strong>CoTrackerOfflineLarge</strong>: Proporciona seguimiento sin conexión para videos largos utilizando un motor incremental eficiente en memoria.</li>

<li><strong>CoTrackerOnline</strong>: Admite el seguimiento de objetos en tiempo real con consultas de cuadrícula avanzada y funciones de cuadrícula de soporte.</li>

<li><strong>CoTrackerVisualizer</strong>: Visualiza resultados de seguimiento con traza personalizable, ancho de línea y modos de visualización.</li>
</ul>
<blockquote>

[! TIP]
Usa el comando de CLI <code>sinapsis info --all-template-names</code> para mostrar una lista con todos los nombres disponibles de Plantillas instalados con Sinapsis CoTracker.

[! TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo Agente config para la Plantilla especificado en <strong><em>TEMPLATE_NAME</em></strong>.

</blockquote>

Por ejemplo, para <strong><em>CoTrackerOffline</em></strong> usa <code>sinapsis info --example-template-config CoTrackerOffline</code> para producir el siguiente ejemplo de configuración:

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: CoTrackerOffline
  class_name: CoTrackerOffline
  template_input: InputTemplate
  attributes:
    device: '`replace_me:typing.Literal[''cuda'', ''cpu'']`'
    generic_key_field: CoTrackerResults
    model_cache_dir: /home/cv/.cache/sinapsis
    model_variant: '`replace_me:typing.Literal[''baseline'', ''scaled'']`'
    use_segmentation_mask: false
    grid_size: '`replace_me:<class ''int''>`'
    grid_query_frame: 0
    backward_tracking: false
```


<details><summary><strong><span style="font-size: 1.25em;">📚 Ejemplo de uso</span></strong></summary>
</details>


A continuación se muestra un ejemplo de configuración YAML para procesar un archivo de vídeo y visualizar resultados de seguimiento utilizando <strong>Sinapsis CoTracker</strong> plantillas. Esta configuración carga un vídeo con el <strong>VideoReaderCV2</strong>, realiza el seguimiento de objetos en tiempo real con el <strong>CoTrackerOnline</strong> plantilla, visualiza los resultados con el <strong>CoTrackerVisualizer</strong>, y guarda la salida como un nuevo archivo de vídeo usando el <strong>VideoWriterCV2</strong>.

<details><summary><strong><span style="font-size: 1.4em;">Config</span></strong></summary>
</details>


```yaml
agent:
  name: cotracker_agent

templates:
  - template_name: InputTemplate
    class_name: InputTemplate
    attributes: {}

  - template_name : VideoReaderCV2
    class_name: VideoReaderCV2
    template_input: InputTemplate
    attributes:
      video_file_path : "artifacts/palace.mp4"
      batch_size: 16

  - template_name: CoTrackerOnline
    class_name: CoTrackerOnline
    template_input: VideoReaderCV2
    attributes:
      model_variant: baseline
      device: cuda
      grid_size: 15

  - template_name: CoTrackerVisualizer
    class_name: CoTrackerVisualizer
    template_input: CoTrackerOnline
    attributes:
      device : cuda
      linewidth: 3
      overwrite: true

  - template_name: VideoWriterCV2
    class_name: VideoWriterCV2
    template_input: CoTrackerVisualizer
    attributes:
      destination_path: "artifacts/result.mp4"
      height: -1
      width: -1
      fps: 30
```



Esta configuración define un <strong>Agente</strong> y una secuencia de <strong>plantillas</strong> para procesamiento de vídeo, seguimiento de objetos y visualización.

<strong>IMPORTANTE</strong>: Las plantillas VideoReaderCV2 y VideoWriterCV2 forman parte de las <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers">sinapsis-data-readers</a> y <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers">sinapsis-data-writers</a> paquetes, respectivamente. Para utilizar este ejemplo, asegúrese de que ha instalado estos paquetes.

Para ejecutar la configuración, utilice el CLI:

```bash
sinapsis run name_of_config.yml
```


<h2 id="documentation">📙 Documentación</h2>
La documentación para este y otros paquetes de sinapsis está disponible en <a href="https://docs.sinapsis.tech/docs">web de sinapsis</a>

Los tutoriales para diferentes proyectos dentro de sinapsis están disponibles en <a href="https://docs.sinapsis.tech/tutorials">sinapsis tutoriales página</a>
<h2 id="license">🔍 Licencia</h2>
Este proyecto está licenciado bajo la licencia AGPLv3, que fomenta la colaboración abierta y el intercambio. Para más detalles, consulta el archivo <a href="LICENSE">LICENSE</a>.

Para uso comercial, consulta el  <a href="https://sinapsis.tech"> sitio web oficial de Sinapsis</a> para información sobre la obtención de una licencia comercial.

