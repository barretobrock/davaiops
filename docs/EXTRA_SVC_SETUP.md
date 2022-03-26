# Setting up extra services
This file covers getting things like apis and other secondary services up and running

## subdomains
Open up the nginx file
```bash
sudo nano /etc/nginx/sites-available/davaiops.com
```
Add the following below the existing code
```nginx
server {
    listen 80;
    server_name viktor.davaiops.com;
    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:<port>;
        proxy_redirect off;
    }
}
server {
    listen 80;
    server_name cah.davaiops.com;
    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:<port>;
        proxy_redirect off;
    }
}
server {
    listen 80;
    server_name dizzy.davaiops.com;
    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:<port>;
        proxy_redirect off;
    }
}
server {
    listen 80;
    server_name nu.davaiops.com;
    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:<port>;
        proxy_redirect off;
    }
}
server {
    listen 80;
    server_name db-admin.davaiops.com;
    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:<port>;
        proxy_redirect off;
    }
}
```
```bash
sudo certbot --nginx -d davaiops.com -d www.davaiops.com -d viktor.davaiops.com -d dizzy.davaiops.com -d cah.davaiops.com -d nu.davaiops.com -d db-admin.davaiops.com
```
Test and restart nginx
```bash
sudo nginx -t
sudo systemctl restart nginx
```