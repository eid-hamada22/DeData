from sklearn.datasets import load_iris, fetch_openml
from tensorflow.keras.datasets import fashion_mnist

def get_df(name):
    if name == 'iris l classifction':
        return load_iris(as_frame=True).frame, 'target'
    if name == 'Fashion MNIST l classifction':
        (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()  # split into tetsing and training
        return fetch_openml('mnist_784', version=1,as_frame=True,parser='auto').frame, 'target'
