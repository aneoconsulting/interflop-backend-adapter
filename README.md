# Interflop Backend Adapter

The interflop backend adapter take an interflop backend and adapt it for any of the three tools Verrou, Verificarlo and PENE.


## Requirements

### Global

- cmake version >= 3.20
- make
- python3
- jinja2

### For PENE

Follow the Requirements section of the README in the [PENE repository](https://github.com/aneoconsulting/pene) (The one bellow may not be up to date):
- g++ compiler for Linux and MSVC compiler for Windows
- pytest

### For Verificarlo

No particular specification to build custom backends for Verificarlo

### For Verrou
Follow the Configure and build requirements section of the README in the [Verrou repository](https://github.com/edf-hpc/verrou) (The one bellow may not be up to date):
- C & C++ compilers (build-essential)
- autoconf & automake (automake)
- Python 3 (python3)
- C standard library with debugging symbols (libc6-dbg)


## Installation

Clone the repository and get into it
```bash
git clone git@github.com:aneoconsulting/interflop-backend-adapter.git
cd interflop-backend-adapter
```

From here, only follow the part of the guide with the backend(s) that interest you


### For PENE

Get into the "pene_files" folder and clone the PENE repository

```bash
cd pene_files
git clone git@github.com:aneoconsulting/PENE.git
```

Once done, you have all the installation requirements to build a custom backend on PENE

### For Verificarlo

There is no specific installation to do, you can already build a backend for Verificarlo

### For Verrou

First, create a "verrou_repo" folder in verrou_files and get into it

```bash
mkdir verrou_files/verrou_repo
cd verrou_files/verrou_repo
```

You should then clone Valgrind and Verrou\
If something seems to be wrong with the installation guide below, then it may be out of date, you should go see the Verrou installation guide in the [Verrou repository](https://github.com/edf-hpc/verrou)

```bash
cd verrou_files/verrou_repo

git clone --branch=VALGRIND_3_22_0 --single-branch git://sourceware.org/git/valgrind.git valgrind-3.22.0+verrou-dev

cd valgrind-3.22.0+verrou-dev
git clone https://github.com/edf-hpc/verrou.git verrou

patch -p1 <verrou/valgrind.diff>
```

Once done, you have all the installation requirements to build a custom backend on Verrou

## Configure and build


For any build you need, you should use Cmake with the good options

```
-DBUILD_FOR_PENE=ON for PENE
-DBUILD_FOR_VERIFICARLO=ON for Verificarlo
-DBUILD_FOR_VERROU=ON for Verrou
```

### For PENE

```bash
mkdir build
cd build
cmake .. -DBUILD_FOR_PENE=ON
```
Once the building is done, you can use the pin binary created in the PENE repository.

### For Verificarlo

```bash
mkdir build
cd build
cmake .. -DBUILD_FOR_VERIFICARLO=ON
```
Once the building is done, all the backend's shared objects are in the "backends_so" folder and you can use them in a environnement var with a Verificarlo compiled binary

### For Verrou

```bash
mkdir build
cd build
cmake .. -DBUILD_FOR_VERROU=ON
```
Once the building is done, you should source on the "verrou_files/verrou_repo/verrou_software/env.sh" and you will be able to use your backend using the name you given to it

### For All frontends

```bash
mkdir build
cd build
cmake .. -DBUILD_FOR_PENE=ON -DBUILD_FOR_VERIFICARLO=ON -DBUILD_FOR_VERROU=ON
```


## Writing a new backend

Create a folder in the backend folder with the name you want
Your functions should be written in a file "backend.cpp" with specific names and syntax
Only C code is allowed in the body of the functions

```bash
mkdir backend/{your_backend_name}
cd backend/{your_backend_name}
touch backend.cpp
```

All currently implemented functions:

- add_float
- add_double
- sub_float
- sub_double
- mul_float
- mul_double
- div_float
- div_double
- madd_float
- madd_double
- sqrt_float
- sqrt_double

For each possible function, you should write it like that:

```c
add_float:
    {BODY OF YOUR FUNCTION}
end_add_float

madd_float:
    {BODY OF YOUR FUNCTION}
end_madd_float

etc...
```

Any writing between the functions will be ignored.