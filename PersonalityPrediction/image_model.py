import glob
import numpy as np
import tensorflow as tf
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from keras.applications.vgg16 import VGG16
from keras.layers import Input, Dense, Flatten,Dropout, LeakyReLU, Rescaling, BatchNormalization
from keras.preprocessing import image


IMAGE_SIZE = [224,224]

vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)
for layer in vgg.layers:
	layer.trainable = False


classifier = keras.Sequential(
	[
		vgg,
		Flatten(),
		Dense(4096, activation='relu', name='dense'),
#         Dense(4096, activation=keras.layers.ELU(), name='dense'),
#         BatchNormalization(axis = 1),
		Dropout(0.5),
		Dense(5, activation='sigmoid', name="output"),
	],
	name="classifier",
)


adversary = keras.Sequential(
	[
		keras.Input(shape=(5,)),
		Dense(200, activation='relu', name="dense"),
#         BatchNormalization(axis = 1),
#         Dense(200, activation=keras.layers.ELU(), name="dense"),
		Dense(2, activation='sigmoid', name="output"),
	],
	name="adversary",
)

class AdversarialDebiasing(keras.Model):
	def __init__(self, classifier, adversary, alpha, c_loss, a_loss, debias=True):
		super(AdversarialDebiasing, self).__init__()
		self.classifier = classifier
		self.adversary = adversary
		self.c_loss = c_loss #metric for classifier
		self.a_loss = a_loss #metric for adversaary
		self.protect_loss_weight = alpha
		self.debias = debias
		
	@property
	def metrics(self):
		return [self.c_loss, self.a_loss]


	def compile(self, optimizer,c_loss_fn, a_loss_fn):
		super(AdversarialDebiasing, self).compile()
		self.c_optimizer = optimizer[0]
		self.a_optimizer = optimizer[1]
		self.c_loss_fn = c_loss_fn
		self.a_loss_fn = a_loss_fn

		
	def call(self, data):
		x = data
		y = self.classifier(x)
		z = self.adversary(y)
		return [y,z]
		
		
	def train_step(self, data):
		
		x, y = data
		
		e_g = y[1]
		y = y[0]

		with tf.GradientTape() as tape:
			c_predictions = self.classifier(x)
			c_loss = self.c_loss_fn(y, c_predictions)

			
		c_grads = tape.gradient(c_loss, self.classifier.trainable_weights)

		
		with tf.GradientTape() as tape:
			c_predictions = self.classifier(x)
			a_predictions = self.adversary(c_predictions)
			a_loss = self.a_loss_fn(e_g, a_predictions)
			
		
		a_grads = tape.gradient(a_loss, self.classifier.trainable_weights) #projection
		
		
		with tf.GradientTape() as tape:
			c_predictions = self.classifier(x)
			a_predictions = self.adversary(c_predictions)
			a_loss = self.a_loss_fn(e_g, a_predictions)
			
		a_grads_own = tape.gradient(a_loss, self.adversary.trainable_weights)

		if self.debias:
			protect_grad = {v.name: g for (g, v) in zip(a_grads, self.classifier.trainable_weights)}
			pred_grad = [] #classifier update function
		
			for (g, v) in zip(c_grads, self.classifier.trainable_weights):
				unit_protect = protect_grad[v.name] / (tf.norm(protect_grad[v.name]) + np.finfo(np.float32).tiny)
				g -= tf.reduce_sum(g * unit_protect) * unit_protect # g- projection
				g -= self.protect_loss_weight * protect_grad[v.name] # g - projection - alpha*adv grad
				pred_grad.append((g, v))
				 
			self.c_optimizer.apply_gradients(pred_grad)
		
		else:
			self.c_optimizer.apply_gradients(zip(c_grads, self.classifier.trainable_weights))
			
		
		self.a_optimizer.apply_gradients(zip(a_grads_own, self.adversary.trainable_weights))
		
		self.c_loss.update_state(y,c_predictions)
		self.a_loss.update_state(e_g, a_predictions)
		
		return {m.name: m.result() for m in self.metrics}
	
	
	
	def test_step(self, data):
		
		x, y = data
		
		e_g = y[1]
		y = y[0]

		c_predictions = self.classifier(x)
		c_loss = self.c_loss_fn(y, c_predictions)
		a_predictions = self.adversary(c_predictions)
		a_loss = self.a_loss_fn(e_g, a_predictions)
			
		
		self.c_loss.update_state(y,c_predictions)
		self.a_loss.update_state(e_g, a_predictions)
		
		return {m.name: m.result() for m in self.metrics}


def ocean_predict(image_feature_path):

	model = AdversarialDebiasing(classifier, adversary, 1,
							   keras.metrics.MeanAbsoluteError(name="c_loss"), 
							   keras.metrics.BinaryCrossentropy(name="a_loss"),
							   debias=False,
							  )


	model.compile(
		optimizer=[keras.optimizers.SGD(nesterov=True),keras.optimizers.SGD(nesterov=True),],
		c_loss_fn = keras.losses.MeanAbsoluteError(),
		a_loss_fn = keras.losses.BinaryCrossentropy(),
	)

	model.built=True

	model.load_weights("D:\\Sarika\\PersonalityPredictionFromAVI\\models\\image 4\\debias_false 50.h5")
	frame_names = glob.glob(image_feature_path + '*')
	predictions =  np.empty((0,5))
	for frame in frame_names:
		img = image.load_img(frame, target_size=IMAGE_SIZE)
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		x/=255
		print(x.shape)
		pred = model.predict(x)[0]
		# predictions += [pred]
		predictions = np.vstack((predictions, pred))
	print(predictions.shape)
	return np.mean(predictions, axis=0)
	# return model.predict(data1)
