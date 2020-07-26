import pandas as pd
import tensorflow as tf 




def get_compiled_model():
  model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1)
  ])

  model.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=['accuracy'])
  return model

  model = get_compiled_model()


df = pd.read_csv('file.csv')
#df.head() prints top rows
#df.dtypes prints datatypes of cols

target = df.pop('target')
dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))

#converts a col of strings into numerical values
#df['thal'] = pd.Categorical(df['thal'])
#df['thal'] = df.thal.cat.codes
model.fit(train_dataset, epochs=3)