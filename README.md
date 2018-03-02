# expanding-redirector
Webservice for dynamic redirecting for monitoring

## Purpose

* To avoid cache hits we want to send unique queries to a monitored service
* We wish to add a irrelevant field (http://....?...&irrelevant=TIMESTAMP)
* Monitor service does not support this
* Solution is to redirect to actual service
* Query `http://service/actual.service:port/path/endpoint?argument=something&irrelevant=%(NOW)%`
* Redirects to `http://actual.service:port/path/endpoint?argument=something&irrelevant=1234567890987`
