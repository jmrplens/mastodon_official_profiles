[WORKING]

Bienvenidx a la wiki del repositorio [mastodon_official_profiles](https://github.com/jmrplens/mastodon_official_profiles).

Aquí podrás encontrar información sobre el funcionamiento interno del repositorio, la automatización para generar los textos informativos y las tablas, etc.

## Automatización

La automatización permite actualizar los archivos `README` del repositorio utilizando los archivos `.csv` y otros archivos como `CONTRIBUTORS.yml`.

Esta automatización se realiza mediante un script escrito en Python [`main.py`](https://github.com/jmrplens/mastodon_official_profiles/blob/main/main.py) y con [GitHub Actions](https://docs.github.com/es/actions) es posible ejecutar el script en los servidores de GitHub y así mantener todo actualizado al instante cuando, por ejemplo, se acepta un Pull Request. Para ejecutar el script, este repositorio utiliza el _workflow_ [`run_python.yml`](https://github.com/jmrplens/mastodon_official_profiles/blob/main/.github/workflows/run_python.yml).

### Workflow

Lo que realiza el workflow utilizado en la automatización es:

1. Espera a cualquier cambio en el repositorio. 
2. Ejecuta un sistema Ubuntu.
3. Configura el sistema para utilizar Python.
4. Añade a la cache los paquetes instalados para reducir el tiempo de ejecución en futuras ejecuciones.
5. Instala los paquetes necesarios indicados en el archivo [`requirements.txt`](https://github.com/jmrplens/mastodon_official_profiles/blob/main/requirements.txt).
6. Ejecuta el script [`main.py`](https://github.com/jmrplens/mastodon_official_profiles/blob/main/main.py).
7. Crea el commit.
8. Escribe los cambios en el repositorio.

A continuación se muestra el código completo del workflow.

```yml
name: Generate MAIN.CSV and README

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    # Check out repository under $GITHUB_WORKSPACE, so the job can access it
    - uses: actions/checkout@v3

    # Run using Python 3.11
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
        architecture: 'x64'

    # Cache dependencies. From:
    # https://github.com/actions/cache/blob/master/examples.md#python---pip
    - uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    # Install dependencies with `pip`
    - name: Install requirements
      run: |
        python3 -m pip install --upgrade pip setuptools wheel
        python3 -m pip install -r requirements.txt

    # Run Python script
    - name: Generate data
      run: |
        python3 --version
        python3 main.py

    # Commit files
    - name: commit files
      run: |
        git config --local user.email "jmrplens@gmail.com"
        git config --local user.name "jmrplens"
        git add -A
        git diff-index --quiet HEAD || (git commit -a -m "updated logs" --allow-empty)

    # Push changes to repo
    - name: push changes
      uses: ad-m/github-push-action@master
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Archivos automatizados

### Tablas

### Colaboradorxs

La tabla de colaboradores que se muestra en los `README` se construye a partir de los datos incluidos en [`CONTRIBUTORS.yml`](https://github.com/jmrplens/mastodon_official_profiles/blob/main/CONTRIBUTORS.yml). 
Se estructura del siguiente modo:

1. `name` - Nombre
2. `avatar` - Fotografia a mostrar
3. `github_user` - Si es usuario de GitHub, al añadir su usuario se mostrará un botón para ver las aportaciones realizadas.
4. `links` - Una lista de enlaces: web, redes sociales, etc. Se debe escribir el servicio en minusculas: `web`, `mastodon`, `instagram`, etc.

Es importante mantener la tabulación, sino no se cargarán correctamente los datos. Se puede omitir cualquier dato si no se quiere incluir.

```yml
- name: Jaz-Michael King
  avatar: https://avatars.githubusercontent.com/u/3419832
  github_user: jazmichaelking
  links:
    web: https://jaz.co.uk/
    mastodon: https://toot.wales/@jaz
    linkedin: https://www.linkedin.com/in/jmking/
- name: Jorge Saturno
  avatar: https://avatars.githubusercontent.com/u/7603402
  github_user: jorgesat
  links:
    web: https://kumulonimb.us/
    mastodon: [https://red.niboe.info/@jorge,https://scholar.social/@jorge]
    orcid: https://orcid.org/0000-0002-3761-3957
- name: jmrplens
  avatar: https://avatars.githubusercontent.com/u/28966312
  github_user: jmrplens
  links:
    web: https://jmrplens.github.io/
    mastodon: https://red.niboe.info/@jmrplens
    pixelfed: https://pixelfed.social/jmrplens
    linkedin: https://www.linkedin.com/in/jmrplens
    scholar: https://scholar.google.com/citations?user=9b0kPaUAAAAJ
    work: https://www.i3m-stim.i3m.upv.es/research/ultrasound-medical-and-industrial-laboratory-umil/
- name: Lydia Gil
  avatar: https://static.mstdn.science/accounts/avatars/109/349/104/436/155/936/original/6811c637ba69ede6.jpg
  links:
    web: https://socialmediaeninvestigacion.com
    mastodon: https://mstdn.science/@TuSocialMedia
    linkedin: https://www.linkedin.com/in/lydiamargaritagil
    instagram: https://www.instagram.com/tusocialmedia/
    twitter: https://twitter.com/TuSocialMedia
    facebook: https://www.facebook.com/TuSocialMediaCiencia
```

### README's