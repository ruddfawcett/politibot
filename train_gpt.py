#!/usr/bin/env python

import os

import gpt_2_simple as gpt2

STEPS = 500
MODEL_NAME = '355M'
FILE_PATH = 'tweets'

if not os.path.isdir(os.path.join('models', MODEL_NAME)):
    print(f'Downloading {MODEL_NAME} model...')
    gpt2.download_gpt2(model_name = MODEL_NAME)

gpt2.encode_dataset(f'{FILE_PATH}.csv')

sess = gpt2.start_tf_sess()

gpt2.finetune(sess,
              'text_encoded.npz',
              model_name=MODEL_NAME,
              steps=STEPS,
              restore_from='fresh',
              run_name='run1',
              print_every=10,
              sample_every=100)
