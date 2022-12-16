#!/usr/bin/env python

import pika

class Publisher:

    def __init__(self, host, port, username, password, queue):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue = queue
        self.channel = ''

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port ,virtual_host='/',credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue)
    
    def submit(self, data):
        return self.channel.basic_publish(exchange='', routing_key=self.queue, body=str(data))
