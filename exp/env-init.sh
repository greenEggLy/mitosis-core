cd /mnt/hdd/ly
mkdir -p mitosis/.base
sudo tar -C ./mitosis/.base -xf ./rootfs.tar
tar -C mitosis -xzf mitosis_app.tar.gz
tar -C mitosis -xzf mitosis_codes.tar.gz
cd mitosis/mitosis-core/mitosis-user-libs/mitosis-lean-container/lib/core 
sed -i '392s/^/\/\//' ./lean_container.c
sed -i '41s/^/\/\//' ./lean_container.c
echo 'export ROOTFS_ABS_PATH=/mnt/hdd/ly/mitosis/.base' >> ~/.bashrc && \
echo 'export work_dir=/mnt/hdd/ly/mitosis/mitosis-core/exp/criu-micro' >> ~/.bashrc && \
source ~/.bashrc
ln -s /mnt/hdd/ly/mitosis /home/liuyang/mitosis
sudo ln -s /home/liuyang /home/ly
cd /home/liuyang
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
cd /mnt/hdd/ly/mitosis/mitosis-core/exp/criu-micro
sudo touch imgs/dump.log
cd /mnt/hdd/ly/mitosis/mitosis-core/mitosis-user-libs/mitosis-lean-container/lib/build
make -j

sudo apt install libcap-dev libnl-3-dev libnet1-dev pkg-config libbsd-dev flex bison libprotobuf-dev libprotobuf-c-dev protobuf-c-compiler protobuf-compiler python-protobuf build-essential libmount-dev -y
