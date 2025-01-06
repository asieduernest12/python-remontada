#!/bin/sh

# # fastapi_app test 
curl -X POST "http://${scheme:-fastapi}.localhost/todos/" -H "Content-Type: application/json" -d '{"title": "item${last_id:-1}", "description": "description1"}' -o /dev/null -w "%{http_code}\n" -s
curl -X GET "http://${scheme}.localhost/todos/"  -w "%{http_code}\n" 
curl -X GET "http://${scheme}.localhost/todos/1" -o /dev/null -w "%{http_code}\n" -s
# Get all todos and extract the id of the last entry

last_id=$(curl -s "http://${scheme}.localhost/todos/" | jq -r '.[-1].id')

# Use the extracted id for further operations
curl -X GET "http://${scheme}.localhost/todos/$last_id" -o /dev/null -w "%{http_code}\n" -s
# curl -X PUT "http://${scheme}.localhost/todos/$last_id" -H "Content-Type: application/json" -d '{"title": "item1_updated", "description": "description1_updated"}' -o /dev/null -w "%{http_code}\n" -s
# curl -X DELETE "http://${scheme}.localhost/todos/$last_id" -w " %{http_code} \n" -s
  