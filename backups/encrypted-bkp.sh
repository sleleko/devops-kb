# this command will create tar.gz archive of ~/tmp directory and encrypt him, in process will ask you password for encryption 
tar -czf - ~/tmp/ | openssl enc -e -aes256 -out ~/tmpdir_`date +%d-%m-%Y_%H-%M`_enc.tar.gz

#on finish you got file tmpdir_20-05-2019_10-00_enc.tar.gz for example

# this command will extract your encrypted tar.gz archive, before extract process, you need enter password of archive
openssl enc -d -aes256 -in ~/tmpdir_DD-MM-YYYY_HH-MM_enc.tar.gz | tar xz -C /dir-that-you-need

#where DD-MM-YYYY_HH-MM is date and time in archive name
