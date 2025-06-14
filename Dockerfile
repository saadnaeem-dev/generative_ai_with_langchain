# Using a miniconda base image:
FROM continuumio/miniconda3:23.9.0-0

ENV PIP_DEFAULT_TIMEOUT=1000

RUN apt-get update && apt-get install -y pandoc wget build-essential && rm -rf /var/lib/apt/lists/*

# Update the environment:
COPY requirements.txt .

# I was sometimes running into errors with hashes:
RUN python -m pip install --upgrade pip && pip cache purge

# This is to avoid getting the GPU torch version. Please remove the index option, if you have a GPU:
RUN pip install torch>=1.11.0 --extra-index-url https://download.pytorch.org/whl/cpu

# Avoid any hash conflicts and extra time compiling:
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

WORKDIR /home
COPY . ./.

EXPOSE 8888
# To support streamlit or other applications, we could add more expose in the Dockerfile, like this:
# EXPOSE 8501

ENTRYPOINT ["jupyter", "notebook", "--notebook-dir=.", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
