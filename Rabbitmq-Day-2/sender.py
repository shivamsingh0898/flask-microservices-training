import pika

#establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Declare an Exchange
channel.exchange_declare(exchange='order_exchange')

#Declare Queues
channel.queue_declare(queue='order_success_queue', durable=True)
channel.queue_declare(queue='order_failed_queue', durable=True)


#Binding Exchange to queues
channel.queue_bind(exchange='order_exchange',
                       queue='order_success_queue',
                       routing_key='success')
channel.queue_bind(exchange='order_exchange',
                       queue='order_failed_queue',
                       routing_key='failed')



#Publish the message to exchange
channel.basic_publish(
    exchange='order_exchange', 
    routing_key='success', body='User Successfully Exchange',
    properties=pika.BasicProperties(headers={'email': 'anita@gmail.com'})
    )
channel.basic_publish(
    exchange='user_registration_exchange', 
    routing_key='error', body='User Failed to Exchange',
    properties=pika.BasicProperties(headers={'email': 'david@gmail.com'})
    )

print("All Messages Sent successfully")
connection.close()