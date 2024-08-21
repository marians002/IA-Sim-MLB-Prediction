# Predicción de los resultados de la MLB

## Integrantes

- Alejandro Álvarez Lamazares - C311
- Marian S. Álvarez Suri - C312
- Carlos A. Bresó Sotto - C312

### Objetivo del Proyecto

Predecir con la mayor exactitud posible los resultados de la MLB en un rango de tiempo determinado (puede ser una temporada completa o una sección de esta) a partir de los datos estadísticos de temporadas previas.

### Componentes de IA presentes en el proyecto

#### Búsqueda

Vamos a determinar cuál sería el line-up óptimo (entiéndase por line-up el conjunto de los 9 jugadores titulares y el pitcher abridor) con el que podría arrancar un equipo, dada la plantilla de jugadores disponibles para la fecha pactada.

La complejidad de esta selección se basa en las condiciones que debe cumplir un line-up para explotar al máximo la capacidad de cada jugador. Por ejemplo, por convención el primer puesto del line-up lo ocupa el jugador que más se embasa; sin embargo, si tenemos dos jugadores que se embasan con la misma frecuencia, podríamos tener en cuenta la velocidad individual para decidir cuál de los dos debería ser el primer bate.

Además, si sabemos que por las estadísticas de un bateador, este se considera el mejor jugador del equipo (digamos que lo colocamos como 4to madero), lo mejor sería tenerlo en cuenta en cualquier line-up que pueda considerarse óptimo.

#### Conocimiento

Dado un momento determinado del juego, el manager toma decisiones de conjunto con el cuerpo de pitcheo y bateo para seleccionar cuál es el mejor paso a seguir. Para ello debe tener en cuenta aspectos como las condiciones actuales del partido y el desempeño individual de cada jugador en diversas situaciones.

Situaciones donde podemos evidenciar esto es a la hora de sustituir un pitcher, seleccionar bateadores emergentes o cambiar jugadores de la alineación titular durante el transcurso del juego por lesiones. También podrían ocurrir cambios predeterminados durante el juego con el objetivo de dar descanso a jugadores veteranos y oportunidades a los nuevos integrantes del equipo.

#### Procesamiento de Lenguaje Natural

Podemos implementar alguna(s) de las siguientes funcionalidades donde se aplicarán elementos relacionados con el Procesamiento de Lenguaje Natural:

- Chatbot donde los usuarios puedan preguntar datos estadísticos específicos.
- Comentario sobre los resultados anteriores a un juego (previa de un partido) y los posibles desenlaces.
- Resumen de un juego una vez concluido este a modo de noticia.
- Narrador en tiempo real: A medida que van ocurriendo los eventos importantes del juego, se narra lo sucedido.
