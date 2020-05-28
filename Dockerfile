FROM tensorflow/tensorflow:2.0.0-gpu-py3

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      screen \
      libopenexr-dev \
      wget && \
    rm -rf /var/lib/apt/lists/* \
    apt-get upgrade

ENV TENSOR_HOME /home/isr
WORKDIR $TENSOR_HOME

RUN pip install --upgrade pip
RUN pip install opencv-python tqdm OpenEXR pyexr ISR
RUN pip install --ignore-installed tensorflow-gpu==2.0.0
RUN mkdir -p /root/.keras/datasets/
RUN wget https://public-asai-dl-models.s3.eu-central-1.amazonaws.com/ISR/rrdn-C4-D3-G32-G032-T10-x4-GANS/rrdn-C4-D3-G32-G032-T10-x4_epoch299.hdf5 -O /root/.keras/datasets/rrdn-C4-D3-G32-G032-T10-x4_epoch299.hdf5