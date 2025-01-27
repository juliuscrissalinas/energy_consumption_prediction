from ec_prediction.assets import constants
from dagster import job, asset, multi_asset, AssetOut, Output, Any
import numpy as np
from keras import layers
from keras.layers import BatchNormalization, Dropout
from keras.models import Sequential
from tensorflow.keras.optimizers.legacy import RMSprop
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from keras.callbacks import Callback


# Define the LivePlot callback to plot training and validation loss in real time
class LivePlot(Callback):
    def on_train_begin(self, logs={}):
        self.epoch = 0
        self.history = {"loss": [], "val_loss": []}

    def on_epoch_end(self, epoch, logs={}):
        self.history["loss"].append(logs.get("loss"))
        self.history["val_loss"].append(logs.get("val_loss"))
        self.epoch += 1
        
        # Clear the current figure to avoid overlaying old plots
        plt.clf()

        # Plot the training and validation loss
        plt.figure(figsize=(10, 5))
        plt.plot(self.history["loss"], label="Training Loss")
        plt.plot(self.history["val_loss"], label="Validation Loss")
        plt.title("Training and Validation Loss")
        plt.xlabel("Epochs")
        plt.ylabel("Loss")
        plt.legend()
        plt.grid(True)
        plt.draw()
        plt.pause(0.001)
# Instantiate the LivePlot callback
live_plot = LivePlot()

@asset(
    group_name='data_transformation'
)
def read_pjmw_data(context) -> list:
    """
      Read PJMW hourly dataset from Kaggle  
    """
    f = open(constants.PJMW_HOURLY_PATH)
    data = f.read()
    f.close()
    lines = data.split("\n")
    header = lines[0].split(",")
    lines = lines[1:]
    print(header)
    print(type(lines))
    context.log.info(f"Lines of data:\n{lines}")
    return lines

@asset(
    group_name='data_transformation',
    deps = ['read_pjmw_data']
)
def convert_to_float(context, read_pjmw_data: list) -> np.ndarray:
    """
      Convert string PJMW_MW column to float
    """

    float_data = np.zeros((len(read_pjmw_data), 1))

    for i, line in enumerate(read_pjmw_data):
        # Split each line on the comma
        parts = line.split(",")

        # Check if the line has exactly two parts: Datetime and PJMW_MW
        if len(parts) != 2:
            context.log.warning(f"Skipping line {i} due to unexpected format: {line}")
            continue

        try:
            # Extract and convert the PJMW_MW value to float
            value = float(parts[1].strip())
            float_data[i, 0] = value
        except ValueError as e:
            context.log.error(f"Skipping line {i} due to conversion error: {line}, Error: {e}")
    
    context.log.info(f"First 5 rows of float_data:\n{float_data[:5].flatten()}")
    return float_data

@asset(
    group_name='data_transformation',
    deps = ['convert_to_float']
)
def normalize_data(context, convert_to_float) -> np.ndarray:
    """
    Normalize data
    """
    # Calculate the mean and standard deviation from the first 70000 rows
    mean = convert_to_float[:70000].mean(axis=0)
    std = convert_to_float[:70000].std(axis=0)
    
    # Perform normalization
    normalized_data = convert_to_float.copy()  # Create a copy to avoid modifying the original data
    normalized_data -= mean
    normalized_data /= std

    # Log details for debugging
    context.log.info(f"Mean: {mean}, Std: {std}")
    context.log.info(f"First 5 rows of normalized data:\n{normalized_data[:5].flatten()}")

    return normalized_data

# A wrapper class for the generator
class GeneratorWrapper:
    def __init__(self, gen_func, *args, **kwargs):
        self.gen_func = gen_func  # Store the generator function
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        return self.gen_func(*self.args, **self.kwargs)  # Recreate the generator

# Generator function
def generator(
    data,
    lookback,
    delay,
    min_index,
    max_index,
    shuffle=False,
    batch_size=128,
    step=12,
    num_outputs=1,
    target_i=0,
):
    if max_index is None:
        max_index = len(data) - delay - 1

    i = min_index + lookback
    while True:
        if shuffle:
            rows = np.random.randint(min_index + lookback, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)

        samples = np.zeros((len(rows), lookback // step, data.shape[-1]))
        targets = np.zeros((len(rows), num_outputs))

        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            if data.shape[-1] == 1:
                targets[j] = data[rows[j] + delay : rows[j] + delay + num_outputs * step : step, 0]
            else:
                targets[j] = data[rows[j] + delay : rows[j] + delay + num_outputs * step, target_i]

        yield samples, targets

@multi_asset(
    group_name= "train_test_split",
    deps = ['normalize_data'],
    outs = {
        "training_data" : AssetOut(),
        "test_data" : AssetOut(),
        "validation_data" : AssetOut(),
    }
)
def train_test_val(context, normalize_data):
    """
    Generate train, test, and validation data as generator outputs.
    """
    float_data = normalize_data
    lookback = 1 * 24 * 30
    step = 12
    delay = 30 * 24
    batch_size = 128

    # Wrap generators in GeneratorWrapper
    train_gen = GeneratorWrapper(
        generator,
        float_data,
        lookback,
        delay,
        min_index=0,
        max_index=100000,
        shuffle=True,
        step=step,
        batch_size=batch_size,
        num_outputs=24,
        target_i=0,
    )

    val_gen = GeneratorWrapper(
        generator,
        float_data,
        lookback,
        delay,
        min_index=100001,
        max_index=121600,
        shuffle=False,
        step=step,
        batch_size=batch_size,
        num_outputs=24,
        target_i=0,
    )

    test_gen = GeneratorWrapper(
        generator,
        float_data,
        lookback,
        delay,
        min_index=121601,
        max_index=None,
        shuffle=False,
        step=step,
        batch_size=batch_size,
        num_outputs=24,
        target_i=0,
    )
    print
    # Yield wrapped generators as outputs
    yield Output(train_gen, output_name="training_data")
    yield Output(val_gen, output_name="validation_data")
    yield Output(test_gen, output_name="test_data")

@asset(
    group_name="model_training",
    deps=["training_data", "validation_data", "normalize_data"]
)
def train_gru_dropout(context, training_data, validation_data, normalize_data) -> str:
    """
    Train a GRU model with dropout and return the trained model.
    """
    # Convert the data into iterators
    train_gen = iter(training_data)  # Convert GeneratorWrapper to an iterator
    val_gen = iter(validation_data)  # Convert GeneratorWrapper to an iterator
    float_data = normalize_data
    
    # Define the model
    model = Sequential()
    model.add(
        layers.GRU(
            32,
            dropout=0.2,
            recurrent_dropout=0.2,
            input_shape=(None, float_data.shape[-1]),
        )
    )
    model.add(layers.Dense(24))

    # Compile the model with the RMSprop optimizer
    model.compile(optimizer=RMSprop(learning_rate=0.001), loss="mae")

    # Train the model
    model.fit(
        train_gen,
        steps_per_epoch=1000,
        epochs=10,
        validation_data=val_gen,
        validation_steps=2000,
        # callbacks=[live_plot],
    )

    # Save the model to disk
    model_path = "trained_model.h5"
    model.save(model_path)
    context.log.info(f"model path: {model_path}")
    # Ensure you return the model wrapped in Output with proper type annotation
    return model_path

@asset(
    group_name="model_prediction",
    deps=["train_gru_dropout", "validation_data"]
)
def generate_predictions(train_gru_dropout: str, validation_data) -> np.ndarray:
    """
    Load the trained model from the specified path and use it to generate predictions.
    """
    val_gen = iter(validation_data)
    vg = []
    for i in range(1000):
        vg.append(next(val_gen))
    model_path = train_gru_dropout
    # Load the trained model
    model = load_model(model_path)
    vg_pred2= model.predict(vg[1][0]) #predict inputs of next 1280 mins

    plt.plot(vg[1][1], label='Actual')
    plt.plot(vg_pred2, label='Predicted')

    plt.legend()
    plt.savefig('plot.png', format='png')
    plt.show()
    print("Predictions generated successfully.")
    return vg_pred2

@job
def my_job():
    float_data = convert_to_float(read_pjmw_data())