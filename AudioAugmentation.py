import librosa
import numpy as np
import matplotlib.pyplot as plt
import json
import os.path
import logging
import logging.handlers
import datetime
from operator import eq
import soundfile as sf
import wave

#############################################
# YOU MUST EDIT ONLY THIS SECTION

work_param_path = './json/work_param.json'
work_info_path  = './log/work_info.json'


#############################################
class AudioInformation:
    info    = []
    path    = ''
    name    = ''
    ext     = ''
    ch      = 0             # 1 : mono, 2 : stereo or N channel
    rate    = 0             # Hz
    depth   = 0             # byte
    len     = 0
    data    = []

    def __init__(self):
        self.info   = []
        self.path   = ''
        self.name   = ''
        self.ext    = ''
        self.ch     = 0
        self.rate   = 0
        self.depth  = 0
        self.len    = 0
        self.data   = []

    def read_audio_file(self, path):
        path = path.rstrip()
        try:
            if os.path.isfile(path):
                self.info   = sf.SoundFile(path)
                self.path   = path
                self.name   = os.path.basename(self.path)
                self.ext    = os.path.splitext(self.path)[1]
                self.ch     = self.info.channels
                self.rate   = self.info.samplerate
                if eq(self.info.subtype, 'PCM_16'):
                    self.depth  = 16
                self.data   = librosa.core.load(self.path)[0]
                self.len    = len(self.data)
                return 0
            else:
                log.debug('%s is not exist' % os.path.basename(path))
                return 1
        except ValueError:
            self.__init__()
            return 1

    # def print_audio_info(self):

    def write_audio_file(self, file, data, sample_rate=16000):
        librosa.output.write_wav(file, data, sample_rate)


class AudioAugmentation:
    work_param  = []        #
    work_info   = []

    def load_work_param(self, path):
        path = path.rstrip()
        try:
            if os.path.isfile(path):
                with open(path, 'r') as f:
                    self.work_param = json.load(fp=f)
                log.debug('load_work_param is finished')
            else:
                log.debug('%s is not exist' % os.path.basename(path))
                exit()
        except ValueError:
            log.debug('load_work_param is failed')
            exit()

    def normalize(self, path):
        print(path)

    def plot_time_series(self, data):
        fig = plt.figure(figsize=(14, 8))
        plt.title('Raw wave ')
        plt.ylabel('Amplitude')
        plt.plot(np.linspace(0, 1, len(data)), data)
        plt.show()

    def add_noise(self, data):
        noise = np.random.randn(len(data))
        data_noise = data + 0.005 * noise
        return data_noise

    def shift(self, data):
        return np.roll(data, 1600)

    def stretch(self, data, rate=1):
        input_length = 16000
        data = librosa.effects.time_stretch(data, rate)
        if len(data) > input_length:
            data = data[:input_length]
        else:
            data = np.pad(data, (0, max(0, input_length - len(data))), 'constant')
        return data


# Set environment variable
log_format  = logging.Formatter('[%(levelname)s] [%(funcName)s(%(lineno)d)] : %(message)s')

log_stream  = logging.StreamHandler()
log_stream.setFormatter(log_format)

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(log_stream)

time_info   = datetime.datetime.now()
time_str    = f'{time_info.year%100:02}{time_info.month:02}{time_info.day:02}_' \
              f'{time_info.hour:02}{time_info.minute:02}{time_info.second:02}'

# Create a new instance from class
AA = AudioAugmentation()
AI_in = AudioInformation()
AI_out = AudioInformation()

# Decode augmentation parameter json file
AA.load_work_param(work_param_path)

# print(json.dumps(AA.work_param, indent='\t'))
# log.debug(json.dumps(AA.work_param['work_order'][0], indent='\t'))

# Read input list or file
in_fp = open(AA.work_param['input_path'], 'r')
for ai, in_path in enumerate(in_fp.readlines()):
    AI_in.read_audio_file(in_path)

    for wi, work in enumerate(AA.work_param.get('work_list')):
        if eq('normalize', work['todo']):
            out_data = AA.normalize(in_path)
        # elif eq('add_noise', work['todo']):
        #     AA.add_noise()
        # elif eq('shift', work['todo']):
        #     AA.shift()
        # elif eq('stretch', work['todo']):
        #     AA.stretch()
        # elif eq('pitch', work['todo']):
        #     AA.pitch()
        # elif eq('convolution', work['todo']):
        #     AA.convolution()
        # elif eq('cut', work['todo']):
        #     AA.cut()
        # else:
            # log.debug('Work to do is unknown')







    # for fi, file in enumerate(in_fp.readlines()):


exit()

#
# data = AA.read_audio_file('data/cat.wav')
# AA.plot_time_series(data)
#
# # Adding noise to sound
# data_noise = AA.add_noise(data)
# AA.plot_time_series(data_noise)
#
# # Shifting the sound
# data_roll = AA.shift(data)
# AA.plot_time_series(data_roll)
#
# # Stretching the sound
# data_stretch = AA.stretch(data, 0.8)
# AA.plot_time_series(data_stretch)
#
# # Write generated cat sounds
# AA.write_audio_file('output/generated_cat1.wav', data_noise)
# AA.write_audio_file('output/generated_cat2.wav', data_roll)
# AA.write_audio_file('output/generated_cat3.wav', data_stretch)
