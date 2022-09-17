from flask import Flask, render_template, url_for, request
import argparse
import time

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels
from brainflow.data_filter import DataFilter
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def home():
    return render_template("index.html")


@app.route('/result/', methods=['POST', 'GET'])
def result():
    BoardShim.enable_board_logger()
    DataFilter.enable_data_logger()
    MLModel.enable_ml_logger()

    params = BrainFlowInputParams()
    params.board_id = -1
    board_id = -1
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    params = BrainFlowInputParams()
    # params.serial_port = 'COM6'

    board = BoardShim(-1, params)
    master_board_id = board.get_board_id()
    sampling_rate = BoardShim.get_sampling_rate(master_board_id)
    board.prepare_session()
    board.start_stream(45000)
    BoardShim.log_message(LogLevels.LEVEL_INFO.value,
                          'start sleeping in the main thread')
    # recommended window size for eeg metric calculation is at least 4 seconds, bigger is better
    time.sleep(5)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(int(master_board_id))
    bands = DataFilter.get_avg_band_powers(
        data, eeg_channels, sampling_rate, True)
    feature_vector = bands[0]
    print(feature_vector)
    print(eeg_channels[0])

    mindfulness_params = BrainFlowModelParams(BrainFlowMetrics.MINDFULNESS.value,
                                              BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
    mindfulness = MLModel(mindfulness_params)
    mindfulness.prepare()
    print('Concentration: %s' % str(mindfulness.predict(feature_vector)))
    if mindfulness.predict(feature_vector) > 0.75:
        print("Beta")
        print("Showing meditation image")
    elif mindfulness.predict(feature_vector) > 0.5 < 0.75:
        print("Alpha")
    elif mindfulness.predict(feature_vector) > 0.25 < 0.5:
        print("Theta")
    else:
        print("Bro's extremely excited")
    mindfulness.release()

    restfulness_params = BrainFlowModelParams(BrainFlowMetrics.RESTFULNESS.value,
                                              BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
    restfulness = MLModel(restfulness_params)
    restfulness.prepare()
    print('Restfulness: %s' % str(restfulness.predict(feature_vector)))
    restfulness.release()

    return render_template('results.html')


if __name__ == "__main__":
    app.run(debug=True)
