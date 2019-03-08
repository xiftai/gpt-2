#!/bin/sh

TAG=xift.ai:gpt-2

if [ $# -eq 0 ];
then
  echo "$0 "INPUT TEXT" [PARAMETERS]"
  echo ""
  echo "Parameters :"
  echo "--seed (None) : a random value is generated unless specified. give a specific integer value if you want to reproduce same results in the future."
  echo "--nsamples (1) : specify the number of samples you want to print"
  echo "--length (None) : number of tokens (words) to print on each sample."
  echo "--batch_size (1) : how many inputs you want to process simultaneously. doesn't seem to affect the results."
  echo "--temperature (1) : scales logits before sampling prior to softmax."
  echo "--top_k (0) : truncates the set of logits considered to those with the highest values."
  echo ""
  echo "Example : $0 \"In a shocking finding, scientist discovered a herd of unicorns living in a remote, previously unexplored valley, in the Andes Mountains.\" --nsamples=2 --top_k 40 --temperature .80"
else
  # Ejecutamos el docker
  docker run -ti ${TAG} python3 src/generate_conditional_samples.py "$@"
fi
