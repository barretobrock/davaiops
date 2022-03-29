# Setup

## Server
NB! This assumes a freshly-created Ubuntu server
### Update packages
```bash
sudo apt update && sudo apt upgrade
```
### Non-root user creation
```bash
MYUSER=username_here
adduser ${MYUSER}
usermod -aG sudo ${MYUSER}
```
### Firewall setup
```bash
ufw allow OpenSSH
ufw enable
ufw status
```
### Enable non-root user access
```bash
rsync --archive --chown=${MYUSER}:${MYUSER} ~/.ssh /home/${MYUSER}
```
Open up a new terminal window, try to log in as non-root user.
Close root session upon successful log in.

Make some new directories on the non-root user's home & set the timezone
```bash
mkdir keys logs venvs extras data
sudo timedatectl set-timezone America/Chicago
# Reconfigure dash to bash
sudo dpkg-reconfigure dash  # select 'No' to default to bash
```

## fail2ban
Follow the guide in sources, then make the following changes:
 - ignore-ips
 - ban timing, duration 
 - Install mailutils to resolve a potential issue with sendmail
   - `sudo apt install mailutils`
   - Select 'local only'
   - enter domain name

### Add slack message option
Next, add slack message to action (see link in sources)

First, copy contents in the link provided to a new file
```bash
sudo nano /etc/fail2ban/action.d/slack-notify.conf
```
Then, make changes in the local jail
```bash
sudo nano /etc/fail2ban/jail.local
```
Restart the service
```bash
sudo systemctl restart fail2ban
```

### Add invalid webpage blocking 
Next we'll add in a filter for repeat invalid page requests. This will use nginx's access.log

First, make a new file to hold the regex patterns and other settings
```bash
sudo nano /etc/fail2ban/filter.d/nginx-4xx.conf
```
Add the following:
```unit file (systemd)
[Definition]
failregex = ^<HOST>.*"(GET|POST).*" (4\d{2}) .*$
ignoreregex = 
```
Then open the jail.local
```bash
sudo nano /etc/fail2ban/jail.local
```
Add the following:
```unit file (systemd)
[nginx-4xx]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 3
```
Restart fail2ban
```bash
sudo systemctl restart fail2ban
```

### Add postgres port blocking
Edit postgres settings to include host in log output
```bash
sudo nano /etc/postgresql/12/main/postgresql.conf
```
Make log_line_prefix look like this:
```editorconfig
log_line_prefix = '%h %m [%p] %q%u@%d '
```
Restart postgres
```bash
sudo systemctl restart postgresql
```

Create a filter for postgres
```bash
sudo nano /etc/fail2ban/filter.d/custom-postgres.conf
```
Populate with this:
```unit file (systemd)
[Definition]
failregex = ^<HOST>.+FATAL:.+password authentication failed for user.+$
            ^<HOST>.+FATAL:.+no pg_hba.conf entry for host.+$
ignoreregex = 
```
Then open the jail.local
```bash
sudo nano /etc/fail2ban/jail.local
```
Add the following:
```unit file (systemd)
[custom-postgres]
enabled = true
port = 5432
logpath = /var/log/postgresql/postgresql-12-main.log
maxretry = 3
```
Restart fail2ban
```bash
sudo systemctl restart fail2ban
```

## nginx / gunicorn / certbot
### Install nginx
```bash
sudo apt install nginx
```
### Firewall adjustment
```bash
sudo ufw allow 'Nginx HTTP'
# Make sure service is running before testing site
sudo systemctl status nginx.service
```
Go to `http://{your-ip}` to confirm that your site is up
### Server block setup
This is used to encapsulate configuration details and host more than one domain from a single server
```bash
# Create directory and set ownership/permissions
sudo mkdir -p /var/www/davaiops.com/html
sudo chown -R ${USER}:${USER} /var/www/davaiops.com/html
sudo chmod -R 755 /var/www/davaiops.com
# Create sample index.html file
nano /var/www/davaiops.com/html/index.html
```
Copy/paste this in that file 
```html
<html>
    <head>
        <title>Welcome to davaiops.com!</title>
    </head>
    <body>
        <h1>Success!  The davaiops.com server block is working!</h1>
    </body>
</html>
```
Then let's make a new configuration file for nginx (instead of adjusting the `default`)
```bash
sudo nano /etc/nginx/sites-available/davaiops.com
```
Copy/paste this into that file
```
server {
   listen 80;
   listen [::]:80;
   
   server_name davaiops.com www.davaiops.com;

   location / {
      proxy_set_header Host $host;
      proxy_pass http://127.0.0.1:<port>;
      proxy_redirect off;   
   }
}
```
Then enable the file by creating a link from it to the `sites-enabled` directory
```bash
sudo ln -s /etc/nginx/sites-available/davaiops.com /etc/nginx/sites-enabled/
```
Correct for possible hash bucket memory problem (idk, seems like something worth avoiding)
```bash
sudo nano /etc/nginx/nginx.conf
```
Uncomment the line that has `server_names_hash_bucket_size`, save and close.
Then test nginx configs and, if succeeded, restart the service.
```bash
sudo nginx -t
sudo systemctl restart nginx
```
### python venv setup
```bash
sudo apt install python3-pip python3-dev python3-venv build-essential libssl-dev libffi-dev python3-setuptools 
# Setup venv and source into it
(cd ~/venvs && python3 -m venv davaiops) && source ~/venvs/davaiops/bin/activate
# Install necessary packages
python3 -m pip install wheel flask gunicorn
```

Install the py-package-manager library
```bash
cd ~/extras && git clone https://github.com/barretobrock/py-package-manager.git
```

Clone the git repo, Create a sample app
```bash
cd ~/extras && git clone https://github.com/barretobrock/davaiops.git
cd davaiops
source ~/venvs/davaiops/bin/activate
```

Allow access to port 5000
```bash
sudo ufw allow 5000
```
Check that the site shows this. Run `run_debug.py` and then go to `http://{ip_address}:5000`

### Gunicorn setup
Check that gunicorn can serve the application correctly
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```
Once that's running, the site again. Go to `http://{ip_address}:5000`

After that, `deactivate` the python env

Create the gunicorn service file
```bash
sudo nano /etc/systemd/system/davaiops.service
```
Add the details from davaiops.service file

Then, add the SECRETKEY and REGISTRATIONKEY to the directories


Start the service & enable it
```bash
sudo systemctl start davaiops
sudo systemctl enable davaiops
```
### Configure proxy requests

Remove port 5000 access since we don't need it
```bash
sudo ufw delete allow 5000
sudo ufw allow 'Nginx Full'
```
### Secure site with certbot
Install certbot & setup the nginx plugin of certbot's SSL configuration
```bash
sudo apt install python3-certbot-nginx
sudo certbot --nginx -d davaiops.com -d www.davaiops.com -d viktor.davaiops.com -d dizzy.davaiops.com -d cah.davaiops.com -d nu.davaiops.com -d db-admin.davaiops.com
```
Remove redundant HTTP profile
```bash
sudo ufw delete allow 'Nginx HTTP'
```
The domain should now load properly when you go to `https://davaiops.com`

## postgres
Follow the guide in sources, then the stuff below:
### Install dependencies for port scanning
```bash
sudo apt install net-tools
```
### Open the port for remote access
First check if it's listening on a public port
```bash
netstat -nlp | grep 5432
```
Then edit `postgresql.conf`
 - change `listen_addresses` to '*'
```bash
sudo nano /etc/postgresql/12/main/postgresql.conf
# Restart with:
sudo systemctl restart postgresql
```
Then edit `pg_hba.conf`
 - add the text to the bottom
```bash
sudo nano /etc/postgresql/12/main/pg_hba.conf
```
```editorconfig
# This is the setup to allow all connections - generally best not to do for a remote server
#host    all             all              0.0.0.0/0                       md5
#host    all             all              ::/0                            md5
host    all             {USER}          {client_ip}/32                  md5
```
Then restart again
```bash
sudo systemctl restart postgresql
```
Then open the port in ufw
```bash
sudo ufw allow 5432/tcp
```
### Update psql users w/ passwords and test remote access
Switch to postgres user, enter Postgres
```bash
sudo -i -u postgres
psql
```
Then begin adding passwords:
```postgresql
alter user {uname} with password '{secret}';
```

### Configure allowed hosts
Update `pg_hba.conf` to set up a list of allowed connection details
```bash
sudo nano /etc/postgresql/12/main/pg_hba.conf
```
Add in something like this:
```
host  {database}     {user}   {client_ip_address}/32     md5
```
Then set the listening addresses
```bash
sudo nano /etc/postgresql/12/main/postgresql.conf
```
Make sure the __server__ ip is included with localhost:
```
listen_addresses = 'localhost,{server_ip_address}'
```
Restart the service
```bash
sudo systemctl restart postgresql
```

### Notes
 - For the `psycopg2` python package, it might be required to `sudo apt install libpq-dev`
 - Test regex applied to fail2ban with something like the following:
   - `sudo fail2ban-regex {LOG_PATH} "{REGEX}"` OR `sudo fail2ban-regex {LOG_PATH} {PATH_TO_FILTER.D/CONF_FILE}`
   - OR, you can write the example log items to a temp file, pass that 

## Logs
 - postgres
   - /var/log/postgresql/postgresql-12-main.log
 - nginx
   - /var/log/nginx/{access,error}.log
 - sshd
   - /var/log/auth.d

## Sources
 - fail2ban
   - https://linuxize.com/post/install-configure-fail2ban-on-ubuntu-20-04/
   - https://github.com/mikey32230/fail2ban-slack-action
   - https://arvind.io/posts/using-fail2ban-to-protect-exposed-services/
   - https://www.ericlight.com/fail2bannginx-blocking-repeated-404s-etc.html
   - https://talk.plesk.com/threads/howto-secure-a-standard-postgres-port-with-fail2ban.355984/
   - https://www.the-art-of-web.com/system/fail2ban-filters/
 - postgres
   - https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04
   - http://www.project-open.com/en/howto-postgresql-port-secure-remote-access
   - https://stackoverflow.com/questions/17838613/open-port-in-ubuntu
   - https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-against-automated-attacks
   
## Troubleshooting 
 - failure on `update_script` with `x86_64-linux-gnu-gcc`
   - `sudo apt install libpq-dev`