wget http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.40.1.tar.gz
tar -xvzf graphviz-2.40.1.tar.gz
cd graphviz-2.40.1/
sudo apt install libgts-dev -y
pkg-config --libs gts
pkg-config --cflags gts
./configure --with-gts  --prefix ~
make
sudo make install
sudo apt-get install graphviz -y
cd ..


