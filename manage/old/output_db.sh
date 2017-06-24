#!/bin/sh


DB='echo \"select * from sm25\" | mysql -u web -p sif_event -X > /var/www/sif/db.xml'

expect -c "
spawn \"echo 'select * from sm25'\" | mysql -u web -p sif_event -X > /var/www/sif/db.xml
expect \"Enter password:\"
send \"password\n\"
"

