import tensorflow as tf
import numpy as np
import Quantizers
import QSGD

from tensorflow.python.ops import standard_ops

input_width = input_height =3
batch_size = 1
input_channels = 1
train_iterations = 10
fixed_size=2
fixed_prec=1

inputs_vals = np.arange(input_width*input_height*input_channels*batch_size).reshape(batch_size,input_width,input_height,input_channels)
print (inputs_vals)
#inputs_vals = np.ones((batch_size,input_width,input_height,input_channels))

inputs = tf.Variable(inputs_vals,dtype=tf.float64)
gold_inputs = tf.Variable(inputs_vals,dtype=tf.float64)

#quantizer=Quantizers.NoQuantizer()
quantizer=Quantizers.FixedPointQuantizer_nearest(fixed_size,fixed_prec)

optimizer = QSGD.GradientDescentOptimizer(0.1,quantizer=Quantizers.NoQuantizer())
output = quantizer.quantize(inputs * 2)
loss = tf.nn.l2_loss(output-inputs)
grads_vars = optimizer.compute_gradients(loss)
train = optimizer.apply_gradients(grads_vars)

gold_optimizer = tf.train.GradientDescentOptimizer(0.1)
gold_output = quantizer.quantize(gold_inputs * 2)
gold_loss = tf.nn.l2_loss(gold_output-gold_inputs)
gold_grads_vars = gold_optimizer.compute_gradients(gold_loss)
gold_train = gold_optimizer.apply_gradients(gold_grads_vars)


with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  for i in range(train_iterations):
    sess.run(train)
    sess.run(gold_train)
  gold_result=gold_output.eval().flatten()
  result=output.eval().flatten()
  print(sess.run(output))
  print(sess.run(gold_output))

failed=False
for i in range(len(result)):
    if result[i] != gold_result[i]:
        failed = True
        break

print('QSGD test:')
if failed:
    print('---failed!---')
else:
    print('+++passed!+++')

