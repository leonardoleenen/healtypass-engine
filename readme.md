# 1. Acerca de HealtyPass Engine 
HealtyPass Engine permite generar, administrar y mantener las libretas sanitarias de las personas en forma descentralizadas y seguras. Es decir, HealthyPass engine provee de un conjunto de servicios que permiten la generacion de los certificados de sanidad aplicando encriptación asimétrica y validación de orígen. 

# 2. Como funciona? 
HealtyPass tiene dos actores: Quien otorga el certificado y quien se beneficia del mismo. Cada certificado pertenece exclusivamente al beneficiario y queda en su poder. 

HealthyPass expone  un servicio para que un solicitante (generalmente desde una app) inice un proceso de solicitud de certificado  a una entidad certificante. Esta petición es derivada a la entidad certificante (**mencionadas en adelante como C.A de sus siglas Certificate Authority**) con las credenciales de HealthyPass. La CA puede otorgar o no el certificado. Ya sea por la afirmativa o por la negativa, el flujo de información es exactamente igual. 

Todos los certificados tiene al menos dos secciones: una sección de request que especifica los datos de origen del request. Generalmente son los datos de la persona que realiza el request y los motivos del mismo. Esta sección no es fija y depende de los datos que requiera la entidad certificante para poder otorgar el certificado (o no)

Estructura modelo del certificado. 
```json
{
    "cid":.....,
	"request":{
		...,
		"ksp":{
			"public_key": ....,
			"kind": ...,
			"signature":...
		}
	},
	"ca_response": {
		...,
		"ksp":{
			"public_key": ....,
			"kind": ...,
			"signature":...,
		}
  },
}
```

## 2.1 Generación del request 
La petención se inicia desde el requirente el cual debe proporcionar los datos solicitados por la C.A (puede ser nombre, apellido, genero, id, etc). Adicionalmente se debe proporcionar una sección particular llamada ksp (Key sign party) donde se exponen los datos públicos que garanticen la inmutabilidad de la información. Los datos solicitados son public_key, el cual es la clave pública que permita verificar que el contenido no ha sido adulterado. Kind se refiere al mecanimos de crypto que se ha usado. Al momento de generar el presente documento el mecanimos popularmente soportado es PGP. Si bien por el momento es el único queda abierta la posibilidad para que se adopten otros mecanismos en el futuro. 

Cabe destacar que la sección de ksp es opcional ya que garantiza la inmutabilidad de la información y tanto para HealthyPass como para la C.A el lazo de confianza se establece con la aplicación cliente. 

Este request (solicitud) es recibido por HealthyPass quien luego establece un handShake con la autoridad certificante a fin de generar el certificado. 

Una vez que es recibida la solicitud por HealthyPass de devuelve una respuesta **pero no el certificado generado** sino que devuelve una solicitud "in progress". Esto se debe a que no es posible determinar si la C.A puede resolver la petición en ese momento o lo hará bajo disponibilidad. Por tal motivo a la solicitud se devuelve un objeto (mismo request) con un código especial el cual es considerado código de rescate. Este código es el que luego se exhibe para completar el proceso. 

La respuesta resultante será muy similar a esta

```json
{
  	
	"request":{
        "cid":"zb2rhe5P4gXftAwvA4eXQ5HJwsER2owDyS9sKaQRRVQPn93bA",
		"firstName":"John",
		"lastName" :"Connor",
		"birthDate":"02/11/1990",
        "email":"john.connor@gmail.com",
        "issuedOn":18892204953,
		"ksp":{
			"public_key": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDfjLg3FtMBih1GeEPaA/5luiMAzQIWUEp9C4H5SC86jvrPo7KqlNU6hHoq/OGhuZ5Yr7VmznD8...",
			"kind": "PGP"
			"signature":"6e6ff7950a36187a801613426e858dce686cd7d7e3c0fc42ee0330072d245c95..."  
		}
	}
}
```
Cada response por parte de HealthyPass devuelve un CID el cual es un código único de tipo content addresseable. Esto **no debe considerarse nunca como el id de certificado sino como un código transitorio**

## 2.2 Acerca de los CID  y consideraciones especiales 
HealthyPass usa CID para identificar el contenido de sus mensajes. Los CID son identificadores especiales que estan orientados al contenido del mensaje. No se debe considerar como una medida de seguridad o critografía del contenido (si bien se hace criptografía) ya que su proposito es tener un elemento de "doble control"  sobre el contenido. 

De esta forma, cada miembro que agrega información al certificado tiene la obligación de generar su propio CID para tener de este modo un doble control sobre la información generada

Para tener información mucho más detallada de este tipo de contenido referirse a: https://github.com/multiformats/cid

## 2.3 Repositorio temporal de las solicitudes 
Una vez que la solicitud es generada queda en un store temporal hasta que la C.A pueda resolver ese pedido. Dicho pedido puede resolverse en forma inmedianta o bien puede demorar en resolverse. Debido a esta situación es que HealthyPass trabaja en forma asincrónica. Una vez que la petición es resuelta, se comunica al solicitante el resultado (el cual puede ser positivo o negativo). 

Para ello, la app cliente debe suscribirse a una cola a la espera de la resolución de su proceso. Todos los procesos tienen al menos tres estados: 

- PENDING, significa que el proceso aún no fue resuelto por la C.A 
- APROBED, lo que significa que el certificado fue aprobado 
- NOT APROBED, lo que significa que no fue aprobado por la C.A 

Para consultar el estado de una solicitud siempre se utiliza el mismo CID (código de rescate). Una vez que la solicitud fue aprobada (o rechazada) la app cliente remueve este estado de la cola (despeja) y el certificado es eliminado. 

En caso que la APP cliente nunca lo pida, la cola lo depura y guarda en los historicos. 

## 2.4 Solicitudes aprobadas
Una vez que la solicitud es aprobada la misma se devuelve a la cola a la espera que sea "rescatada"  por el requierente. Las solicitudes que no sean rescatadas dentro del periodo establecido de TimeOut de la cola son archivadas en el historico y podrán ser rescatadas unicamente por solicitud. 

Cuando la solicitud es aprobada por la C.A la misma realiza las siguientes tareas: 

1. Completa la información de respuesta (estado, fecha de estado, etc)
2. Firma con su clave privada el contenido 

Esa información vuelve a HealthyPass quien termina de confeccionar el certificado agregando 
1. CID para el request de la C.A 
2. Signature de todo el certificado 
3. Generar los certificados digitales para ser distribuidos (passkit API, etc)

```json
    {
      "certificate_id":"vjklsoj4n6990QQnzzs22DSoco3mm2ede01983",
      "request":{
        "cid":"zb2rhe5P4gXftAwvA4eXQ5HJwsER2owDyS9sKaQRRVQPn93bA",
        "firstName":"John",
        "lastName" :"Connor",
        "birthDate":"02/11/1990",
        "email":"john.connor@gmail.com",
        "issuedOn":18892204953,
        "ksp":{
          "public_key": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDfjLg3FtMBih1GeEPaA/5luiMAzQIWUEp9C4H5SC86jvrPo7KqlNU6hHoq/OGhuZ5Yr7VmznD8...",
          "kind": "PGP",
          "signature":"6e6ff7950a36187a801613426e858dce686cd7d7e3c0fc42ee0330072d245c95..."  
        }
      },
      "ca_response":{
        "cid":"OPPSxvd9924dfvGT54GTTwasss23149CRV",
        "status":"APPROVED",
        "certKind":"A",
        "issuedOn":1889301344,
        "typeOfCertificate":"ASISTENCIA A PERSONAS MAYORES O CON DISCAPACIDAD",
        "authorizedSince":198908912,
        "authorizedUntil":198889998,
        "authorizedTrip":[[-32.32132,68.0929302],[-38.0023232,72.0023223]],
        "ksp":{
          "public_key": "ZZZZyy22NzaC1yc2EAAAADAQABAAABgQDfjLg3FtMBih1GeEPaA/5luiMAzQIWUEp9C4H5SC86jvrPo7KqlNU6hHoq/OGhuZ5Yr7VmznD8...",
          "kind": "PGP",
          "signature":"00224efhhesdhfs7950a36187a801613426e858dce686cd7d7e3c0fc42ee0330072d245c95..."
        }
      }

    }
```

NOTA: Los campos de respuesta de la C.A dependen exclusivamente de ella y son agnostico para HealthyPass. De todas formas, HP tiene atributos reservados que luego son utilizados para presentar en el certificado. 

## 2.5 Atributos reservados 
Cada sección tiene sus atributos reservados que son utilizados por el engine para realizar validaciones. El atributo en común siempre es 

### 2.5.1 Atributos del request
| Atributo | Descripción | 
|----------|:------------|
| firstName   | Es el nombre del la persona|
| lastName | Es el apellido de la persona | 
| birthDate | Es la fecha de nacimiento de la persona | 
| email | (opcional) Email de la persona |
| issuedOn | Fecha en la que fue requerido el certificado | 


### 2.5.2 Atributos de ca_response

| Atributo | Descripción | 
|----------|:------------|
| status   | Indica el estado del certificado los cuales pueden ser APPROVED, NOT APPROVED|
| certKind | Indica el tipo de certficado. Generalmente son letras y nros como A,B,C, A1,B2,C1
| issuedOn | Indica la fecha que fue aprobado el certificado. El formato es timestamp, numérico y en milisegundos |
| type | Es un texto descriptivo del tipo de certificado | 
| authorizedSince | (opcional) Es la fecha en la que entra en vigencia el certificado |
| authorizedUntil | (opcional) Es la fecha que vence el certificado | 
| authorizedTrip | (opcional) Es un vector de posiciones latitud / Longitud que delimita el área habilitada 

## 2.6 Solicitudes rechazadas 
La potestad de aprobar o rechazar una solicitud siempre es prerrogativa de la C.A y la C.A puede delegar parte de esa prerrogativa a HealthyPass. 

Cuando una solicitud es rechazada, de igual manera se genera un id de certificado pero con estado no aprobado. 

Todos los certificados ya sean NO APROBADOS o bien que luego fueron revocados integran lo que se conoce como "Black List". Las black list es un repositorio de todos los certificados emitidos y que fueron revocados (no incluye a los que están vencidos)

# Que pasa si? 

## 1. La C.A deja de responder 
HealthyPass seguirá intentando con una politica decreciente, es decir, la comienzo intentará durante periodos de un minuto, luego 3, luego 10 y sucesivamente hasta llegar al TimeOut y remover todo de la cola y pasarlo al historico como timeOut

## 2. La aplicación cliente envia el request sin CID o con un CID repetido
En este caso el engine devuelve el request como ínvalido 

## 3. La Aplicación cliente envia el request sin ksp
Este campo es opcional. Para el engine la App es quien tiene el lazo de confianza. 


