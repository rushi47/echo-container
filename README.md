
# Echo Container

As the name suggests echo container, is light weight container which can be used for testing while 
writing helm charts or if you want to just play with docker. My initial idea while developing 
this was, I wanted something which I can use to test my health checks, readiness probe, liveness
probe while writing helm charts.

With the same idea i build out this service. Below are the API References, to quickly get
started with your development.

> Brownie ;) Wanna test it in k8s and bored of writing helm chart ? Head over to below repo and get the helm chart for this container. https://github.com/rushi47/echo-container-chart 

## In Action

Working of code is quite straight forward, and all endpoints work on GET request. There is one flag named `ready` inside the app
which is used to know if the code is maintenance or not. The flag is controlled by different endpoints documented
[below](#api-reference).

When `App is in maintenance` below endpoints will fail: 

* `/health` & `/` 
* `/rprobe` & `/rediness_probe`
* `/lprobe` & `/liveness_probe`

App can be added in maintenance using the endpoint `/setm` documented [below](#api-reference).

`App will automatically, recover after 220 seconds, if not removed from maintenance before that.`

### Environment Variables 
App can be configured using few of **Env Variables** : 

* **SLEEP_TIME** : If time for automatic recovery need to change it can be changed by passing `SLEEP_TIME` in seconds. `Default: 200` 

```bash
docker run -p 8080:8080 -e SLEEP_TIME=100 --name echo_svc echo_containe
```

* **ECHO_PORT** : If port for the app needs to be changed. `Default: 8080`

* **ECHO_DEBUG** : If app debug mode needs to be changed, Supports boolean. `Default: True`

## Run

Container can be built using 

```bash
  docker built -t echo_container .
```

Run the container which we just built

```bash
  docker run -p 8080:8080 --name echo_svc echo_container
```
## API Reference

#### Health check

```http
 /
 /health
```
| Method | Return Status Code    | Description                       |
| :-------- | :------- | :-------------------------------- |
| GET      |  200 | Return 200 when app is not in maintenance mode|
| GET      |  503 | Return 503 when app is in maintenance mode|

#### Get IP of container

```http
 /ip
 /getip
```
| Method | Return Status Code    | Description                       |
| :-------- | :------- | :-------------------------------- |
| GET      |  200 | Return 200 and output of command : hostname -I|

#### Readiness probe endpoint

```http
 /rprobe
 /rediness_probe
```
| Method | Return Status Code    | Description                       |
| :-------- | :------- | :-------------------------------- |
| GET      |  200 | Return 200 if app is not in maintenance mode |
| GET      |  503 | Return 503 if app is in maintenance mode |

#### Liveness Probe

```http
 /lprobe
 /liveness_probe
```
| Method | Return Status Code    | Description                       |
| :-------- | :------- | :-------------------------------- |
| GET      |  200 | Return 200 when app is not in maintenance mode|
| GET      |  503 | Return 503 when app is in maintenance mode|


#### Set Maintenance

```http
 /setm
 /set_maintenance
```
| Method | Return Status Code    | Description                       |
| :-------- | :------- | :-------------------------------- |
| GET      |  200 | Return 200 and set app in maintenance mode |

#### Remove Maintenance

```http
 /remom
 /remove_maintenance
```
| Method | Return Status Code    | Description                       |
| :-------- | :------- | :-------------------------------- |
| GET      |  200 | Return 200 and remove app from maintenance mode |


