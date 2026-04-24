<h1 align="center"><br/><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis Trackers
<br/></h1>
<h4 align="center">Mono repo con paquetes modulares para seguimiento multiobjeto utilizando algoritmos avanzados. </h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#packages">📦 Paquetes</a> •
<a href="#webapps">🌐 Webapps</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#license">🔍 Licencia</a>


<h2 id="installation">🐍 Instalación</h2>


Este mono repo consiste en paquetes modulares para implementar y visualizar el seguimiento multiobjeto utilizando diversos algoritmos y modelos de seguimiento:



<ul>
<li><code>sinapsis-cotracker</code></li>

<li><code>sinapsis-supervision</code></li>

<li><code>sinapsis-rf-trackers</code></li>
</ul>
Instala el administrador de tu paquete de elección. Alentamos el uso de <code>uv</code>

<h3> sinapsis-cotracker </h3>

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
<h4> Instrucciones de pip solo</h4>
Instale cotracker en su entorno de trabajo como sigue:

```bash
pip install git+https://github.com/facebookresearch/co-tracker.git
```

entonces instalar sinapsis-cotracker

```bash
pip install sinapsis-cotracker --extra-index-url https://pypi.sinapsis.tech
```
<h3>sinapsis-supervision</h3><h4> Instrucciones UV</h4>
Instalar sinapsis-supervision

```bash
uv pip install sinapsis-supervision --extra-index-url https://pypi.sinapsis.tech
```
<h4> Instrucciones de pip solo</h4>
Instalar sinapsis-supervision

```bash
pip install sinapsis-supervision --extra-index-url https://pypi.sinapsis.tech
```
<h3>sinapsis-rf-trackers</h3><h4> Instrucciones UV</h4>
Instalar sinapsis-rf-trackers

```bash
uv pip install sinapsis-rf-trackers --extra-index-url https://pypi.sinapsis.tech
```
<h4> Instrucciones de pip solo</h4>
Instalar sinapsis-rf-trackers

```bash
pip install sinapsis-rf-trackers --extra-index-url https://pypi.sinapsis.tech
```
<h3>(Opcional) Instalar paquetes con todas las dependencias adicionales</h3>

<blockquote>

[!IMPORTANT]
Las plantillas en cada paquete pueden requerir dependencias adicionales. Para el desarrollo, recomendamos instalar el paquete con todas las dependencias opcionales:


</blockquote>

```bash
  uv pip install sinapsis-cotracker[all] --extra-index-url https://pypi.sinapsis.tech

  uv pip install sinapsis-supervision[all] --extra-index-url https://pypi.sinapsis.tech

  uv pip install sinapsis-rf-trackers[all] --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-cotracker[all] --extra-index-url https://pypi.sinapsis.tech

  pip install sinapsis-supervision[all] --extra-index-url https://pypi.sinapsis.tech

  pip install sinapsis-rf-trackers[all] --extra-index-url https://pypi.sinapsis.tech
```


<blockquote>

[!TIP]
También puede instalar todos los paquetes dentro de este proyecto:


</blockquote>

```bash
  uv pip install sinapsis-trackers[all] --extra-index-url https://pypi.sinapsis.tech
```
<h2 id="packages">📦 Paquetes</h2>
Este repositorio se organiza en paquetes modulares, cada uno diseñado para la integración específica con diferentes modelos de seguimiento, incluyendo CoTracker y ByteTrack. Estos paquetes proporcionan plantillas listas para usar para aplicaciones como seguimiento de objetos, seguimiento de múltiples objetos y visualización de resultados en tiempo real o offline.


A continuación se presenta una visión general de los paquetes disponibles:

<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">Sinapsis Cotrackers</span></strong></summary>



Este paquete de sinapsis proporciona una aplicación robusta para el seguimiento multiobjeto con el modelo Co-Tracker de Facebook Research. Incluye:

<ul>
<li>Plantillas para el seguimiento multiobjeto utilizando <strong>Co-Tracker</strong>, ofreciendo flexible <strong>offline</strong>, <strong>online</strong>, y <strong>visualización</strong> Modos.</li>

<li>Procesamiento y visualización eficientes de resultados de seguimiento directamente en marcos de vídeo para una salida clara.</li>

<li>Herramientas para manejar el seguimiento dinámico a través de marcos, incluyendo relleno, ancho de línea y configuración de trazas.</li>
</ul>
Para instrucciones específicas y más detalles, ve el <a href="https://github.com/Sinapsis-AI/sinapsis-trackers/blob/main/packages/sinapsis_cotracker/README.md">README.md</a>.

</details>
<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">Sinapsis Supervision</span></strong></summary>



Este paquete Sinapsis proporciona una solución integral para el seguimiento de objetos con el algoritmo ByteTrack. Incluye:

<ul>
<li>Una plantilla para el seguimiento de objetos usando <strong>ByteTrack</strong>, diseñado para manejar el seguimiento multiobjeto en tiempo real en videos.</li>

<li>Procesamiento de detección y actualizaciones con parámetros configurables para la activación de pistas, emparejamiento y manejo de oclusión, mejorando la precisión y estabilidad.</li>
</ul>
Para más detalles, ve el <a href="https://github.com/Sinapsis-AI/sinapsis-trackers/blob/main/packages/sinapsis_supervision/README.md">README.md</a>.


</details>
<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">Sinapsis RF Trackers</span></strong></summary>



Este paquete Sinapsis proporciona plantillas robustas para el seguimiento multiobjeto, aprovechando la biblioteca de rastreadores. Integra potentes algoritmos como SORT y DeepSORT en el ecosistema de Sinapsis.

<ul>
<li>SORT Tracker: Un rastreador sencillo y eficiente basado en movimiento ideal para aplicaciones de alta velocidad.</li>

<li>DeepSORT Tracker: Un rastreador avanzado que mejora el SORT incorporando características de apariencia utilizando un modelo configurable de Re-Identificación (Re-ID). Esto hace que sea más robusto contra las oclusiones y ayuda a mantener identidades de objetos en escenas complejas.</li>

<li>Configuración flexible: Ofrece atributos extensos al comportamiento del rastreador fino, incluyendo soporte para varios modelos Re-ID a través de la biblioteca de timm.</li>
</ul>
Para instrucciones específicas y más detalles, ve el <a href="https://github.com/Sinapsis-AI/sinapsis-trackers/blob/main/packages/sinapsis_rf_trackers/README.md">README.md</a>.



Para más detalles, ve el <a href="https://docs.sinapsis.tech/docs">documentación oficial</a>

</details>

<h2 id="webapps">🌐 Aplicaciones web</h2>
Las aplicaciones web incluidas en este proyecto muestran la modularidad de las plantillas, en este caso para tareas de seguimiento y visualización multiobjetos.



<blockquote>

[!IMPORTANT]
Para ejecutar la aplicación, primero necesitas clonar este repo:


</blockquote>

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-trackers.git
cd sinapsis-trackers
```


<blockquote>

[! NOTA]
Si deseas habilitar el intercambio de aplicaciones externas en Gradio, <code>export GRADIO_SHARE_APP=True</code>


[! NOTA]
La configuración del agente se puede actualizar a través de <code>AGENT_CONFIG_PATH</code> Environment var. Puede comprobar las configuraciones disponibles en cada carpeta de configuración de paquetes.


</blockquote>



<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>



<strong>IMPORTANTE</strong>: Esta imagen Docker depende de <code>sinapsis-nvidia:base</code>. Para instrucciones detalladas, consulta el <a href="https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker">README</a>.

<ol>
<li><strong>Construir la imagen de los sinapsis-trackers</strong>:</li>
</ol>

```bash
docker compose -f docker/compose.yaml build
```
<ol start="2">
<li><strong>Iniciar el contenedor</strong>:</li>
</ol>
Para sinapsis-cotracker

```bash
docker compose -f docker/compose_tracker.yaml up sinapsis-cotracker-gradio -d
```

Para sinapsis-supervision con demo predeterminado bytetrack-ultralytics

```bash
docker compose -f docker/compose_tracker.yaml up sinapsis-supervision-gradio -d
```

Para sinapsis-supervision con demo bytetrack-dfine

```bash
export DFINE_CONFIG_DOWNLOAD=True
export AGENT_CONFIG_PATH=/app/sinapsis_supervision/configs/bytetrack_dfine_demo.yml
docker compose -f docker/compose_tracker.yaml up sinapsis-supervision-gradio -d
```
<ol start="3">
<li><strong>Comprueba el estado</strong>:</li>
</ol>
Para sinapsis-cotracker

```bash
docker logs -f sinapsis-cotracker-gradio
```

Para sinapsis-supervision

```bash
docker logs -f sinapsis-supervision-gradio
```
<ol start="4">
<li><strong>Los registros mostrarán la URL para acceder a la aplicación web, por ejemplo,</strong>:</li>
</ol>

```bash
Running on local URL:  http://127.0.0.1:7860
```

<strong>NOTA</strong>: La URL local puede ser diferente, por favor revise los registros

<ol start="5">
<li><strong>Para detener la aplicación</strong>:</li>
</ol>

```bash
docker compose -f docker/compose_tracker.yaml down
```

</details>
<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">📦 UV</span></strong></summary>Para ejecutar la aplicación web utilizando <code>uv</code> administrador de paquetes, por favor:


<ol>
<li><strong>Crear el entorno virtual y sincronizar las dependencias</strong>:</li>
</ol>

```bash
uv sync --frozen --extra cotracker
```
<ol start="2">
<li><strong>Instalar el paquete sinapsis-trackers</strong>:</li>
</ol>

```bash
uv pip install sinapsis-trackers[all] --extra-index-url https://pypi.sinapsis.tech
```
<ol start="3">
<li><strong>Ejecute la aplicación web</strong>:</li>
</ol>
Para ejecución por defecto<a href="https://github.com/Sinapsis-AI/sinapsis-trackers/blob/main/packages/sinapsis_cotracker/src/sinapsis_cotracker/configs/cotracker_online.yml">cotracker-online</a>.

```bash
uv run webapps/tracking_demo.py
```

Para la demostración corre la configuración de agente <a href="https://github.com/Sinapsis-AI/sinapsis-trackers/blob/main/packages/sinapsis_supervision/src/sinapsis_supervision/configs/bytetrack_ultralytics_demo.yml">bytrack-ultralytics</a>.

```bash
export AGENT_CONFIG_PATH="packages/sinapsis_supervision/src/sinapsis_supervision/configs/bytetrack_ultralytics_demo.yml"
uv run webapps/tracking_demo.py
```

Para la demostración corre la configuración de agente <a href="https://github.com/Sinapsis-AI/sinapsis-trackers/blob/main/packages/sinapsis_supervision/src/sinapsis_supervision/configs/bytetrack_dfine_demo.yml">bytetrack-dfine</a>.

```bash
export DFINE_CONFIG_DOWNLOAD=True
export AGENT_CONFIG_PATH="packages/sinapsis_supervision/src/sinapsis_supervision/configs/bytetrack_dfine_demo.yml"
uv run webapps/tracking_demo.py
```
<ol start="4">
<li><strong>El terminal mostrará la URL para acceder a la aplicación web, por ejemplo.</strong>:</li>
</ol>

```bash
Running on local URL:  http://127.0.0.1:7860
```

<strong>NOTA</strong>: La URL local puede ser diferente, por favor revise la salida de la terminal.


</details>

<h2 id="documentation">📙 Documentación</h2>
La documentación está disponible en el <a href="https://docs.sinapsis.tech/docs">sitio web de sinapsis</a>


Los tutoriales para diferentes proyectos dentro de sinapsis están disponibles en <a href="https://docs.sinapsis.tech/tutorials">la página de sinapsis tutoriales</a>

<h2 id="license">🔍 Licencia</h2>
Este proyecto está licenciado bajo la licencia AGPLv3, que fomenta la colaboración abierta y el intercambio. Para más detalles, consulta el archivo<a href="LICENSE">LICENSE</a>.


Para uso comercial, consulta nuestra página <a href="https://sinapsis.tech">oficial de Sinapsis</a> para información sobre la obtención de una licencia comercial.



