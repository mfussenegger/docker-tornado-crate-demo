====================================
Docker / Crate / Tornado Webapp Demo
====================================

Simple demo to showcase how to run a tornado python web application with a
Crate backend using docker containers.

Requirements
============

 - Docker installed


Prepare Docker Images
=====================

Get Crate docker image::

    docker pull crate:latest


Build the Docker image that contains the webapp::

    docker build -t webapp .


Run the crate container::

    docker run --rm -t -i --name db crate

In a separate shell run the webapp container::

    docker run -p 8080:8080 --link db:db -t -i --rm webapp
