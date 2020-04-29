# S+ Manager

## Setup

* Clone
* Create a virtualenv
```
python3 -m venv .venv
```
* Activate the virtualenv
```
. .venv/bin/activate
```
* Install Python dependencies
```
pip install -r requirements.txt
```
* Install NPM dependencies 
```
npm install
```
* Link the assets
```
ln -sf $PWD/node_modules apps/core/static
```
* Run migrations
```
./manage.py migrate
```
* Create the PayPal plans
```
./manage.py create_paypal_plan LA 5
./manage.py create_paypal_plan US 10
./manage.py create_paypal_plan EU 8
```
* Create webhooks
```
./manage.py subscribe_to_webhooks https://<url>/accounts/webhook/ PAYMENT.SALE.COMPLETED
```
* Run the web server
```
./manage.py run_server
```