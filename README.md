# kamailio-dev-dc

Docker-compose file for developig for Kamailio and Asterisk as a backend helper


## Dispatcher add
```
# docker-compose exec kamailio bash
> kamcmd
>> dispatcher.add 1 sip:asterisk_2:5060
```