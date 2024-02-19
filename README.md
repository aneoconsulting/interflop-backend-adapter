# Interflop Backend Adapter

The interflop backend take an interflop backend and adapt it for any of the three tool Verrou,
~~Verificarlo and PENE~~. (Only Verrou for now)


## Requirements

- cmake version >= 3.20
- python3
- jinja2

    ### For Verrou

    Coming soon

    ### For Verificarlo

    Coming soon

    ### For Verrou
    Follow the Configure and build requirements of the README in the [Verrou repository](https://github.com/edf-hpc/verrou) (The one bellow may not be up to date):
    - C & C++ compilers (build-essential),
    - autoconf & automake (automake),
    - Python 3 (python3)
    - C standard library with debugging symbols (libc6-dbg).


## Installation

First, clone the repository and create a "verrou_repo" folder in verrou_files

```bash
cd [ interflop-backend-adapter repository ]
mkdir verrou_files/verrou_repo
```

You should then clone Valgrind and Verrou. If something doesn't seems to be wrong with the installation below, it may not be up to date and you should go see the Verrou installation guide in the [Verrou repository](https://github.com/edf-hpc/verrou).

```bash
cd verrou_files/verrou_repo

git clone --branch=VALGRIND_3_22_0 --single-branch git://sourceware.org/git/valgrind.git valgrind-3.22.0+verrou-dev

cd valgrind-3.22.0+verrou-dev
git clone https://github.com/edf-hpc/verrou.git verrou

patch -p1 <verrou/valgrind.diff
```

## Configure and build


For any build you need, you should use Cmake with the good options.

```
-BUILD_FOR_PENE=ON for PENE
-BUILD_FOR_VERIFICARLO=ON for Verificarlo
-DBUILD_FOR_VERROU=ON for Verrou
```

### For PENE

Coming soon

### For Verificarlo

Coming soon

### For Verrou

```bash
mkdir build
cd build
cmake .. -DBUILD_FOR_VERROU=ON
```
Once the build finished, you should source on the "verrou_files/verrou_repo/verrou_software/env.sh" and you will be able to use your backend using the name you gived to it.


## Write a new backend

Create a folder with the name you want for your backend in the backend folder.
Your functions should be written in a file "backend.cpp" with specific names and syntax:

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

For each possible functions, you should write it like that:

```c
add_float:
    {BODY OF YOUR FUNCTION}
end_add_float

madd_float:
    {BODY OF YOUR FUNCTION}
end_madd_float

etc...
```