echo "1/4 Creating ~/Sonica, Installing modules and prerequisites"
mkdir ~/Sonica
cd ~/Sonica/

wget http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
tar -xf pa_stable_v190600_20161030.tgz 
mv pa_stable_v190600_20161030 portaudio
cd portaudio/

./configure
sudo make install

cd ..

sudo apt update
sudo apt install libatlas-base-dev espeak pulseaudio
python2 -m pip install python-vlc pyttsx3 numpy

echo "2/4 Opening Firefox to http://docs.kitt.ai/snowboy/"
echo "Please download the correct version of Snowboy for your system and place it in ~/Sonica"
echo "Then press Enter to continue"
firefox http://docs.kitt.ai/snowboy/#downloads
read
#wget https://s3-us-west-2.amazonaws.com/snowboy/snowboy-releases/ubuntu1404-x86_64-1.1.1.tar.bz2

echo "3/4 Extracting Snowboy"
echo "Expect some errors, these can be ignored safely"
tar -xf ubuntu1404-x86_64-1.1.1.tar.bz2
tar -xf rpi-arm-raspbian-8.0-1.1.1.tar.bz2
mv ubuntu1404-x86_64-1.1.1 snowboy
mv rpi-arm-raspbian-8.0-1.1.1 snowboy

echo "4/4 Downloading sonica.py"
wget https://github.com/sciboy12/Sonica/raw/master/sonica.py

echo "Done"
