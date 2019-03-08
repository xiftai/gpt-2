#!/usr/bin/env python3

import fire
import json
import os
import numpy as np
import tensorflow as tf
import sys

import model, sample, encoder

from py_translator import Translator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def interact_model(
    model_name='117M',
    seed=None,
    nsamples=1,
    batch_size=None,
    length=None,
    temperature=1,
    top_k=0,
):
    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0
    np.random.seed(seed)
    tf.set_random_seed(seed)

    enc = encoder.get_encoder(model_name)
    hparams = model.default_hparams()
    with open(os.path.join('models', model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    print("GPT-2 Parameters")
    print("================")
    print("Model Name : "+ str(model_name))
    print("Seed = " + str(seed))
    print("N Samples = " + str(nsamples))
    print("Batch Size = " + str(batch_size))
    print("Length = " + str(length))
    print("Temperature = " + str(temperature))
    print("Top K = " + str(top_k))

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k
        )
        
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
        saver.restore(sess, ckpt)

        context_tokens = enc.encode(raw_text)
        print("Context Tokens = " + str(context_tokens))
        generated = 0
        for _ in range(nsamples // batch_size):
            out = sess.run(output, feed_dict={
                context: [context_tokens for _ in range(batch_size)]
            })[:, len(context_tokens):]
            for i in range(batch_size):
                generated += 1
                text = enc.decode(out[i])
                print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                print(text)
        print("=" * 80)

if __name__ == '__main__':
    input_text = sys.argv.pop(1)
    raw_text = Translator().translate(text=input_text, dest='en').text
    print("Input Text (Translated)")
    print("=======================")
    print(str(raw_text))
    print("")
    fire.Fire(interact_model)

