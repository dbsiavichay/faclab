FROM python:3.12-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    APP_ROOT=/app \
    CONFIG_ROOT=/config \
    LANG=es_EC.UTF-8 \
    LC_ALL=es_EC.UTF-8

# Actualización de paquetes, instalación de locales y dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    locales \
    build-essential \
    software-properties-common \
    apt-utils \
    python3-dev \
    git && \
    sed -i -e 's/# es_EC.UTF-8 UTF-8/es_EC.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=es_EC.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Actualización de pip y setuptools
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade setuptools

# Creación de directorios
RUN mkdir -p ${CONFIG_ROOT} ${APP_ROOT}

# Copia e instalación de dependencias del sistema
COPY ./requirements_sys.txt ${CONFIG_ROOT}/
RUN apt-get update && \
    xargs -a ${CONFIG_ROOT}/requirements_sys.txt apt-get install -y --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia de archivos de requisitos
COPY ./requirements.txt ${CONFIG_ROOT}/
COPY ./requirements_dev.txt ${CONFIG_ROOT}/
RUN pip install --no-cache-dir -r ${CONFIG_ROOT}/requirements_dev.txt

# Copia del código de la aplicación
COPY . ${APP_ROOT}/

# Establecimiento del directorio de trabajo
WORKDIR ${APP_ROOT}

# Creación de usuario no root y cambio de propietario de la carpeta de la aplicación
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    chown -R appuser:appuser ${APP_ROOT}

# Cambio al usuario no root
USER appuser

# Comando de inicio
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
