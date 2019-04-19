# zfs create mount point
zfs create -o mountpoint=/srv /rpool/srv

# zfs create new volume src, it will create new volume in path /srv/src
zfs create rpool/srv/src

# if you need delete volume
zfs destoy rpool/srv/src

#if your volume has sub volumes, delete it recursive
zfs destory -r rpool/srv/src

# create new snapshot of volume
zfs snapshot rpool/srv/src@any-text-or-int-for-identification-snapshot

# create new snapshot of volume and sub volumes (recursive)
zfs snapshot rpool/srv/src@any-text-or-int-for-identification-snapshot -r

# move zfs sub volumes from one parent volume to other, with all him snapsjots if its exist
zfs rename rpool/srv/db/subvolume rpool/srv/old/db/subvolume

# send volume from one node to two node via ssh. Note: this command runing on target node and with "pv" utility
# for display progress bar of operation
ssh sourcenode zfs send -v rpool/srv/db/somevolume | pv | zfs recv -Fv rpool/srv/db/somevolume 
