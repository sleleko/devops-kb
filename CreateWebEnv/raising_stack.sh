# This is example of raising nginx+php7.4+mysql8 on Rhel8 or Centos

yum install mysql

# if mysqld service was not enabled by default
systemctl enable mysqld.service

# securting mysql
mysql_secure_installation

# log in into mysql with your new root cridentials
mysql -u root -pYourpassword

# into mysql you must create your Users and databases, when grant priv
***
# quit mysql

# installing nginx
yum install @nginx

# if you want, you can check status of nginx service
service nginx status

# enable firiwall rule for http (or https)
firewall-cmd --zone=public --permanent --add-service=http
firewall-cmd --reload

# install epel-release repos for php7.4 next I,l use dnf for install
dnf install epel-release -y
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm -y
dnf install https://rpms.remirepo.net/enterprise/remi-release-8.rpm -y
dnf -y install dnf-utils -y
dnf module install php:remi-7.4 -y
php --version
dnf update -y

# install php modules
dnf install php-{mysqlnd,curl,gd,intl,pear,recode,xmlrpc,mbstring,gettext,gmp,json,xml,fpm} -y


