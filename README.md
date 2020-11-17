# kamailio-dev-dc

This mode is done to check loop protection mechanism based on htable
Explicitly Kamailio 4.4

```
docker-compose exec sipp bash
# sipp kamailio -s 1234 -sf sipp_reg_200.xml -r 1 -l 1 -m 10
```