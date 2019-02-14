FROM tensorflow/tensorflow:1.12.0-gpu-py3

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    NVIDIA_REQUIRE_CUDA="cuda>=8.0" \
    LANG=C.UTF-8

RUN apt-get update && mkdir /gpt-2
ADD requirements.txt /gpt-2/requirements.txt
RUN pip3 install -r /gpt-2/requirements.txt

WORKDIR /gpt-2
ADD . /gpt-2

CMD ["sleep", "infinity"]
