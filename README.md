# kamailio-dev-dc

This mode is about to emulate sending from Kamailio INVITE-CANCEL sequence after getting REGISTER with TCP connection.
Explicitly Kamailio 4.4

```
docker-compose exec sipp bash
# sipp kamailio -s 1234 -sf sipp_reg_invite_cancel.xml -r 1 -l 1 -m 1 -t t1
```