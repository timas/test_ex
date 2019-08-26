### Install for ubuntu
Install some system-wide depencies (if not installed):
```sh
sudo apt-get install virtualenv
sudo apt-get install python-pip
sudo apt-get install libpq-dev
sudo apt-get install xvfb
```
Create virtual environment:
```sh
virtualenv -p python3.6 test_ex
cd test_ex
. bin/activate
```
Download according version for chrome driver (check version chrome installed)
```sh
wget https://chromedriver.storage.googleapis.com/76.0.3809.126/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip
```
### Install for mac
Create virtual environment:
```sh
virtualenv -p python3.6 test_ex
cd test_ex
. bin/activate
```
Download according version for chrome driver (check version chrome installed)
```sh
wget https://chromedriver.storage.googleapis.com/76.0.3809.126/chromedriver_mac64.zip
unzip chromedriver_mac64.zip
rm chromedriver_mac64.zip
```
Clone project
```sh
git clone https://github.com/timas/test_ex.git src
cd src
pip install -r requirements.txt
```
### Usage
Under activated virtualenv run:
```sh
$ python test_1.py
$ python test_1.py
```
Or pytest for both:
```sh
$ python -m pytest .
```