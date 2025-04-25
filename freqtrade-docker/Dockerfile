FROM freqtradeorg/freqtrade:stable

# Switch user to root if you must install something from apt
# Don't forget to switch the user back below!
USER root
RUN apt-get update && apt-get install -y build-essential libarchive-dev gcc libssl-dev git libffi-dev libzmq3-dev libczmq-dev openssl libhdf5-dev libgfortran5 pkg-config cmake gcc-arm-none-eabi libnewlib-arm-none-eabi

USER ftuser
# The below dependency - pyti - serves as an example. Please use whatever you need!
RUN pip install --user pip keras PyWavelets finta tensorflow pytorch-lightning tqdm PrettyTable statsmodels h5py xgboost torch darts==0.20.0 quantstats simdkalman pykalman scipy scikit-learn statsforecast==0.6.0 multiprocess numba arrow
RUN pip install --upgrade typing-extensions

# Instalar PyTorch e pacotes relacionados
RUN pip install --user torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# Switch back to user (only if you required root above)