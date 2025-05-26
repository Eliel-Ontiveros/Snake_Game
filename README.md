# Juego de la Serpiente (Snake Game)

Este es un clásico juego de la Serpiente implementado en Python utilizando la biblioteca Pygame. El juego cuenta con varias características, incluyendo diferentes apariencias para la serpiente, niveles de dificultad y un sistema de clasificación.

## Características

* **Juego Clásico de la Serpiente:** Controla la serpiente para comer comida y crecer, ¡evita chocar contra las paredes o tu propio cuerpo!
* **Múltiples Pantallas:**
    * **Título:** Menú principal para iniciar el juego, ver clasificaciones, opciones o salir.
    * **Juego:** La pantalla principal donde se desarrolla la acción.
    * **Fin del Juego:** Muestra tu puntuación final al perder.
    * **Clasificación:** Muestra las 10 puntuaciones más altas.
    * **Opciones:** Permite personalizar la apariencia y la dificultad.
* **Apariencias Personalizables:** Elige entre varias apariencias para la serpiente y el fondo, cada una con su propia música y efectos de sonido.
    * Clásico
    * Kirby
    * La Criatura
    * Yoshi
* **Niveles de Dificultad:** Ajusta la velocidad de la serpiente para un desafío mayor.
* **Sistema de Clasificación:** Guarda y muestra las 10 puntuaciones más altas.
* **Música y Sonidos:** Música de fondo y efectos de sonido para comer y perder.

## Requisitos

* Python 3.x
* Pygame

## Instalación

1.  **Clona el repositorio (o descarga los archivos):**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO>
    ```
2.  **Instala Pygame:**
    ```bash
    pip install pygame
    ```

## Cómo Jugar

1.  **Ejecuta el juego:**
    ```bash
    python Snake.py
    ```
2.  **Menú Principal:**
    * Usa las teclas **ARRIBA** y **ABAJO** para navegar por las opciones.
    * Presiona **ESPACIO** para seleccionar.
3.  **En el Juego:**
    * Usa las teclas de **flecha (ARRIBA, ABAJO, IZQUIERDA, DERECHA)** para dirigir la serpiente.
    * Come la comida (pastel) para crecer y aumentar tu puntuación.
    * Evita chocar contra los bordes de la pantalla o el cuerpo de la serpiente.
4.  **Opciones:**
    * Navega con **ARRIBA** y **ABAJO**.
    * Presiona **ESPACIO** para cambiar la apariencia o la dificultad, o para regresar al menú principal.

## Archivos y Directorios

* `Snake.py`: El script principal del juego.
* `Snake_02.py`: Una versión alternativa o en desarrollo del juego que incluye obstáculos.
* `Docs/`: Contiene archivos de documentación.
    * `rankings.txt`: Almacena las puntuaciones más altas.
* `IMG/`: Contiene todas las imágenes y gráficos utilizados en el juego.
* `FX/`: Contiene los archivos de música y efectos de sonido.
* `Font/`: Contiene la fuente utilizada para el texto (se requiere `Minecraft.ttf`).

## Notas

* Asegúrate de tener todas las carpetas (`IMG`, `FX`, `Font`, `Docs`) y sus respectivos archivos en la misma ubicación que `Snake.py` para que el juego funcione correctamente.
* `Snake_02.py` introduce obstáculos, pero la lógica de colisión podría ser experimental.
