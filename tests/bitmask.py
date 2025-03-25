from typing import List


def calculate_tcspc_bitmask(input_channels: List[int]) -> int:
    """
    Calculate a bitmask for TCSPC device based on input channels.

    Args:
        input_channels: List of integers representing channel numbers

    Returns:
        Integer representing the bitmask where each bit corresponds to an input channel
    """
    bitmask = 0

    for channel in input_channels:
        # Set the bit at position (channel-1)
        # For example: channel 1 sets bit 0, channel 2 sets bit 1, etc.
        bitmask |= 1 << (channel - 1)

    return bitmask


def main():
    # Test cases with assertions
    assert calculate_tcspc_bitmask([1]) == 1, (
        'Single input 1 should result in bitmask 1'
    )
    assert calculate_tcspc_bitmask([2]) == 2, (
        'Single input 2 should result in bitmask 2'
    )
    assert calculate_tcspc_bitmask([3]) == 4, (
        'Single input 3 should result in bitmask 4'
    )
    assert calculate_tcspc_bitmask([4]) == 8, (
        'Single input 4 should result in bitmask 8'
    )
    assert calculate_tcspc_bitmask([1, 2]) == 3, (
        'Inputs 1,2 should result in bitmask 3'
    )
    assert calculate_tcspc_bitmask([1, 2, 3]) == 7, (
        'Inputs 1,2,3 should result in bitmask 7'
    )

    print('All tests passed!')

    # Additional examples for demonstration
    print(f'Bitmask for channels [1]: {calculate_tcspc_bitmask([1])}')
    print(f'Bitmask for channels [2]: {calculate_tcspc_bitmask([2])}')
    print(f'Bitmask for channels [1, 2]: {calculate_tcspc_bitmask([1, 2])}')
    print(
        f'Bitmask for channels [1, 2, 3]: {calculate_tcspc_bitmask([1, 2, 3])}'
    )


if __name__ == '__main__':
    main()
