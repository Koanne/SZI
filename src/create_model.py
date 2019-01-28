import tensorflow as tf
from svhn import SVHN

n_input = 3072   # warstwa wejściowa(32x32x3 piksele i rgb)
n_hidden1 = 512 # pierwsza warstwa ukryta
n_hidden2 = 256 # druga warstwa ukryta
n_hidden3 = 128 # trzecia warstwa ukryta
n_output = 10   # warstwa wyjściowa (cyfry od 0 do 9)

svhn = SVHN("../res", n_output, use_extra=False, gray=False)

learning_rate = 0.001
batch_size = 40
n_iterations = int(svhn.train_examples / batch_size)

normalization_offset = 0.0  # beta
normalization_scale = 1.0  # gamma
normalization_epsilon = 0.001  # epsilon

#placeholdery na wejściowe i wyjściowe dane
X = tf.placeholder("float", [None, 32, 32, 3], name="X")
Y = tf.placeholder("float", [None, n_output], name="Y")

#wagi pomiędzy warstwami
weights = {
    'w1': tf.Variable(tf.truncated_normal([n_input, n_hidden1], stddev=0.1)),
    'w2': tf.Variable(tf.truncated_normal([n_hidden1, n_hidden2], stddev=0.1)),
    'w3': tf.Variable(tf.truncated_normal([n_hidden2, n_hidden3], stddev=0.1)),
    'out': tf.Variable(tf.truncated_normal([n_hidden3, n_output], stddev=0.1)),
}

#wartości przesunięcia
biases = {
    'b1': tf.Variable(tf.constant(0.1, shape=[n_hidden1])),
    'b2': tf.Variable(tf.constant(0.1, shape=[n_hidden2])),
    'b3': tf.Variable(tf.constant(0.1, shape=[n_hidden3])),
    'out': tf.Variable(tf.constant(0.1, shape=[n_output]))
}

mean, variance = tf.nn.moments(X, [1, 2, 3], keep_dims=True)
x = tf.nn.batch_normalization(X, mean, variance, normalization_offset, normalization_scale, normalization_epsilon)

#zmiana obrazu na talbice
x = tf.reshape(x, [-1, n_input])

#definicja modelu z wykorzystanie funkcji aktywacji ReLU
layer_1 = tf.add(tf.matmul(x, weights['w1']), biases['b1'])
layer_1 = tf.nn.relu(layer_1)
layer_2 = tf.add(tf.matmul(layer_1, weights['w2']), biases['b2'])
layer_2 = tf.nn.relu(layer_2)
layer_3 = tf.add(tf.matmul(layer_2, weights['w3']), biases['b3'])
layer_3 = tf.nn.relu(layer_3)
output_layer = tf.add(tf.matmul(layer_3, weights['out']), biases['out'], name = "output")
print("Output layer", output_layer)



cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=Y, logits=output_layer))

#trening modelu algorytmem Adam
train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

#dokładność modelu pomiędzy 0 a 1
correct_pred = tf.equal(tf.argmax(output_layer, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

saver = tf.train.Saver()
# trening na próbkach wielkości 128 i na nich dokonujemy aktualizacji modelu
for i in range(n_iterations):
    batch_x, batch_y = (svhn.train_data[i * batch_size:(i + 1) * batch_size], svhn.train_labels[i * batch_size:(i + 1) * batch_size])

    #algorytm propagacji wstecznej
    sess.run([train_step, cross_entropy], feed_dict={X: batch_x, Y: batch_y})

    # wyświetlamy cząstkowe wartości dla funkcji straty i dokładność klasyfikaci na próbce danych
    if i%100==0:
        minibatch_loss, minibatch_accuracy = sess.run([cross_entropy, accuracy], feed_dict={X: batch_x, Y: batch_y})
        print("Iteracja:", str(i), "\t| Strata =", str(minibatch_loss), "\t| Dokładność =", str(minibatch_accuracy))

test_accuracy = sess.run(accuracy, feed_dict={X: svhn.test_data, Y: svhn.test_labels})
print("\nDokładność na zbiorze testowym:", test_accuracy)

saved_path = saver.save(sess, './model/my-model')
print("Model saved in path: %s" % saved_path)
