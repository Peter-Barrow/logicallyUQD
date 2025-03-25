from time import sleep
from logicallyUQD import UQDLogic16, LogicMode, pattern_from_channels

uqd = UQDLogic16(calibrate=False)
num_channels = uqd.number_of_channels
for ch in range(num_channels):
    uqd.input_threshold = (ch + 1, 0.1)

print(f'Found device with:\n\t# Channels: {uqd.number_of_channels}')
print(f'\tResolution: {uqd.resolution} ps')

logic = LogicMode(uqd)
read_time = 0.1

# Generate the masks to address the counters for each channel
input_channels = [pattern_from_channels([i + 1]) for i in range(num_channels)]
# Alternatively you could access coincidences likes so for coincidences between
# channels 1, 2 and 3:
#   cc_123 = pattern_from_channels([0, 1, 2])

for i in range(10):
    sleep(read_time)
    logic.read_logic()

    time = logic.get_time_counter() * 5e-9
    singles = [logic.calc_count_pos(in_ch) for in_ch in input_channels]
    singles_ext = [logic.calc_count(in_ch, 0) for in_ch in input_channels]

    # assert that both methods for getting counts from the channels is the same
    assert all([s == s_e for s, s_e in zip(singles, singles_ext)])

    print(time, singles)
