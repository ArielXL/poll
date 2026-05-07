.PHONY: info

NAME 	   	:= Django
VERSION		:= 1.0
DEVELOPERS	:= Ariel Plasencia
COPYRIGHT  	:= Grupo AOV © 2026: $(DEVELOPERS)

run: ## Run the backend
	python3 manage.py runserver

makemigration: ## Update migrations
	python3 manage.py makemigrations

migrate: ## Ensure database
	python3 manage.py migrate

migrations: ## Run the migrations
	python3 manage.py makemigrations
	python3 manage.py migrate

create_super_user: ## Create super user
	python3 manage.py createsuperuser

info: ## Display project description
	@echo "$(NAME) v$(VERSION)"
	@echo "$(COPYRIGHT)"

version: ## Show the project version
	@echo "$(NAME) v$(VERSION)"

install: ## Install dependencies
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install -r requirements.txt

activate_enviroment: ## Activate the enviroment
	source .venv/bin/activate

clean: ## Remove temporary files
	echo "cleaning"

black: ## Format all python code
	black .

isort: ## Sort libraries properly
	isort .

mer: ## Make the model entity relational
	python3 manage.py graph_models -a -o mer.png

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'