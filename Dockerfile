FROM continuumio/miniconda3

COPY . /CIMP5_Historical
WORKDIR /CIMP5_Historical

RUN conda env create -f environment.yml

RUN echo "conda activate myenv" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

RUN conda install -c conda-forge --file requirements.txt -y
