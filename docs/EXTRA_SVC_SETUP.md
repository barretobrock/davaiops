# Setting up extra services
This file covers getting things like apis and other secondary services up and running

## subdomains
Create a new nginx file for the new subdomain
```bash
sudo nano /etc/nginx/sites-available/{subdomain}.davaiops.com
```
Add the following:
```nginx
server {
    listen 80;
    server_name <subdomain>.davaiops.com;
    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:<port>;
        proxy_redirect off;
    }
}
```
Symlink the file with one in `sites-enabled`
```bash
sudo ln -s /etc/nginx/sites-available/{subdomain}.davaiops.com /etc/nginx/sites-enabled/
```
If this isn't the first time you've added these subdomains, check `/etc/nginx/sites-available/default` and make sure that certbot didn't add them there. If so, you'll want to remove the references to them there, otherwise you'll get a message indicating that nginx is ignoring a conflicting server.

Test nginx
```bash
sudo nginx -t
```

```bash
sudo certbot --nginx -d davaiops.com,www.davaiops.com,viktor.davaiops.com,dizzy.davaiops.com,cah.davaiops.com,nu.davaiops.com,db-admin.davaiops.com
```

The nginx file should look something like this:
```nginx
server {
    server_name <subdomain>.davaiops.com;
    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:<port>;
        proxy_redirect off;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/... # managed by Certbot
    ssl_certificate_key /etc/...; # managed by Certbot
    include /etc/...; # managed by Certbot
    ssl_dhparam /etc/...; # managed by Certbot

}

```

Test and restart nginx
```bash
sudo nginx -t
sudo systemctl restart nginx
```