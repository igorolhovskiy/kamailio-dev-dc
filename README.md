# kamailio-dev-dc

Replicating insocistency in URI forming

## Start and monitor
```
> docker compose up -d
> docker compose exec kamailio bash
# sngrep
```
## Start test
```
sipp -r 1 -m 1 -sf uac_1.xml -s 11111 localhost
```
