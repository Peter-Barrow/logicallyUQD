# logically-uqd

>> Get the features of the UQD into Python, logically...

## About
Exports the functionality of the `CTimeTag` and `CLogic` headers distributed by Universal Quantum Devices for their Logic-16 time taggers.

## Installation
**NOTE: THIS IS ONLY TESTED ON LINUX**

1. Copy the *entire* "CTimeTag" directory from the zip file UQD distribute into `logicallyUQD/opt`, you must have the following structure:
```sh
logicallyUQD
    └── opt
        ├── CTimeTag
        │   ├── Include
        │   │   ├── CLogic.h
        │   │   ├── CTimeTag.h
        │   │   └── CTimeTag.h.bak
        │   ├── Linux
        │   │   ├── libtimetag32.so
        │   │   ├── libtimetag64.so
        │   │   └── libtimetagARM.so
        │   ├── Win32
        │   │   ├── CTimeTagLibDebug.lib
        │   │   └── CTimeTagLib.lib
        │   └── Win64
        │       ├── CTimeTagLibDebug.lib
        │       └── CTimeTagLib.lib
        └── README.md <- you are here
```
The contents of the Linux, Win32 and Win64 may differ but this is not important for us.

2. Ensure that the following are installed:
    1. Python
    2. libusb (libusb1 specifically), included the development headers
    3. libtimetag32 for 32bit Linux or libtimetag64 for 64bit Linux is installed, this should be in `/lib/` or `lib64` respectively.
    4. (Optionally) Make, this should be installed by default

3. Build the library:
    Run the following:
    ```sh
	python3 -m build --wheel
    ```
    Or if you have make installed:
    ```sh
    make build
    ```
4. Install:
    ```sh
    python3 -m pip install ./dist/logicallyUQD*.whl
    ```

