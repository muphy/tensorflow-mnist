import tensorflow as tf
import numpy as np
import os
import csv
import collections

class PackageGroup:
    X_RATE = 10
    Y_RATE = 1000
    def __init__(self):
        # self.package_dict = {}
        self.package_dict = collections.OrderedDict()

    def append_package(self,package):
        key = package.make_key()
        if key not in self.package_dict:
            self.package_dict[key] = []
            # print(key)
        self.package_dict[key].append(package)

    def print_items(self):
        for k,v in self.package_dict.items():
            print(k,v)
            # packages = v

    def get_xy_data(self,package):
        x_data = []
        y_data = []
        key = package.make_key()
        try:
            packages = self.package_dict[key]
        except KeyError:
            return None,None
        # print(packages)
        for package in packages:
            x_data.append(float(package.age)/self.X_RATE)
            y_data.append(float(package.price)/self.Y_RATE)

        x_data = np.array(x_data,dtype=np.float32)
        y_data = np.array(y_data,dtype=np.float32)
        return x_data,y_data

class Package:
    def __init__(self,row = None):
        if row is not None:
            self.age = row['age']
            self.gender = row['gender']
            self.job = row['job']
            self.cover_code = row['cover_code']
            self.price = row['price']

    # key value = gender+job+cover_code
    def make_key(self):
        return self.gender+self.job+self.cover_code

    @classmethod
    def from_csv_string(cls,gender,job,cover_code):
        cls.gender = gender
        cls.job = job
        cls.cover_code = cover_code
        return cls()


packageGroups = PackageGroup()

csv_dir = os.path.dirname(os.path.abspath(__file__))
with open(csv_dir+'/data/query_result.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(dir(row))
        package = Package(row)
        packageGroups.append_package(package)

# packageGroups.print_items()
def calc_package_price(age,gender,job,cover_code):
    package = Package.from_csv_string(gender,job,cover_code)
    x_data,y_data = packageGroups.get_xy_data(package)
    if x_data is None:
        return 0
    x = tf.placeholder(tf.float32)
    W = tf.Variable([1.], tf.float32)
    b = tf.Variable([-1.], tf.float32)
    sess = tf.Session()
    linear_model = W * x + b
    init = tf.global_variables_initializer()
    sess.run(init)
    y = tf.placeholder(tf.float32)
    squared_deltas = tf.square(linear_model - y)
    loss = tf.reduce_sum(squared_deltas)
    optimizer = tf.train.GradientDescentOptimizer(0.001)
    train = optimizer.minimize(loss)
    sess.run(init)
    for i in range(1000):
        sess.run(train, {x: x_data, y: y_data})
    prices = sess.run(linear_model, feed_dict={x: age})
    price = int((prices[0]*PackageGroup.Y_RATE).item())
    return price

res = calc_package_price(6.5,'2','1','00000000000000001p0000')
# print(type(res))
# print(res)