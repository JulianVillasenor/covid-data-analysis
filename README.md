# Covid-19 Dashboard

Este proyecto es un dashboard interactivo que muestra información sobre la pandemia de Covid-19 en Durango, México. La información se obtiene de la base de datos de la Secretaría de Salud y abarca desde enero de 2020 hasta diciembre 2022.

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/JulianVillasenor/covid-data-analysis.git
    cd covid-data-analysis
    ```

2. Crea un entorno virtual y actívalo:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. Instala las dependencias del proyecto:
    ```bash
    pip3 install -r requirements.txt
    ```
    
4. Inicializa el servidor de desarrollo:
    ```bash
    streamlit run app.py
    ```