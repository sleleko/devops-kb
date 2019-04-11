# zfs create mount point
zfs create -o mountpoint=/srv /rpool/srv

# zfs create new volume src, it will create new volume in path /srv/src
zfs create rpool/srv/src

# if you need delete volume
zfs destoy rpool/srv/src

#if your volume has sub volumes, delete it recursive
zfs destory -r rpool/srv/src
