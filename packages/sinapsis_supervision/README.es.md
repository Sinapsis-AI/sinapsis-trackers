<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis Supervision
<br/></h1>
<h4 align="center">Plantillas para seguimiento multiobjeto utilizando el modelo ByteTrack</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features"> 🚀 Características</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#license"> 🔍 Licencia </a>


El módulo <code>sinapsis-supervision</code> ofrece una aplicación potente y flexible para el seguimiento multiobjeto utilizando el <a href="https://github.com/ifzhang/ByteTrack"><strong>ByteTrack</strong></a> algoritmo. Permite a los usuarios configurar y ejecutar fácilmente <strong>oleoductos de seguimiento</strong> para el procesamiento de entrada de vídeo, detección de objetos y tareas de seguimiento.

<h2 id="installation"> 🐍 Instalación </h2>

Instala el administrador de paquetes de tu elección. Alentamos el uso de <code>uv</code>


Ejemplo con <code>uv</code>:



```bash
  uv pip install sinapsis-supervision --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-supervision --extra-index-url https://pypi.sinapsis.tech
```
<h2 id="features">🚀 Características</h2><h3> Plantillas soportadas</h3>
El <strong>Sinapsis ByteTrack</strong> módulo proporciona una plantilla para seguimiento multiobjeto utilizando el <strong>ByteTrack</strong> algoritmo. Actualmente, el paquete incluye la siguiente plantilla:
<ul>
<li><strong>ByteTrack</strong>: Una plantilla para rastrear objetos a través de marcos de vídeo, con parámetros personalizables para la activación de la pista, umbrales de coincidencia y manejo de oclusión.</li>
</ul>
<blockquote>

[! TIP]
Usa el comando de CLI <code>sinapsis info --all-template-names</code> para mostrar una lista con todos los nombres disponibles de Plantillas instalados con Sinapsis Supervision.

[! TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo Agente config para la Plantilla especificado en <strong><em>TEMPLATE_NAME</em></strong>.

</blockquote>

Por ejemplo, para <strong><em>ByteTrack</em></strong> usa <code>sinapsis info --example-template-config ByteTrack</code> para producir el siguiente ejemplo de configuración:

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: ByteTrack
  class_name: ByteTrack
  template_input: InputTemplate
  attributes:
    track_activation_threshold: 0.2
    lost_track_buffer: 30
    minimum_matching_threshold: 0.7
    frame_rate: 30
    minimum_consecutive_frames: 1
```


<details><summary><strong><span style="font-size: 1.25em;">📚 Ejemplo de uso</span></strong></summary>
</details>


A continuación se muestra un ejemplo de configuración YAML para procesar un archivo de vídeo y visualizar los resultados de seguimiento utilizando el <strong>Sinapsis Supervision</strong> plantilla. Esta configuración carga un vídeo con el <strong>VideoReaderCV2</strong>, realiza detección de objetos y seguimiento en tiempo real con el <strong>UltralyticsPredict</strong> y <strong>ByteTrack</strong> plantillas, dibujar cajas de fijación alrededor de objetos detectados con los <strong>BBoxDrawer</strong>, y guarda la salida como un nuevo archivo de vídeo usando el <strong>VideoWriterCV2</strong>.


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



Esta configuración define un <strong>Agente</strong> y una secuencia de <strong>plantillas</strong> para procesamiento de vídeo, detección de objetos, seguimiento en tiempo real y visualización.

<strong>IMPORTANTE</strong>: Las plantillas de VideoReaderCV2, BBoxDrawer y VideoWriterCV2 forman parte de las <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers">sinapsis-data-readers</a>, <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_visualization">sinapsis-data-visualization</a>, y <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers">sinapsis-data-writers</a> paquetes, respectivamente. Para utilizar este ejemplo, asegúrese de que ha instalado estos paquetes.

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

