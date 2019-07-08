# reduce /dev/TMP-VM/home from 50GB to 5GB and expand /dev/TMP-VM/var from 5GB to 50GB

# first step umount /home
umount /home

#NOTE: if you have a message about /home is busy, please check any users or services who can work in this moment with this directory, and close them

# Now you can check file system for errors and reduce /home volume
e2fsck -f /dev/mapper/vg_tmp-vm-lv_home
resize2fs /dev/mapper/vg_tmp-vm-lv_home 5G

# After that you can reduce LVM volume to 5G
lvreduce -L 5G /dev/mapper/vg_tmp-vm-lv_home

# Now you can extend LVM Volume of /var for all free space
lvextend -l +100%FREE /dev/mapper/vg_tmp-vm-lv_var

#and extend file system 
resize2fs /dev/mapper/vg_tmp-vm-lv_var

# finish step mount home
mount /home
