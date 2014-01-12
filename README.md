Practica3IV
===========

José Miguel Colella
-------------------

#Comparaciones


Se van a ser 6 diferentes comparaciones, entre los cuales 4 serán
comparaciones entre servicios IaaS, a las últimas dos comparaciones
se haran comparando las configuraciones de máquinas creadas con VirtualBox
y Vagrant.

1. Los IaaS (Infrastructure as a Service) que se van a emplear para
comparar son AWS y Azure.

* Comparaciones

- La primera comparación que se hará es la construcción de un sistema mínimo que
tendrá el sistema operativo Ubuntu 12.04 LTS para el despliegue de una aplicación
en python que requiere acceso

- La segunda comparación que se hará es la entre el sistemas operativo Red Hat Enterprise
Linux 6.4 (64 bit) que se usará en AWS, y CentOS en Azure.


2. Para las últimas configuraciones se usará Vagrant. Vagrant usa herramientas de automatización como Chef para proporcionar
un entorno de desarrollo en poco tiempo. La configuración de la máquina a crear
se declara en un `Vagrantfile`. Todas las configuraciones se declaran en Ruby.

Esta comprobación se hará teniendo una máquina con Ubuntu 12.04 mientras la segunda
máquina usará Ubuntu 13.10. Esta comparación determinará si usar un sistema
operativo más reciente mejora el rendimiento de la máquina.

* Comprobar el rendimiento de servidores web
Se comprobará el rendimiento entre las máquinas usando dos benchmarks; ab y httperf

Para concluir denoto las comparaciones con una tabla

| Num.     | Comparación |
| ------------- |:-------------:|
| 1  | azure ubuntu 12.04 (64 bit) vs aws ubuntu 12.04 (64 bit)|
| 2   | azure CentOS 6.4 (64 bit) vs aws Red hat Linux 6.4 (64 bit)|
| 3   | vagrant ubuntu 12.04 (64 bit) vs vagrant ubuntu 13.10 (64 bit) |

Con las primeras dos comparaciones quiero comparar el hardware y los hipervisores
que usan los dos para crear las máquinas. Con la tercera comparación quiero comparar
el efecto de un sistema operativo mas reciente en comparación con un sistema operativo
más antiguo sobre las prestaciones de la aplicación.

Aplicación a montar
===================

La aplicación que voy a montar y desplegar en todas las máquinas creadas para
esta práctica es una aplicación que usa MongoDB como bases de datos para registrar
información de nuevos usuarios, proporciona geolocalización de tweet usando la API
de Google Maps, y además usa las API de Google Charts. Dicha aplicación
ha sido construida con el micro-framework [web.py][1].

##Despligue de la aplicación en las máquinas creadas
Cuando se crean las maquinas, se descarga git para poder obtener
un script que automatizará todo relacionado con los paquetes
de dependencia, descarga el código fuente de la aplicación, y
abre el puerto 80 para servir dicha aplicación.

El script que uso para automatizar el proceso de despliegue esta alojado
en https://gist.github.com/josecolella/8352996. Los gists son pequeñas lineas
de código, que denotan scripts de automatización, configuración, etc...que se almacenan
para ser clonado por otros usuarios o el mismo usuario.

El script, después de ser descargado en la máquina se ejecuta usando

```sh
source automate.sh
```

Se usa *source* ya que cuando se ejecuta un script, un nuevo proceso se lanza y
cuando se cambia de directorio solo se cambia en el proceso.

El script descarga los paquetes esenciales para ejecutar la aplicación. Además he tomado
ventaja de que el framework web.py emplea un CGI y no he descargado apache, para hacer
una instalación minimalista.

A continuación podemos ver los pasos seguidos en el script.

```bash
#!/bin/bash
# Author: Jose Miguel Colella
# Description: Script creado para automatizar el proceso
# de instalar todo
cd ../

sudo apt-get update
sudo apt-get install -y language-pack-en
sudo apt-get install -y build-essential
sudo apt-get install -y python-dev
sudo apt-get install -y python-setuptools

# Instalar web.py
sudo easy_install web.py
#Instalar lenguaje de templating
sudo easy_install mako
#Instalar driver para mongodb-server
sudo easy_install pymongo
#Instalar interfaz de twitter
sudo easy_install tweepy
# Instalar el feedparser
sudo easy_install feedparser

git clone https://github.com/josecolella/DAI_Practica4.git
cd DAI_Practica4
chmod +x index.py
# Para que el script siga ejecutando despues de que salga de ssh
sudo nohup ./index.py 80 &
```

El comando nohup se usa para que cuando me desconecte con la instancia siga
ejecutandose el script

##Bases de Datos
Con gestionar las bases de datos, lo tradicional hubiera sido descargarse
en todas las máquinas creadas el paquete demonio de MongoDB. Este enfoque
no es moderno y es monotono. Hoy en día con la Nube hay servicios que denoto
como Database-as-a-Service que proporcionan la infraestructura con el gestor
de bases de datos a los desarrolladores. [MongoLab][2] proporciona un database-
as-a-Service para desarrolladores gratis pero limitado. Proporcionan 500 MB de
espacio.

Ya creada una cuenta se tiene que crear un usuario para poder acceder a las
bases de datos desde la aplicación

!["Usuario"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/mongodbPhotos/Screen%20Shot%202014-01-10%20at%2010.22.10.png)

Se tiene que ver que el usuario ha sido creado como en la siguiente imagen.

!["Usuario creado"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/mongodbPhotos/Screen%20Shot%202014-01-10%20at%2010.43.29.png)

`mongodump` para exportar las bases de datos en local e importarlas en mongolab
con el comando `mongorestore`

En local hay que ejecutar el comando:

```sh
mongodump
```

para obtener una representación en json y bson de las bases de datos para que
se puedan importar en las bases de datos de MongoLab.

Los comandos para importar las bases de datos y collecciones del Mongo

```sh
mongorestore -h ds063158.mongolab.com:63158 -d dai_db -u <user> -p <password> <input db directory>
mongorestore -h ds063158.mongolab.com:63158 -d dai_db -u <user> -p <password> <input .bson file>
```

Ya restauradas las bases de datos tiene que tener las collecciones que se han agregado

!["Cosas agregadas"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/mongodbPhotos/Screen%20Shot%202014-01-10%20at%2010.43.29.png)

Para poder usarlo hay que registrarse e identificar el servicio de alojamiento
que se usará para dicha base de datos. Yo he optado por alojamiento de Amazon Web
Services.

Además hay que crear un usuario para poder acceder a las bases de datos.
Finalmente se tiene que reflejar este cambio de conexión a bases de datos
en el código.

Por ejemplo con el modulo pymongo que se usa para conectarse con MongoDB desde
python, el cambio se refleja agregando información sobre la ruta hacia el servicio,
con el puerto. Adicionalmente, hay un paso de autentificación que se tiene que denotar
en el código para poder usar las bases de datos de MongoLab

En el siguiente código se puede ver lo que hay que cambiar para poder
interactuar con las bases de datos de MongoLab. No se ha puesto la información
verdadera por razones de serguridad.

```python
from pymongo import MongoClient

connection = MongoClient('dsXXXX.mongolab.com', 63158)
db = connection['dai_db']
db.authenticate('user','password')
```

Este servicio proporcionará una ayuda al momento de desplegar la aplicación
en las diversas máquinas. Las bases estarán intactas y ya creadas se usarán por
todas las máquinas. Aquí vemos otra instancia de los beneficios que aporta la nube.

Azure
=====

Para la construcción de las máquinas virtuales en Azure he optado por crearlas con
la interfaz gráfica ya que hay muchas opciones que se pueden seleccionar al tiempo
de crearlas y con la interfaz gráfica se pueden ver estas opciónes más facilmente.

Para hacer la comparación entre AWS y Azure he tenido que construir las máquinas virtuales
más basicas que ofrecen los dos.


|  Proveedor    | CPU       | RAM (MB)   | Rendimiento de Red
| ------------- |:-------------:|:-------------:|
| AWS  | 1 | 615  | Muy baja
| Azure   | 1 (Compartida)    |   768  |

La información de Amazon Web Services se ha obtenido de [aquí][3] mientras
que la información de Azure se ha obtenido de [aquí][4].

Primero hay que configurar la máquina para el despliegue de la aplicación.
Los paquetes esenciales para esto son:

Los siguientes paquetes son necesarios para obtener el código fuente
de la aplicación

|  Paquetes    | Utilidad |
| ------------- |:-------------:|
| git  | Sistema de control de versiones |
| python-dev   | paquete para desarrollar con python |
| build-essential   | paquete que contiene todos los paquetes para desarrollar |

Los siguientes modulos se requieren para ejecutar la aplicación

|  Modulos de Python    | Utilidad |
| ------------- |:-------------:|
| feedparser  | Modulo para trabajar con rss y xml |
| tweepy   | API para trabajar con Twitter |
| web.py   | Micro-Framework para Python |
| mako   | Lenguaje de Template para Python |
| pymongo   | Driver de Python para MongoDB |

###Ubuntu 12.04

Usando la interfaz web, he creado la máquina virtual. Para poder a dicha máquina desde el puerto 80, y para
que pueda conectarse con las bases de datos de MongoLab hay que indicarle a azure que dichos puertos
tienen que estar abiertos.

En la siguiente imagen se puede ver la especificación de dichas reglas.

![""](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/azure2Photos/Screen%20Shot%202014-01-11%20at%2019.05.19.png)

Ahora hay que conectarse mediante ssh para poder desplegar la aplicación.
Después hay que descargarse git para poder automatizar el proceso de despligue:

```bash
sudo apt-get install -y git
```

Cuando se descarga el script mediante git clone, se tiene que ejecutar.
A continuación se puede ver los comandos a seguir.

```bash
git clone https://gist.github.com/8374477.git Automate
cd Automate/
chmod +x automate.sh
source automate.sh
```

En la siguiente imagen se puede ver que la aplicación ha sido desplegada correctamente.

![""](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/azure1Photos/Screen%20Shot%202014-01-11%20at%2022.33.44.png)

En la siguiente imagen se puede ver que se ha autentificado con exito, y esto significa que se ha hecho una conexión con las bases de
datos en MongoLab.

![""](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/azure1Photos/Screen%20Shot%202014-01-11%20at%2022.33.46.png)

El dns de la aplicación es http://ivmachine.cloudapp.net/



###CentOS 6.3

Para crear la máquina he seguido el mismo procedimiento pero hay que escoger OpenLogic
como sistema operativo en vez que Ubuntu.

Accediendo mediante ssh como se puede ver en la siguiente imagen

![""](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/azure2Photos/Screen%20Shot%202014-01-12%20at%2000.46.18.png)

se ejecutan los siguintes comandos:

```bash
sudo yum update
sudo yum groupinstall -y "Development tools"

# Instalar web.py
sudo easy_install web.py
#Instalar lenguaje de templating
sudo easy_install mako
#Instalar driver para mongodb-server
sudo easy_install pymongo
#Instalar interfaz de twitter
sudo easy_install tweepy
# Instalar el feedparser
sudo easy_install feedparser

git clone https://github.com/josecolella/DAI_Practica4.git
cd DAI_Practica4
chmod +x index.py
# Para que el script siga ejecutando despues de que salga de ssh
sudo nohup ./index.py 80 &
```

En la siguiente imagen se puede ver que se ha desplegado correctamente la aplicación

![""](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/azure2Photos/Screen%20Shot%202014-01-12%20at%2000.57.42.png)

El dns del sitio es http://ivmachine2.cloudapp.net/

AWS
====

Amazon Web Services proporciona la habilidad de crear y configurar máquinas
virtuales de manera bien facil.

Yo he optado por crear la máquina virtual con la interfaz gráfica ya que hay
muchas opciones que considerar. La cuenta que ofrecen AWS a los usuarios de no pago
solo proporciona la habilidad de crear una micro-instancia.

!["Micro Instancia"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/aws1photos/tiMicro.png)

Cuando se crea la máquina virtual hay que crear un certificado .pem para poder
acceder a el desde manera remota. También hay que configurar los grupos de seguridad
que habilitan el acceso al puerto 80 desde afuera, así se puede visualizar la
applicación que esta almacenada dentro de dicha máquina. El los grupos de seguridad
hay que especificar que se tiene que abrir el puerto a donde se conectará a las bases
de datos de MongoLab. En mi caso es por el puerto 63158. En los grupos de seguridad
se expresa con una "Custom Rule" de tipo de conexión TCP.

!["Grupo de seguridad"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/aws1photos/SecurityGroup.png)

Para poder acceder a AWS necesitas el certificado .pem que se proporciona al momento
de crear una instancia EC2.

La primera máquina que he creado es un servidor que tiene la distribución Ubuntu Server
12.03 LTS. El servidor se ha creado en Irelanda

```sh
ssh -i josecolella.pem ubuntu@54.194.187.157
```

Ya dentro se ha descargado git para poder obtener el script de automatización
se ha ejecutado dicho script con:

```bash
source automate.sh
```

En la siguiente imagen se puede ver que se ha desplegado la aplicación correctamente

![""](https://github.com/josecolella/Practica3IV/blob/master/Screenshots/aws1photos/Screen%20Shot%202014-01-11%20at%2022.37.38.png)

Además que si me autentifico en el formulario de entrada, entra a la cuenta que había
creado. Esto significa que la conexión con las bases de datos alojadas en MongoLab se
ha hecho bien.

La url de la primera máquina montada es http://ec2-54-194-187-157.eu-west-1.compute.amazonaws.com/

#####Red Hat Enterprise Linux

Para la segunda máquina se ha seguido el mismo procedimiento, excepto que se ha escojido el sistema operativo
Red Hat Linux.

![""](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/aws2Photos/Screen%20Shot%202014-01-12%20at%2000.08.50.png)

En la siguiente imagen se puede comprobar la distribución:

![""](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/aws2Photos/Screen%20Shot%202014-01-12%20at%2000.12.41.png)

Para poder desplegar la aplicación he usado los siguientes comandos:

```bash
sudo yum update
sudo yum groupinstall -y "Development tools"

# Instalar web.py
sudo easy_install web.py
#Instalar lenguaje de templating
sudo easy_install mako
#Instalar driver para mongodb-server
sudo easy_install pymongo
#Instalar interfaz de twitter
sudo easy_install tweepy
# Instalar el feedparser
sudo easy_install feedparser

git clone https://github.com/josecolella/DAI_Practica4.git
cd DAI_Practica4
chmod +x index.py
# Para que el script siga ejecutando despues de que salga de ssh
sudo nohup ./index.py 80 &
```

El dns de dicha máquina es http://ec2-54-194-113-118.eu-west-1.compute.amazonaws.com


Vagrant
=======

Vagrant es una herramienta que ofrece un despliegue rapido de un entorno de producción.
Las configuración se hace mediante un fichero `Vagrantfile`, donde se especifican
todas las reglas de la nueva máquina creada, desde la distribución hasta propiedades de red.

Para instalar vagrant se ejecuta

```bash
gem install vagrant
```

El despliegue de la aplicación sobre Vagrant fue el más rapido de todos.
Esto ilustra la importancia de las herramientas de automatización como Chef y Puppet.

Los benchmarks para estas máquinas se han generado desde las máquinas

###Ubuntu 12.04

Antes de poder crear la máquina hay que especificar un port forwarding en el fichero de configuración.
Esto servirá para que se pueda visualizar la aplicación desde afuera.

En la siguiente imagen se puede ver lo que se ha agregado al `Vagrantfile` para tener
port-forwarding. Lo que hará esto es que desde el puerto 8080 podemos visualizar lo
que hay en el puerto 80 de la máquina virtual

!["Port Forwarding"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/vagrant1Photos/Screen%20Shot%202014-01-12%20at%2011.36.44.png)

Para crear la máquina virtual se ejecuta el comando que se puede ver en la siguiente imagen:

!["vagrant up"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/vagrant1Photos/Screen%20Shot%202014-01-12%20at%2011.39.11.png)

Para poder acceder de manera remota se usa el comando que se puede ver en la siguiente imagen

!["vagrant ssh"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/vagrant1Photos/Screen%20Shot%202014-01-12%20at%2011.39.22.png)

Ahora para poder desplegar la aplicación se siguen los siguientes comandos:

```bash
sudo apt-get install -y git
git clone https://gist.github.com/8374477.git Automate
cd Automate/
chmod +x automate.sh
source automate.sh
```

Como se puede ver en la siguiente imagen la aplicación se ha desplegado correctamente

!["application"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/vagrant1Photos/Screen%20Shot%202014-01-12%20at%2011.43.25.png)

El fichero vagrant de esta máquina se puede encontrar [aquí](https://github.com/josecolella/Practica3IV/blob/master/Vagrantfile1)

###Ubuntu 13.10

Para crear la segunda máquina se han tenido que hacer dos cambios en el fichero de configuración.
Uno es cambiar el sistema operativo que se va a descargar, y hacer lo de port forwarding

En la siguiente imagen se puede ver como se hace para cambiar el sistema operativo que se
descarga. Se cambia la url en el cual vagrant busca la distribución.

!["Cambio en sistema"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/vagrant2Photos/Screen%20Shot%202014-01-12%20at%2011.56.05.png)

En la siguiente imagen se puede ver lo que se tiene que cambiar para tener
port-forwarding. En este caso se redirige al puerto 8081 ya que el 8080 esta usado
por la primera máquina.

!["Port Forwarding"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/vagrant2Photos/Screen%20Shot%202014-01-12%20at%2011.59.56.png)

Se crea la máquina con el comando que se visualiza en la siguiente imagen

!["vagrant up"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/vagrant2Photos/Screen%20Shot%202014-01-12%20at%2012.02.18.png)

Se accede remotamente para poder desplegar la aplicación.

```bash
vagrant ssh
```

En la siguiente imagen se puede ver que la máquina vagrant emplea Ubuntu 13.10

!["distribution"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/vagrant2Photos/Screen%20Shot%202014-01-12%20at%2012.02.43.png)

Finalmente se puede ver que la aplicación se ha desplegado correctamente

!["application"](https://raw.github.com/josecolella/Practica3IV/master/Screenshots/vagrant2Photos/Screen%20Shot%202014-01-12%20at%2012.06.44.png)

El fichero vagrant de esta máquina se puede encontrar [aquí](https://github.com/josecolella/Practica3IV/blob/master/Vagrantfile2)

Benchmarks
==========

Sobre las maquinas se han ejecutado varios benchmarks para determinar la como
se comportan debajo el estrez que genera el benchmark. Los benchmarks seleccionados
hacen un emfasis sobre la robustez de la red, y el tiempo de respuestas a las peticiones
de los clientes. Una aplicación robusta tiene que esta disponible para posibles clientes
todo el tiempo posible.

Se han ejecutado los benchmarks desde un ordenador externo para también tener
en cuenta la latencia de red.

###ab
ab es una benchmark para comprobar el rendimiento del servidor web que esta sirviendo
la aplicación. En este caso esta haciendo el benchmark sobre el CGI que proporciona web.py
por defecto.

Para instalar ab en mi ordenador he usado el gestor de paquetes, `brew`.

```bash
brew install ab
```

```bash
ab -n 1000 -c 100 ec2-54-194-187-157.eu-west-1.compute.amazonaws.com/index.html
ab -n 1000 -c 100 http://ivmachine.cloudapp.net/index.html
```

Para los dos he generado 1000 conexiones que serán ejecutadas concurrente 100 a la vez

###httperf
httperf es una herramienta para analizar el rendimiento de un servidor web. Esto significa
que es un benchmark que compruba el tiempo de respuesta a las peticiones generadas de httperf.

Para instalar httperf en mi ordenador he usado el gestor de paquetes, `brew`.

```bash
brew install httperf
```

```bash
httperf --server ec2-54-194-187-157.eu-west-1.compute.amazonaws.com --port 80 --rate 10 --num-conn 1000 --uri /index.html
httperf --server http://ivmachine.cloudapp.net/ --port 80 --rate 10 --num-conn 1000 --uri /index.html
```

El rate determina cuantas peticiones se generan por segundo, mientras que el parametro
de num-conn determina el numero de conexiones.

He creado un script en Python que automatiza el proceso de lanzar y guardar los
resultados de los benchmarks. Basicamente ejecuta el benchmark sobre el proveedor
que se especifica por la linea de comando y guarda los resultados en ficheros txt.

El código se puede encontrar [aquí][5]


###Notas sobre los benchmarks

He enfocado los benchmarks empleados a atacar dos de los componentes más importantes
cuando se tiene una aplicación web, que son la red y la memoria. Estos dos benchmarks
se enfocan en atacar estos componenets de la aplicación. Con los resultados obtenidos
de dichos benchmarks ya se podrán sacar conclusiones sobre cual de las opciones
es optima para la aplicación.




[1]: http://webpy.org
[2]: https://mongolab.com/
[3]: http://aws.amazon.com/ec2/instance-types/instance-details/
[4]: http://msdn.microsoft.com/en-us/library/windowsazure/dn197896.aspx
[5]: https://gist.github.com/josecolella/8374477