# Django

## Instalar postgres en ubuntu 22.04

[postgresql-quickstart-ubuntu22.04](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-22-04-quickstart)

```bash
sudo apt-get -y install gdal-bin
sudo apt-get install postgis postgresql-postgis
```

## Crear el enviroment y las dependencias del proyecto

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Crear la base de datos

```bash
sudo -u postgres psql
```

```sql
DROP DATABASE <database_name>;
CREATE DATABASE <database_name>;
ALTER USER postgres WITH PASSWORD 'root';
\q
```

## Migraciones iniciales

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## Correr el admnistrador de Django

```bash
python3 manage.py runserver
```

## Crear un super usuario

```bash
python3 manage.py createsuperuser
```

## Generar el modelo entidad relacional

```bash
sudo apt-get install graphviz
sudo apt-get install graphviz-dev
python3 manage.py graph_models <app> -o app.png
```

## Documentación de los commits

Nos gustaría tener algunos estándares de nomenclatura en las confirmaciones. Vamos a intentar tanto como podamos usar el siguiente formato al nombrar nuestras confirmaciones:

```bash
<label>: <brief explanation>

<Optional body to explain your changes in more detail>
```

A partir de ahora, las etiquetas válidas son:

* `doc` for documentation related contributions.
* `fix` if you want to fix a bug.
* `feat` if you want to add any new feature.
* `ref` if you want to refactor some parts of the existing codebase.
* `test` if the change is related to adding tests to our project.
* `mig` for to run some migration.
* `git` for work with git.

### Ejemplos

```text
feat: Add user model, serializer, view, url endpoint, filter class and admin register
test: Add tests for user
mig: Create migrations for user
git: Merge success
```

## Formatear el código

Estamos tratando de hacer que el código sea lo más estandarizado posible. Una forma de lograr esto es formateando su código correctamente. Se recomienda utilizar el formateador `black` después de haber realizado todos los cambios.

Puede formatear todo el proyecto ejecutando este comando en el directorio raíz:

```bash
make black
```

## Importaciones

El orden de las bibliotecas importadas es importante en Python. Entre otras cosas, facilita la identificación de bibliotecas de terceros para incluirlas en nuestros archivos de requisitos. Se recomienda usar `isort` para ordenar las bibliotecas correctamente. Se puede hacer ejecutando este comando en el directorio raíz:

```bash
sudo apt-get install isort
isort .
```
