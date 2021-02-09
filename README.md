# kamailio-dev-dc

Asterisk experiment to stop dialstring with multiple destinations

More details - https://samael28.blogspot.com/2021/02/cancel-calls-in-asterisk-dialsting.html

```
docker-compose exec sipp_uas bash
sipp asterisk -s 1234 -sf sipp_uac.xml -r 1 -l 1 -m 1
```