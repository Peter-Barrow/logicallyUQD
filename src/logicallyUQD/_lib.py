import cython
import time
from cython.cimports import _lib as _lib
from cython.cimports.libcpp import bool as cbool
from typing import List, Tuple
from cython.cimports.libc.stdint import uint8_t as u8
from cython.cimports.libc.stdint import uint32_t as u32
from cython.cimports.libc.stdint import uint64_t as u64
from numpy import ndarray, zeros, uint8, uint64, float64

# from cython.cimports import _tangy


UQD_ERROR_FLAG = {
    1: (
        'DataOverflow',
        'An overflow in the 512 k values SRAM FIFO has been detected. \
        The time-tag generation rate is higher than the USB transmission rate.',
    ),
    2: ('NegFifoOverflow', 'Internal reason, should never occur'),
    4: ('PosFifoOverflow', 'Internal reason, should never occur'),
    8: (
        'DoubleError',
        'One input had two pulses within the coincidence window.',
    ),
    16: (
        'InputFifoOverflow',
        'More than 1024 successive tags were detected with a rate greater 100 MHz',
    ),
    32: (
        '10MHzHardError',
        'The 10 MHz input is not connected or connected to a wrong type of signal.',
    ),
    64: (
        '10MHzSoftError',
        'The 10 MHz input is connected, but the frequency is not 10 MHz.',
    ),
    128: ('OutFifoOverflow', 'Internal error, should never occur'),
    256: (
        'OutDoublePulse',
        'An output pulse was generated, while another pulse was still present \
        on the same output. The pulse length is too long for the given rate.',
    ),
    512: (
        'OutTooLate',
        'The internal processing was too slow. This is because the output \
        event queue is too small for the given rate. Increase the value with \
        SetOutputEventQueue()',
    ),
}


@cython.ccall
def error_from_bit_set(bit_set: int) -> List[int]:
    bits = zeros(16, dtype=uint8)
    i: cython.Py_ssize_t = 0
    x: u32
    for i in range(16):
        x = bit_set >> i
        if x & 1:
            bits[15 - i] = 2**i
    return bits


@cython.cclass
class UQDLogic16:
    """

    NOTE:
        Linux users will need to add the following file to their system, \
        ``/etc/udev/rules.d/UQDLogic16.rules`` that contains the following line \
        ``ATTR{idVendor}=="0bd0", ATTR{idProduct}=="f100", MODE="666"``. This \
        will ensure that the device does not need additional root privaledges to \
        operate. After this file has been created the user will have to log out \
        and the log in again or run the following command \
        ``sudo udevadm control --reload-rules && udevadm trigger`` to update the \
        current device rules.

    """

    _c_timetag: _lib.CTimeTag_ptr

    _channel_ptr: cython.pointer(_lib.c_ChannelType)
    _timetag_ptr: cython.pointer(_lib.c_TimeType)

    _device_id: cython.int
    _number_of_channels: cython.int
    _led_brightness: cython.int
    _filter_min_count: cython.int
    _filter_max_time: cython.double
    _logic_enabled: cython.int
    _gating_enabled: cython.int
    _input_thresholds: ndarray(float64)
    _inversion: ndarray(uint8)
    _input_delay: ndarray(float64)
    _function_generator_period: int
    _function_generator_high: int
    _exclusion: ndarray(uint8)
    _10MHz: cbool = False
    _time_gate: cbool = False
    _gate_width: int

    def __init__(
        self,
        device_id: int = 1,
        calibrate: bool = True,
    ):
        if device_id < 1:
            raise ValueError('device_id must be >= 1')

        self._c_timetag = _lib.CTimeTag_create()

        if self.is_open() is True:
            raise ResourceWarning(f'Device with id={device_id} in use')

        self._device_id = device_id
        # self._c_timetag.Open(device_id)
        _lib.CTimeTag_open(self._c_timetag, device_id)
        self._input_thresholds = zeros(self.number_of_channels, dtype=float64)
        self._inversion = zeros(self.number_of_channels, dtype=uint8)
        self._input_delay = zeros(self.number_of_channels, dtype=float64)
        self._exclusion = zeros(self.number_of_channels, dtype=uint8)

        if calibrate is True:
            self.calibrate()

        return

    def is_open(self) -> bool:
        res: int = _lib.CTimeTag_isOpen(self._c_timetag)
        if res == 1:
            return True

        return False

    def __close__(self):
        print('Gracefully closing connection to device...')
        _lib.CTimeTag_destroy(self._c_timetag)

    def __exit__(self):
        print('Gracefully closing connection to device...')
        _lib.CTimeTag_destroy(self._c_timetag)

    def calibrate(self):
        _lib.CTimeTag_calibrate(self._c_timetag)

    @property
    def led_brightness(self) -> int:
        """
        Brightness of front panel LED.

        Args:
            percent (int): brightness in percent
        """
        return self._led_brightness

    @led_brightness.setter
    def led_brightness(self, percent: int):
        """
        Brightness of front panel LED.

        Returns:
            percent (int): brightness in percent
        """
        if (percent < 0) or (percent > 100):
            raise ValueError(
                'led_brightness must be in an integer between 0 and 100'
            )

        _lib.CTimeTag_setLedBrightness(self._c_timetag, percent)
        self._led_brightness = percent

    @property
    def fpga_version(self) -> cython.int:
        """
        Version of FPGA design on device.

        Returns:
            (int): fpga design version
        """
        return _lib.CTimeTag_getResolution(self._c_timetag)

    @property
    def resolution(self) -> float:
        """
        Get the resolution of the device.

        Depending on the device firmware this will return either 78.125ps or
        156.25ps.

        Returns:
            (float): resolution
        """
        res: cython.double = _lib.CTimeTag_getResolution(self._c_timetag)
        return res

    @property
    def number_of_channels(self) -> int:
        """
        Number of channels enabled on the device.

        Depending on loaded firmware this will return either 8 or 16

        Returns:
            (int): number of usable input channels
        """
        return _lib.CTimeTag_getNoInputs(self._c_timetag)

    @property
    def input_threshold(self) -> List[float64]:
        """
        Input thresholds

        Returns:
            List[float64]: Currently set input thresholds
        """
        return self._input_thresholds

    @input_threshold.setter
    def input_threshold(self, value: Tuple[int, float64]):
        """
        Set input threshold for a channel.

        Takes a tuple in the form Tuple[channel, voltage], channel is the range
        0 <= channel < UQD.number_of_channels and voltage must be the range of
        -2V to + 2V in steps of 15mV

        Args:
            value (Tuple[int, float64]): Tuple of (channel, voltage)

        """

        n: int = self.number_of_channels
        channel: int = value[0]
        if (channel < 1) or (channel > n):
            raise ValueError(f'channel must be in range 0 <= channel < {n}')

        voltage: float64 = value[1]
        if abs(voltage) > 2:
            raise ValueError('abs(voltage) must be <= 2V')

        self._input_thresholds[channel - 1] = voltage
        _lib.CTimeTag_setInputThreshold(self._c_timetag, channel, voltage)

    @property
    def inversion(self) -> List[uint8]:
        """
        Channels set to use negative edge triggering

        Returns:
            (List[uint8]): List of channels set to trigger on negative edges
        """
        return self._inversion

    @inversion.setter
    def inversion(self, invert: Tuple[uint8, uint8]):
        """
        Channels set to use negative edge triggering

        Args:
            channel (uint8): channel to enable negative edge triggering on
        """

        channel: int = invert[0]
        mask: int = invert[1]

        n: int = self.number_of_channels
        if (channel < 0) or (channel >= n):
            raise ValueError(f'channel must be in range 0 <= channel < {n}')
        self._inversion[channel] = mask

    @cython.ccall
    def inversion_apply(self):
        bits = self.inversion
        # bits.reverse()
        bit_string = ''
        for b in bits[::-1]:
            bit_string += str(b)
        mask: cython.int = int(bit_string, 2)
        _lib.CTimeTag_setInversionMask(self._c_timetag, mask)

    @property
    def input_delay(self) -> float64:
        """
        Delays in seconds set on each channel

        Returns:
            (float64): delays on each channel in seconds
        """
        return self._input_delay

    @input_delay.setter
    def input_delay(self, value: Tuple[int, float64]):
        """
        Set delay of input channel

        Args:
            value (Tuple[int, float64]): Tuple of (channel, delay)
        """

        n: int = self.number_of_channels
        channel: int = value[0]
        if (channel < 0) or (channel >= n):
            raise ValueError(f'channel must be in range 0 <= channel < {n}')

        max_delay: float = ((2**18) - 1) * self.resolution
        delay: int = value[0] // self.resolution
        if (delay < 0) or (delay > max_delay):
            raise ValueError(
                f'Delay is out of range, must be >= 0 or < {max_delay}s'
            )

        self._input_delay[channel] = delay
        _lib.CTimeTag_setDelay(self._c_timetag, channel, delay)

    @property
    def external_10MHz_reference(self) -> bool:
        """ """
        return self._10MHz

    @external_10MHz_reference.setter
    def external_10MHz_reference(self, value: bool):
        use: cbool
        if value is True:
            use = True
        else:
            use = False

        _lib.CTimeTag_use10MHz(self._c_timetag, use)
        self._external_10MHz_reference = value

    def start_timetags(self):
        """
        Start transmitting timetags from the device to the host computer
        """

        if self._have_buffer is True:
            self._buffer.clear()

        _lib.CTimeTag_startTimetags(self._c_timetag)

    def stop_timetags(self):
        """
        Stop transmitting timetags from the device to the host computer
        """
        _lib.CTimeTag_stopTimetags(self._c_timetag)

    @cython.ccall
    def read_tags(self) -> Tuple[int, List[uint8], List[uint64]]:
        count: int = _lib.CTimeTag_readTags(
            self._c_timetag, self._channel_ptr, self._timetag_ptr
        )
        count: int = 10
        channel_arr: uint8[:] = zeros(count, dtype=uint8)
        timetag_arr: uint64[:] = zeros(count, dtype=uint64)

        channel_view: u8[:] = channel_arr
        timetag_view: u64[:] = timetag_arr

        i: cython.Py_ssize_t
        for i in range(count):
            channel_view[i] = channel_arr[i]
            timetag_view[i] = timetag_arr[i]

        return (count, channel_arr, timetag_arr)

    @property
    def filter_min_count(self) -> int:
        """
        Minimum size of a group to be transmitted to the host computer.

        Returns:
            (int): Minimum size of a group to be transmitted
        """
        return self._filter_min_count

    @filter_min_count.setter
    def filter_min_count(self, count: int):
        """
        Set the minimum size of a group

        Args:
            count (int): size of group
        """
        if (count < 1) and (count > 10):
            raise ValueError('Count filter must be between 1 and 10')
        self._filter_min_count = count
        _lib.CTimeTag_setFilterMinCount(self._c_timetag, count)

    @property
    def filter_max_time(self) -> cython.double:
        """
        Maximum time between two pulses in the same group.

        Returns:
            (float): maximum time between two pulses in the same group
        """
        return self._filter_max_time

    @filter_max_time.setter
    def filter_max_time(self, max_time: cython.double):
        """
        Maximum time between two pulses in the same group.

        Args:
            time (float): maximum time between two pulses in the same group
        """
        bins: int = max_time // self.resolution
        self._filter_max_time = time
        _lib.CTimeTag_setFilterMaxTime(self._c_timetag, bins)

    @property
    def exclusion(self) -> List[uint8]:
        """ """
        return self._exclusion

    @exclusion.setter
    def exclusion(self, value: Tuple[int, int]):
        n: int = self.number_of_channels
        channel: int = value[0]
        mask: int = value[1]
        if (channel < 0) or (channel >= n):
            raise ValueError(f'channel must be in range 0 <= channel < {n}')
        _lib.CTimeTag_setFilterException(self._c_timetag, channel)
        self._exclusion[channel] = mask

    @cython.ccall
    def exclusion_apply(self):
        bits = self.exclusion
        if sum(bits) == 0:
            _lib.CTimeTag_setInversionMask(self._c_timetag, 0)
            return

        if sum(bits) == self.number_of_channels:
            _lib.CTimeTag_setInversionMask(self._c_timetag, 0)
            return

        # bits.reverse()
        bit_string = ''
        for b in bits[::-1]:
            bit_string += str(b)
        mask: cython.int = int(bit_string, 2)
        _lib.CTimeTag_setInversionMask(self._c_timetag, mask)

    @property
    def level_gate(self) -> bool:
        """ """
        return _lib.CTimeTag_levelGateActive(self._c_timetag)

    @level_gate.setter
    def level_gate(self, value: bool):
        use: cbool
        if value is True:
            use = True
        else:
            use = False

        _lib.CTimeTag_useLevelGate(self._c_timetag, use)


@cython.cclass
class LogicMode:
    _uqd_logic16: UQDLogic16
    _c_logic: _lib.CLogic_ptr

    def __init__(self, uqd_logic16):
        self._uqd_logic16 = uqd_logic16
        self._c_logic = _lib.CLogic_create(self._uqd_logic16._c_timetag)
        # self._c_logic = _get_logic(uqd_logic16)
        _lib.CLogic_switchLogicMode(self._c_logic)
        return

    def switch_logic_mode(self):
        _lib.CLogic_switchLogicMode(self._c_logic)

    def set_window_width(self, window: int):
        _lib.CLogic_setWindowWidth(self._c_logic, window)

    def set_window_width_ex(self, index: int, window: int):
        _lib.CLogic_setWindowWidthEx(self._c_logic, index, window)

    def set_delay(self, channel: int, delay: int):
        _lib.CLogic_setDelay(self._c_logic, channel, delay)

    def read_logic(self):
        result: int = _lib.CLogic_readLogic(self._c_logic)
        return result

    def calc_count_pos(self, pattern: int):
        result: int = _lib.CLogic_calcCountPos(self._c_logic, pattern)
        return result

    def calc_count(self, positive: int, negative: int):
        result: int = _lib.CLogic_calcCount(self._c_logic, positive, negative)
        return result

    def get_time_counter(self):
        result: int = _lib.CLogic_getTimeCounter(self._c_logic)
        return result

    def set_output_width(self, width: int):
        _lib.CLogic_setOutputWidth(self._c_logic, width)

    def set_output_pattern(self, output: int, positive: int, negative: int):
        _lib.CLogic_setOutputPattern(self._c_logic, output, positive, negative)

    def set_output_event_count(self, events: int):
        _lib.CLogic_setOutputEventCount(self._c_logic, events)
