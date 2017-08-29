# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/centos-7.2"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network :forwarded_port, guest: 22, host: 3300

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network :private_network, ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network :public_network

  # If true, then any SSH connections made will enable agent forwarding.
  # Default value: false
  # config.ssh.forward_agent = true

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder "../takler-monitor-test", "/takler-monitor-test"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider :virtualbox do |vb|
    # Don't boot with headless mode
    # vb.gui = true

    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "2048"]
  end


  config.vm.provision "shell", inline: <<-SHELL
    echo "Installing softwares..."
    yum groups mark convert
    yum group install -y "Development tools"
    yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
    yum install -y epel-release

    echo "Installing python 3..."
    cd /home/vagrant
    mkdir app
    cd app
    wget -q https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
    tar -xvf Python-3.6.1.tgz
    cd Python-3.6.1
    ./configure --enable-unicode=ucs4
    make
    make install
    chown -R vagrant:vagrant /home/vagrant/app

    echo "Installing python packages..."
    /usr/local/bin/pip3  install click thrift pytest pyparsing
  SHELL

end
