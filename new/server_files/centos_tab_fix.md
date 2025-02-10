### In case of when tab button not completing commands on centos system


- [x] install bash completion
```bash
sudo dnf install bash-completion -y
```

- [x] enable bash completion
```bash
source /usr/share/bash-completion/bash_completion
```

- [x] add line `source /usr/share/bash-completion/bash_completion` to end of .bashrc file
```bash
echo 'source /usr/share/bash-completion/bash_completion' >> ~/.bashrc
```


- [x] reload .bashrc file
```bash
source ~/.bashrc
```

- [x] reboot system
```bash
reboot
```
