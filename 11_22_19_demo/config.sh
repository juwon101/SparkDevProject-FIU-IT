#modules for python

yum install -y python-pip
yum install -y python-dateutil

pip install pymongo
pip install flask

# syslog-ng

yum install -y epel-release
yum install -y syslog-ng
setenforce 0

mkdir /syslog
touch /syslog/sparkdev

cat <<EOF > /etc/syslog-ng/conf.d/sparkdev.conf
source s_sd              { udp(ip(0.0.0.0) port(514)); };
destination d_sd     { file("/syslog/sparkdev"); };
destination d_sd_gold           { file("/syslog/gold");};
destination d_sd_blue           { file("/syslog/blue"); };
filter f_sd_gold                { match("GOLD") };
filter f_sd_blue                { match("BLUE"); };
log             { source(s_sd); filter(f_sd_gold); destination(d_sd_gold); flags(final); };
log             { source(s_sd); filter(f_sd_blue); destination(d_sd_blue); flags(final); };
log             { source(s_sd); destination(d_sd); };
EOF

# mongodb

cat <<EOF > /etc/yum.repos.d/mongodb-org-4.2.repo
[mongodb-org-4.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/4.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc
EOF

yum install -y mongodb-org


# certbot

yum install -y certbot



# start services
systemctl start syslog-ng
systemctl start mongod


# start collecting data
python data.py > /dev/null &

# push to mongodb
python pushToMongoDB.py > /dev/null  &

python server.py > /dev/null  &

# The command below will be used to get the cert from letsencrypt
#certbot certonly --webroot -w /home/carau017/ -d $1

#sed -i "s/DOMAIN/$1/g" serverwithDB.py

#python serverwithDB.py > /dev/null  &
