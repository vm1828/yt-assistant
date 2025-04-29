Access db inside container:  
`docker exec -it yt_assistant_db psql -U user -d yt_assistant_db`

Tables:  
`\dt`

Remove volume:

```
docker volume ls`
docker volume remove yt-assistant_db_data
# docker volume prune
```

Downgrade the db:

```
docker exec -it <container_name> bash
cd /app
poetry run alembic history
poetry run alembic downgrade -1
exit
rm alembic/versions/<migration_file>.py # in repo
```
