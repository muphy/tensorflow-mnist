import tensorflow as tf


x = tf.placeholder(tf.float32)
W = tf.Variable([1.],tf.float32)
b = tf.Variable([-1.],tf.float32)

sess = tf.Session()
linear_model = W*x+b
init = tf.global_variables_initializer()
sess.run(init)
print(sess.run(W))
print(sess.run(b))

x_data = [ 2.5,  4.5 ]
y_data = [ 8.924, 16.106 ]
# x_data = [1,2,3,4]
# y_data = [0,-1,-2,-3]

print(sess.run(linear_model,{x:x_data}))

y = tf.placeholder(tf.float32)
squared_deltas = tf.square(linear_model-y)
loss = tf.reduce_sum(squared_deltas)
print(sess.run(loss,{x:x_data,y:y_data}))


optimizer = tf.train.GradientDescentOptimizer(0.001)
train = optimizer.minimize(loss)
# print(train)
sess.run(init)
for i in range(1000):
    sess.run(train,{x:x_data,y:y_data})

print(sess.run([W,b]))
