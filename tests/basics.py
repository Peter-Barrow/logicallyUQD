import numpy as np
from time import perf_counter_ns, sleep
from logicallyUQD import UQDLogic16

uqd = UQDLogic16(calibrate=False)

print(f'Found device with:\n\t# Channels: {uqd.number_of_channels}')
print(f'\tResolution: {uqd.resolution} ps')

print('Starting timetags')
uqd.start_timetags()

for ch in range(uqd.number_of_channels):
    uqd.input_threshold = (ch + 1, 0.1)

read_time = 0.1
samples = 4

m_time_numpy = []
print('numpy read')
for _ in range(samples):
    sleep(read_time)
    a = perf_counter_ns()
    (total, channels, timestamps) = uqd.read_tags_numpy()
    b = perf_counter_ns()
    print(total, channels, timestamps)
    # uqd.print_tags()
    # print(f'total -> {total} in {b - a}ns')
    m_time_numpy.append(b - a)


# for _ in range(samples):
#     sleep(read_time)
#     uqd.read_tags_print()


uqd.stop_timetags()
uqd.__close__()

m_time_numpy = np.array(m_time_numpy)

avrg_numpy = np.mean(m_time_numpy)
std_numpy = np.std(m_time_numpy)

print(f'Numpy:\t{avrg_numpy:.2f} +/- {std_numpy:.2f}ns')
