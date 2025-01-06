.ONESHELL:
.SILENT:
.SHELL:=/bin/bash

# Color codes
COLOR_RESET=\033[0m
COLOR_GREEN=\033[32m


# Print helper
print:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(COLOR_GREEN)%-30s$(COLOR_RESET) %s\n", $$1, $$2}' | sed -e 's/\$$(COLOR_GREEN)/\033[32m/g' -e 's/\$$(COLOR_RESET)/\033[0m/g'



seed_domain: ## generate seeders
	# # fastapi_app test 
	curl -X POST "http://${domain:=fastapi}.localhost/todos/" -H "Content-Type: application/json" -d '{"title": "item${last_id:-1}", "description": "description1"}' -o /dev/null -w "%{http_code}\n" -s
	curl -X GET "http://${domain}.localhost/todos/"  -w "%{http_code}\n" 

	# create a new todo with title as title-count description: description-count, where count is the number of items returned by /todos/
	count=$(curl -s "http://${domain}.localhost/todos/" | jq '. | length')
	echo "count: $count"
	curl -X POST "http://${domain}.localhost/todos/" -H "Content-Type: application/json" -d "{\"title\": \"title-${count}\", \"description\": \"description-${count}\"}" -o /dev/null -w "%{http_code}\n" -s

seed: ## seed all domains
	# set seed_max to 10 , use seq and xargs to run the seed_domain command
	domains="fastapi\n flask\n django";
	echo -e "$$domains" | xargs -I{} bash -c 'seq $${see_max:=10} | xargs -Ixx bash -c "$(MAKE) seed_domain domain={} last_id=xx"'
	

delete_domain: ## delete all todos in a domain
	seq $${deletions:=1} | xargs -Ixx bash -c 'curl -X DELETE "http://${domain}.localhost/todos/" -w "%{http_code}\n" -s'



domain_count:
	count=$(curl -s "http://$${domain}.localhost/todos/" | jq '. | length'); \
	echo "$${domain} has $${count} todos"
	