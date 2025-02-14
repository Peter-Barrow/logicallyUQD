# Build System

Copy the CTimeTag folder into here, such that you have the following structure:

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
