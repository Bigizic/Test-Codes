## When you upgrade a vps and notice there's a mismatch between the current partition and the new partition, you can run this cmd on centos


- [x] growpart /dev/vda 3

- [x] xfs_growfs /


confirm with ``fdisk -l`` and ``df -h``
