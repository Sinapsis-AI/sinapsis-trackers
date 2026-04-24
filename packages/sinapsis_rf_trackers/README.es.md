<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis Roboflow Trackers
<br/></h1>
<h4 align="center">Plantillas de seguimiento multiobjeto utilizando algoritmos SORT y DeepSORT alimentados por Roboflow</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features"> 🚀 Características</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#license"> 🔍 Licencia </a>


El  módulo <code>sinapsis-rf-trackers</code> proporciona implementaciones potentes y flexibles para el seguimiento multiobjeto utilizando <strong>SORT</strong> y <strong>DeepSORT</strong> algoritmos de los <strong>Biblioteca de rastreadores de Roboflow</strong>. Este paquete ofrece una integración perfecta con los flujos de trabajo de Sinapsis, permitiendo a los usuarios configurar y ejecutar fácilmente <strong>oleoductos de seguimiento</strong> para el procesamiento de entrada de vídeo, detección de objetos y tareas de seguimiento con varios backends detector.

<h2 id="installation"> 🐍 Instalación </h2>

Instala el administrador de paquetes de tu elección. Alentamos el uso de <code>uv</code>


Ejemplo con <code>uv</code>:



```bash
  uv pip install sinapsis-rf-trackers --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-rf-trackers --extra-index-url https://pypi.sinapsis.tech
```
<h3 id="optionaldependencies">Dependencias optativas</h3>
Para una completa funcionalidad con diferentes detectores y operaciones I/O:

```bash
# For Ultralytics YOLO detectors
uv pip install sinapsis-rf-trackers[sinapsis-ultralytics] --extra-index-url https://pypi.sinapsis.tech

# For DFINE detectors
uv pip install sinapsis-rf-trackers[sinapsis-dfine] --extra-index-url https://pypi.sinapsis.tech

# For video processing capabilities
uv pip install sinapsis-rf-trackers[sinapsis-data-readers,sinapsis-data-writers] --extra-index-url https://pypi.sinapsis.tech

# Install all dependencies
uv pip install sinapsis-rf-trackers[all] --extra-index-url https://pypi.sinapsis.tech
```
<h2 id="features">🚀 Características</h2><h3> Plantillas soportadas</h3>
El <strong>Sinapsis RF Trackers</strong> módulo proporciona Plantillas de Sinapsis que envuelven los algoritmos de rastreo probados de Roboflow para el seguimiento de múltiples objetos. El paquete aprovecha el <strong>Biblioteca de rastreadores de Roboflow</strong> para ofrecer un rendimiento de seguimiento de nivel empresarial con configuraciones fáciles de usar.

Actualmente, el paquete incluye las siguientes plantillas:
<ul>
<li>
<strong>SORTTrackerInference</strong>: Sencilla aplicación de algoritmos de seguimiento en línea y en tiempo real de Roboflow, con seguimiento basado en movimiento utilizando filtros Kalman y algoritmo húngaro para asociación de datos.


<details><summary>Atributos</summary>
</details>

<ul>
<li><code>track_activation_threshold</code> (Optional): Detection confidence threshold for track activation. Aumentar este valor mejora la precisión y la estabilidad, pero podría perderse las verdaderas detecciones. Disminuirlo aumenta la integridad, pero los riesgos de introducir ruido e inestabilidad (por defecto: <code>0.25</code>).</li>

<li><code>lost_track_buffer</code> (Opcional): Número de marcos para amortiguar cuando se pierde una pista. Aumentar este valor aumenta la manipulación de la oclusión, reduciendo significativamente la probabilidad de fragmentación o desaparición de las vías causadas por deficiencias breves de detección (por defecto: <code>30</code>).</li>

<li><code>frame_rate</code> (Opcional): La velocidad de marco de la secuencia de vídeo que se está procesando. Esto afecta la dinámica temporal del algoritmo de rastreo (por defecto: <code>30.0</code>).</li>

<li><code>minimum_consecutive_frames</code> (Opcional): Número de marcos consecutivos que un objeto debe ser rastreado antes de que se considere una pista 'válida'. Aumentar este valor impide la creación de pistas accidentales de detección falsa o doble detección, pero corre el riesgo de falta de pistas más cortas (por defecto: <code>3</code>).</li>

<li><code>minimum_iou_threshold</code> (Opcional): umbral mínimo de UI para asociar las detecciones con pistas. Los valores más altos requieren una mejor superposición espacial para la asociación, mejorando la precisión pero potencialmente reduciendo la memoria (por defecto: <code>0.3</code>).</li>
</ul>

</li>

<li>
<strong>DeepSORTTrackerInference</strong>: algoritmo SORT mejorado de Roboflow con características de aspecto profundo para mejorar la reidentificación y reducir los interruptores de identidad durante oclusaciones.


<details><summary>Atributos</summary>
</details>

<ul>
<li><code>track_activation_threshold</code> (Optional): Detection confidence threshold for track activation. Aumentar este valor mejora la precisión y la estabilidad, pero podría perderse las verdaderas detecciones. Disminuirlo aumenta la integridad, pero los riesgos de introducir ruido e inestabilidad (por defecto: <code>0.25</code>).</li>

<li><code>lost_track_buffer</code> (Opcional): Número de marcos para amortiguar cuando se pierde una pista. Aumentar este valor aumenta la manipulación de la oclusión, reduciendo significativamente la probabilidad de fragmentación o desaparición de las vías causadas por deficiencias breves de detección (por defecto: <code>30</code>).</li>

<li><code>frame_rate</code> (Opcional): La velocidad de marco de la secuencia de vídeo que se está procesando. Esto afecta la dinámica temporal del algoritmo de rastreo (por defecto: <code>30.0</code>).</li>

<li><code>minimum_consecutive_frames</code> (Opcional): Número de marcos consecutivos que un objeto debe ser rastreado antes de que se considere una pista 'válida'. Aumentar este valor impide la creación de pistas accidentales de detección falsa o doble detección, pero corre el riesgo de falta de pistas más cortas (por defecto: <code>3</code>).</li>

<li><code>minimum_iou_threshold</code> (Opcional): umbral mínimo de UI para asociar las detecciones con pistas. Los valores más altos requieren una mejor superposición espacial para la asociación, mejorando la precisión pero potencialmente reduciendo la memoria (por defecto: <code>0.3</code>).</li>

<li><code>appearance_threshold</code> (Optional): Threshold for appearance-based matching. Los valores más altos hacen que el rastreador sea más conservador en apariencia igualando, reduciendo los interruptores de identidad pero potencialmente perdiendo pistas durante occlusiones (por defecto: <code>0.7</code>).</li>

<li><code>appearance_weight</code> (Opcional): Peso de las características de apariencia versus las características de movimiento en el costo de asociación. Valores más altos priorizan la coincidencia de apariencia, valores inferiores priorizan la consistencia del movimiento (por defecto: <code>0.5</code>).</li>

<li><code>distance_metric</code> (Opcional): métrica de distancia para la comparación de características de apariencia. Las métricas soportadas incluyen 'cosina' y 'euclidean'. La distancia cosina es generalmente más robusta para las características de apariencia (por defecto: <code>"cosine"</code>).</li>

<li><code>reid_model_name</code> (Opcional): Nombre del modelo ReID para usar. Debe ser compatible con biblioteca de timm o formato de modelo personalizado (por defecto: <code>"tf_efficientnet_b1.in1k"</code>).</li>

<li><code>reid_device</code> (Opcional): Dispositivo para ejecutar la extracción de características. CUDA proporciona una inferencia más rápida pero requiere disponibilidad de GPU. Opciones: <code>"auto"</code>, <code>"cuda"</code>, <code>"cpu"</code> (por defecto: <code>"auto"</code>).</li>

<li><code>reid_get_pooled_features</code> (Opcional): Ya sea para usar las características combinadas del modelo Re-ID (por defecto: <code>true</code>).</li>

<li><code>reid_kwargs</code> (Optional): Otros argumentos de palabras clave para pasar al constructor modelo Re-ID.</li>
</ul>

</li>
</ul>
<blockquote>

[! TIP]
Usa el comando de CLI <code>sinapsis info --all-template-names</code> para mostrar una lista con todos los nombres de plantilla disponibles instalados con Sinapsis RF Trackers.

[! TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo Agente config para la Plantilla especificado en <strong><em>TEMPLATE_NAME</em></strong>.

</blockquote>

Por ejemplo, para <strong><em>SORTTrackerInference</em></strong> usa <code>sinapsis info --example-template-config SORTTrackerInference</code> para producir el siguiente ejemplo de configuración:

```yaml
agent:
  name: sort_tracker_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: SORTTrackerInference
  class_name: SORTTrackerInference
  template_input: InputTemplate
  attributes:
    track_activation_threshold: 0.25
    lost_track_buffer: 30
    minimum_consecutive_frames: 3
    minimum_iou_threshold: 0.3
    frame_rate: 30
```

Para <strong><em>DeepSORTTrackerInference</em></strong> usa <code>sinapsis info --example-template-config DeepSORTTrackerInference</code> para producir el siguiente ejemplo de configuración:

```yaml
agent:
  name: deepsort_tracker_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: DeepSORTTrackerInference
  class_name: DeepSORTTrackerInference
  template_input: InputTemplate
  attributes:
    track_activation_threshold: 0.25
    lost_track_buffer: 30
    minimum_consecutive_frames: 3
    minimum_iou_threshold: 0.3
    frame_rate: 30
    appearance_threshold: 0.7
    appearance_weight: 0.5
    distance_metric: "cosine"
    reid_model_name: "tf_efficientnet_b1.in1k"
    reid_device: "cuda"
```


<details><summary><strong><span style="font-size: 1.25em;">📚 Ejemplo de uso</span></strong></summary>
</details>


A continuación se muestra el ejemplo de configuraciones YAML para procesar archivos de vídeo y realizar un seguimiento en tiempo real utilizando diferentes backends detector con algoritmos de seguimiento de Roboflow.


<details><summary><strong><span style="font-size: 1.4em;">SORT with Ultralytics YOLO</span></strong></summary>
</details>


```yaml
agent:
  name: sort_tracker_agent
  description: "SORT tracking with Ultralytics detector"

templates:
  - template_name: InputTemplate
    class_name: InputTemplate
    attributes: {}

  - template_name: VideoReaderCV2
    class_name: VideoReaderCV2
    template_input: InputTemplate
    attributes:
      video_file_path: "artifacts/demo_video.mp4"
      batch_size: -1

  - template_name: UltralyticsPredict
    class_name: UltralyticsPredict
    template_input: VideoReaderCV2
    attributes:
      model_class: YOLO
      model: yolo11n.pt
      task: detect
      prediction_params:
        conf: 0.7
        iou: 0.8

  - template_name: SORTTrackerInference
    class_name: SORTTrackerInference
    template_input: UltralyticsPredict
    attributes:
      track_activation_threshold: 0.25
      lost_track_buffer: 30
      minimum_consecutive_frames: 3
      minimum_iou_threshold: 0.3
      frame_rate: 30

  - template_name: BBoxDrawer
    class_name: BBoxDrawer
    template_input: SORTTrackerInference
    attributes:
      overwrite: true
      randomized_color: false
      draw_extra_labels: true

  - template_name: VideoWriterCV2
    class_name: VideoWriterCV2
    template_input: BBoxDrawer
    attributes:
      destination_path: "artifacts/tracked_result.mp4"
      height: -1
      width: -1
      fps: 30
```




<details><summary><strong><span style="font-size: 1.4em;">DeepSORT con DFINE</span></strong></summary>
</details>


```yaml
agent:
  name: deepsort_tracker_agent
  description: "DeepSORT tracking with DFINE detector"

templates:
  - template_name: InputTemplate
    class_name: InputTemplate
    attributes: {}

  - template_name: VideoReaderCV2
    class_name: VideoReaderCV2
    template_input: InputTemplate
    attributes:
      video_file_path: "artifacts/demo_video.mp4"
      batch_size: -1

  - template_name: DFINEInference
    class_name: DFINEInference
    template_input: VideoReaderCV2
    attributes:
      threshold: 0.5
      config_file: artifacts/configs/dfine/dfine_hgnetv2_n_coco.yml
      device: cuda
      pretrained_model:
        size: n
        variant: coco

  - template_name: DeepSORTTrackerInference
    class_name: DeepSORTTrackerInference
    template_input: DFINEInference
    attributes:
      track_activation_threshold: 0.25
      lost_track_buffer: 30
      minimum_consecutive_frames: 3
      minimum_iou_threshold: 0.3
      frame_rate: 30
      appearance_threshold: 0.7
      appearance_weight: 0.5
      distance_metric: "cosine"
      reid_model_name: "tf_efficientnet_b1.in1k"
      reid_device: "cuda"

  - template_name: BBoxDrawer
    class_name: BBoxDrawer
    template_input: DeepSORTTrackerInference
    attributes:
      overwrite: true
      randomized_color: false
      draw_extra_labels: true

  - template_name: VideoWriterCV2
    class_name: VideoWriterCV2
    template_input: BBoxDrawer
    attributes:
      destination_path: "artifacts/tracked_result.mp4"
      height: -1
      width: -1
      fps: 30
```



<strong>IMPORTANTE</strong>: Las plantillas de VideoReaderCV2, BBoxDrawer y VideoWriterCV2 forman parte de las <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers">sinapsis-data-readers</a>, <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_visualization">sinapsis-data-visualization</a>, y <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers">sinapsis-data-writers</a> paquetes, respectivamente. Los Ultralytics Predict template es parte de <a href="https://github.com/Sinapsis-AI/sinapsis-ultralytics">sinapsis-ultralytics</a> DFINEInference es parte de <a href="https://github.com/Sinapsis-AI/sinapsis-dfine">sinapsis-dfine</a>. Para utilizar estos ejemplos, asegúrese de haber instalado los paquetes correspondientes.

Para ejecutar la configuración, utilice el CLI:

```bash
sinapsis run your_config.yml
```


<h2 id="documentation">📙 Documentación</h2>
La documentación para este y otros paquetes de sinapsis está disponible en <a href="https://docs.sinapsis.tech/docs">web de sinapsis</a>

Los tutoriales para diferentes proyectos dentro de sinapsis están disponibles en <a href="https://docs.sinapsis.tech/tutorials">sinapsis tutoriales página</a>
<h2 id="license">🔍 Licencia</h2>
Este proyecto está licenciado bajo la licencia AGPLv3, que fomenta la colaboración abierta y el intercambio. Para más detalles, consulta el archivo <a href="LICENSE">LICENSE</a>.

Para uso comercial, consulta el  <a href="https://sinapsis.tech"> sitio web oficial de Sinapsis</a> para información sobre la obtención de una licencia comercial.

