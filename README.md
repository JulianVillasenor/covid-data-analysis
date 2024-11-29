# Covid-19 Dashboard

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

## Uso

Dentro del proyecto, es necesario crear un folder con el nombre de data, donde deven estar almacenados:
COVID19_2020_CONFIRMADOS.csv, COVID19_2021_CONFIRMADOS.csv y COVID19_2022_CONFIRMADOS.csv
Una vez que el servidor esté en funcionamiento, dirígete a `http://localhost:8501/`

## Instalación de Python y pip

## Sigue estos pasos para instalar **Python** y **pip** en tu sistema operativo:

### En Windows

1. **Descargar el instalador:**
   - Ve a [python.org/downloads](https://www.python.org/downloads/) y descarga el instalador de Python para Windows.

2. **Ejecutar el instalador:**
   - Haz doble clic en el archivo descargado.
   - **Importante:** Asegúrate de marcar la casilla **"Add Python to PATH"** antes de continuar.

3. **Completar la instalación:**
   - Selecciona **"Install Now"** o personaliza la instalación según tus necesidades.

4. **Verificar la instalación:**
   - Abre una terminal (CMD) y ejecuta:
     ```bash
     python --version
     ```
   - También verifica `pip` con:
     ```bash
     pip --version
     ```

---

### En macOS

1. **Usar Homebrew para instalar Python (recomendado):**
   - Si no tienes Homebrew, instálalo ejecutando este comando en la terminal:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Luego, instala Python con:
     ```bash
     brew install python
     ```

2. **Verificar las versiones instaladas:**
   - Abre la terminal y ejecuta:
     ```bash
     python3 --version
     pip3 --version
     ```

---

### En Linux (Ubuntu/Debian)

1. **Actualizar el sistema:**
   ```bash
   sudo apt update && sudo apt upgrade

## Python y pip

### instalar python
    sudo apt install python3

### instalar pip
    sudo apt install python3-pip


### verificar las versiones instaladas
    python3 --version
    pip3 --version
