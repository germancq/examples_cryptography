https://stackoverflow.com/questions/55380437/how-to-force-usage-of-python-3-in-cocotb

Writed by : FabienM

I found a proper way to do it.

First download the last version of python on the official website :

$ wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz

Then unflat it and configure it with the option --enable-shared

$ tar -Jxvf Python-3.7.4.tar.xz
$ cd Python-3.7.4
$ ./configure --enable-shared
$ make
$ sudo make install

Once installed go to your cocotb test directory then install virtual environment :

$ export LD_LIBRARY_PATH=/usr/local/lib
$ virtualenv --python=/usr/local/bin/python3.7 envp37
$ source envp37/bin/activate
$ python -m pip install cocotb

Then you can launch your cocotb test environment with traditional make :

$ make

Dectivate the python environment with :

$ deactivate

