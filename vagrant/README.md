### How to install vagrant on windows

    mkdir virtualMachine
    cd virutalMachines
    mkdir ubuntu17
    cd ubuntu17
    vagrant box add ubuntu/xenial64
    vagrant init ubuntu/xenial64
    vagrant plugin install vagrant-vbguest
    vagrant up
    vagrant ssh
    
    
    use exit to close vagrant
    
    anytime you want to login on cmd u use vagrant up and vagrant ssh afterwards
    

