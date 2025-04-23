Access db inside container:  
`docker exec -it yt_assistant_db psql -U user -d yt_assistant_db`

Tables:  
`\dt`

Remove volume:
`docker volume ls`
`docker volume remove yt-assistant_db_data`