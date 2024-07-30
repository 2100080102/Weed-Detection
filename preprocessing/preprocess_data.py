from tensorflow.keras import layers, models
import tensorflow as tf
from datasets.deep_weeds import DeepWeeds

# Specify the root directory for storing the datasets
data_dir = "D:\\Users\\acer\\PycharmProjects\\WeedDetection"

# Instantiate the builder
builder = DeepWeeds(data_dir=data_dir)

# Download and prepare the dataset
builder.download_and_prepare()

# Load the dataset using the builder
ds_train, ds_val = builder.as_dataset(split=['train[:80%]', 'train[80%:]'], as_supervised=True)
ds_info = builder.info

# Function to preprocess images
def preprocess_image(image, label):
    image = tf.image.resize(image, [256, 256])  # Resize images to 256x256
    image = tf.cast(image, tf.float32) / 255.0  # Normalize to [0, 1]
    return image, label

# Apply preprocessing to datasets
ds_train = ds_train.map(preprocess_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)
ds_val = ds_val.map(preprocess_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)

# Batch and shuffle the datasets
batch_size = 32
ds_train = ds_train.shuffle(1000).batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE)
ds_val = ds_val.batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE)

# # Print dataset info
# print(ds_info)

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(9, activation='softmax')  # Adjust num_classes according to your dataset
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

epochs = 1  # Adjust as needed
history = model.fit(ds_train, epochs=epochs, validation_data=ds_val)
model.save('D:\\Users\\acer\\PycharmProjects\\WeedDetection\\model\\my_model.keras')  # Use .keras extension for SavedModel format
