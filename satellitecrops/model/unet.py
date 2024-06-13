import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate, Conv2DTranspose, BatchNormalization, Dropout, Lambda
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import CategoricalFocalCrossentropy
from keras import Model

from typing import Tuple
from colorama import Fore, Style

from satellitecrops.evaluation import metrics

def categorical_focal_crossentropy_ignore(y_true, y_pred):
    print('y_true.shape: ', y_true.shape)
    print('y_pred.shape: ', y_pred.shape)
    background_classif_pixel = np.zeros(y_true.shape[-1])
    background_classif_pixel[0] = 1
    # Generate modified y_pred where all truly class0 pixels are correct
    y_true_class0_indicies = tf.where(tf.math.equal(y_true, background_classif_pixel))
    y_pred_updates = tf.repeat([
        background_classif_pixel],
        repeats=y_true_class0_indicies.shape[0],
        axis=0)
    yp = tf.tensor_scatter_nd_update(y_pred, y_true_class0_indicies, y_pred_updates)

    return CategoricalFocalCrossentropy.call(y_true, yp)


def unet(n_classes:int,
         img_height:int,
         img_width:int,
         img_channels:int,
         optimizer='adam',
         alpha:float=0.25,
         gamma:float=2.0
         ):
    '''
    Initialize and compile a Unet model. Source of model architecture (https://youtu.be/csFGTLT6_WQ).

    n_classes: The possible number of labels the prediction task can have.
    img_height: Height of the image.
    img_width: Width of the image.
    img_channels: Number of bands used to predict.
    optimizer: Optimizer used to compile.
    alpha: Categorical focal loss parameter. A weight balancing factor for all classes, default is 0.25 as mentioned in the reference. It can be a list of floats or a scalar. In the multi-class case, alpha may be set by inverse class frequency by using compute_class_weight from sklearn.utils.
    gamma: Categorical focal loss parameter. A focusing parameter, default is 2.0 as mentioned in the reference. It helps to gradually reduce the importance given to simple (easy) examples in a smooth manner.
    '''

    s = Input((img_height, img_width, img_channels))

    #Contraction path
    c1 = Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(s)
    c1 = Dropout(0.1)(c1)
    c1 = Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
    c2 = Dropout(0.1)(c2)
    c2 = Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
    c3 = Dropout(0.2)(c3)
    c3 = Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
    p3 = MaxPooling2D((2, 2))(c3)

    c4 = Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
    c4 = Dropout(0.2)(c4)
    c4 = Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
    p4 = MaxPooling2D(pool_size=(2, 2))(c4)

    c5 = Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
    c5 = Dropout(0.3)(c5)
    c5 = Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)

    #Expansive path
    u6 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
    u6 = concatenate([u6, c4])
    c6 = Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
    c6 = Dropout(0.2)(c6)
    c6 = Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)

    u7 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
    u7 = concatenate([u7, c3])
    c7 = Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
    c7 = Dropout(0.2)(c7)
    c7 = Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)

    u8 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
    u8 = concatenate([u8, c2])
    c8 = Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
    c8 = Dropout(0.1)(c8)
    c8 = Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)

    u9 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
    u9 = concatenate([u9, c1], axis=3)
    c9 = Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
    c9 = Dropout(0.1)(c9)
    c9 = Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)

    outputs = Conv2D(n_classes, 1, activation='softmax', padding='same')(c9)

    model = Model(inputs=[s], outputs=[outputs])
    model.compile(optimizer=optimizer, loss=tf.keras.losses.CategoricalFocalCrossentropy(alpha=alpha,gamma=gamma), metrics=metrics(n_classes))
    model.summary()

    return model


def train_model(model: Model,
        X: np.ndarray,
        y: np.ndarray,
        batch_size=16,
        patience=5,
        validation_data=None, # overrides validation_split
        validation_split=0.2
    ) -> Tuple[Model, dict]:
    """
    Fit the model and return a tuple (fitted_model, history)
    """
    print(Fore.BLUE + "\nTraining model..." + Style.RESET_ALL)

    es = EarlyStopping(
        monitor="val_loss",
        patience=patience,
        restore_best_weights=True,
        verbose=0
    )

    history = model.fit(
        X,
        y,
        validation_data=validation_data,
        validation_split=validation_split,
        epochs=100,
        batch_size=batch_size,
        callbacks=[es],
        verbose=0
    )

    print(f"✅ Model trained on {len(X)} rows with min val meanIoU: {round(np.min(history.history['mean_io_u']), 2)}")

    return model, history
