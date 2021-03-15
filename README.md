# Twitter stream logger #

## Goal ##

+ Connect to the [Twitter Streaming API][twitter_streaming_api]
+ Filter messages
+ Keep track of messages per second statistics across multiple runs of the application

## Architecture ##

The project was done using the [microservices architectural pattern][microservices_article].

It is common to use HTTP (and REST), but as we’ll see, 
we can use other types of communication protocols such as RPC (Remote Procedure Call) 
over AMQP (Advanced Message Queuing Protocol).

For that, we will use [Nameko][nameko], a Python microservices framework. 
It has RPC over AMQP built in, allowing for you to easily communicate between your services. 
It also has a simple interface for HTTP queries, which we’ll use in this project for simplicity. 
However, for writing Microservices that expose an HTTP endpoint, 
it is recommended that you use another framework, such as [Flask][flask] or [FastAPI][fastapi]. 
To call Nameko methods over RPC using Flask, you can use [flask_nameko][flask_nameko], 
a wrapper built just for interoperating Flask with Nameko.

Also Nameko allows to scale the service very easily.
Nameko is built to robustly handle methods calls in a cluster.
It’s important to build services with some backward compatibility in mind, 
since in a production environment it can happen for several different versions of the same 
service to be running at the same time, especially during deployment. 
If you use Kubernetes, during deployment it will only kill all the old version containers 
when there are enough running new containers.

For Nameko, having several different versions of the same service running at the same 
time is not a problem. Since it distributes the calls in a round-robin fashion, 
the calls might go through old or new versions. 

The service classes are instantiated at the moment a call is made and destroyed after 
the call is completed. 
Therefore, they should be inherently stateless, meaning you should not try to keep any 
state in the object or class between calls. 
This implies that the services themselves must be stateless. 
With the assumption that all services are stateless, 
Nameko is able to leverage concurrency by using [eventlet][eventlet] greenthreads. 
The instantiated services are called “workers,” and there can be a configured maximum 
number of workers running at the same time.

## Requirements

* [Docker][docker]
* [Docker-compose][docker-compose]


### Running

```shell script
$ docker-compose up
```

or 

```shell script
$ docker-compose up -d
```
if you don't want to see logs.

Then after it's up you can use the launch endpoint to launch streaming:

```shell script
$ curl -i -d '{"track": ["bieber"]}' localhost:8004/launch
```
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 25
Date: Mon, 08 Feb 2021 11:28:00 GMT

{"process_started": true}
```

And view statistics about the stream:

```shell script
$ curl -i localhost:8004/statistics
```
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 63
Date: Mon, 08 Feb 2021 11:28:40 GMT

{"amount": 10, "speed": 0.3448275862068966, "elapsed_time": 29}
```

### Tests

```shell script
$ make coverage
```
to run the tests with coverage

### Log file

```shell script
$ make log
```
to view the log file.

### Service shell

```shell script
$ docker-compose exec statistics bash
```

```shell script
root@33f8d35d65ba:/app# nameko shell --config config.yml
Nameko Python 3.9.1 (default, Jan 12 2021, 16:45:25) 
[GCC 8.3.0] shell on linux
Broker: amqp://guest:guest@rabbit:5672/
>>> 
```

And to interact with a service inside nameko shell:

```shell script
n.rpc.statistics.get_statistics()
```

It will give the statistics.
You can access all the services.

Use exit() or Ctrl-D (i.e. EOF) to exit.

### To Do

* Add Flask or Fast API with a proper validation ans schemas
* Add Flasgger
* Add CI/CD
* Add Swagger documentation
* Add Unit and functional tests
* Transform services to packages
* Catch negative use case scenarios
* Add k8s to manage the nodes running the service
* Extend statistics

[twitter_streaming_api]: https://developer.twitter.com/en/docs
[microservices_article]: https://martinfowler.com/articles/microservices.html
[nameko]: https://nameko.readthedocs.io/en/stable/
[flask]: https://flask.palletsprojects.com/en/1.1.x/
[fastapi]: https://fastapi.tiangolo.com/
[flask_nameko]: https://github.com/jessepollak/flask-nameko
[eventlet]: http://eventlet.net/
[docker]: https://docs.docker.com/get-docker/
[docker-compose]: https://docs.docker.com/compose/install/