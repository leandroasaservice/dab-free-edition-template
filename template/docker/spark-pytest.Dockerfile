# Spark + pytest Docker image for testing PySpark applications
# Based on https://github.com/leandroasaservice/spark-compose

ARG PYTHON_VERSION=3.13.0
ARG ALPINE_VERSION=3.20

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

# Spark and Delta Lake versions
ARG SPARK_VERSION=3.5.7
ARG DELTA_SPARK_VERSION=3.3.2

# Install system dependencies (Java is required for Spark)
# Build tools needed to compile numpy from source (no pre-built wheel for numpy<2.0 on Python 3.13)
RUN apk add --no-cache \
    bash \
    openjdk17-jre-headless \
    gcc \
    g++ \
    musl-dev \
    && rm -rf /var/cache/apk/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk

# Install Python packages for Spark and testing
# setuptools provides distutils (removed in Python 3.12) needed by pyspark.testing
# pandas and pyarrow are required by pyspark.testing utilities
# numpy<2.0 and pandas<3.0 are required for PySpark 3.5 compatibility
RUN pip install --no-cache-dir \
    setuptools \
    "numpy<2.0" \
    "pandas<3.0" \
    pyarrow \
    pyspark==${SPARK_VERSION} \
    delta-spark==${DELTA_SPARK_VERSION} \
    pytest \
    pytest-cov \
    pytest-bdd

WORKDIR /app
ENV PYTHONPATH=/app

CMD ["pytest", "-v"]
