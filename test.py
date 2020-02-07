import gpt_2_simple as gpt2
import re
import tensorflow as tf

MIN_LENGTH = 20
MAX_LENGTH = 40
STEP_LENGTH = 10

sess = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(sess)
generate_count = 0

subject = 'I hate Trintino because'

prepend = f'<|startoftext|>{subject}'
text = prepend
length = MIN_LENGTH

# Heavily influenced by https://github.com/minimaxir/reddit-gpt-2-cloud-run/blob/master/app.py.
while '<|endoftext|>' not in text and length <= MAX_LENGTH:
    text = gpt2.generate(sess,
                         length=STEP_LENGTH,
                         temperature=0.7,
                         top_k=40,
                         prefix=text,
                         include_prefix=True,
                         return_as_list=True
                         )[0]
    print(text)
    print(generate_count)
    length += STEP_LENGTH

    generate_count += 1
    if generate_count == 8:
        # Reload model to prevent Graph/Session from going OOM
        tf.compat.v1.reset_default_graph()
        sess.close()
        sess = gpt2.start_tf_sess(threads=1)
        gpt2.load_gpt2(sess)
        generate_count = 0

prepend_esc = re.escape('<|startoftext')
eot_esc = re.escape('<|endoftext|>')
patter = f'(?:{prepend_esc})(.*)(?:{eot_esc})'

trunc_text = re.search(pattern, text)

print(trunc_text.group(1))
