#!/bin/bash

CUDA_VISIBLE_DEVICES=0,1 accelerate launch --num_processes 2 benchmark/eval_humaneval.py \
 --eval_mode para_sd \
 --gamma 5 \
 -n 1 \
 -e H_PSD_llama3_3_1b \
 --draft_model meta-llama/Llama-3.2-1B \
 --target_model meta-llama/Llama-3.2-3B \
 --max_tokens 1024 \
 --temp 0