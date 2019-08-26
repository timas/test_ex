

sudo apt-get install virtualenv
sudo apt-get install python3-pip
sudo apt-get install python-pip
sudo apt-get install libpq-dev


virtualenv -p python3 test_ex


pip install sshtunnel
pip install selenium

wget https://chromedriver.storage.googleapis.com/76.0.3809.126/chromedriver_linux64.zip
wget https://chromedriver.storage.googleapis.com/76.0.3809.126/chromedriver_mac64.zip
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip

sudo apt-get install xvfb
pip install PyVirtualDisplay




### Install for mac
Create virtual environment:
```sh
virtualenv -p python3.6 test_ex
cd test_ex
. bin/activate
```
Download according version for chrome driver (check version)
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


### Usage for mac
Under activated virtualenv run:
```sh
$ python test_1.py
$ python test_1.py
```
Or pytest for both:
```sh
$ python -m pytest .
```