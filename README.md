

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



### Usage
Under activated virtualenv run:
```sh
$ python test_1.py
$ python test_1.py
```
Or simple pytest for both:
```sh
$ pytest
```