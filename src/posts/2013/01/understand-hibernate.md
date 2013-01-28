Date: 2013-01-27
Title: Basic of Hibernate Concepts 
Tags: hibernate, java
Slug: understand-hibernate
Category: Blog

This article aims to discuss the basic concepts of Hibernate. Those that you need to know well before actually implementing a Hibernate-based application. And if you are already using Hibernate, hope it is still useful for you. Fundamentals always serves as building blocks for advanced techniques, an idea well illustrated in old time Chinese martial art movies. 

## Hibernate's business case: 

Hibernate is mainly designed for web application. Hibernate has `Session` object as its persistence interface. All of the database operations can be invoked through the `Session` object. This `Session` object should be accessed from a single thread. How long a `Session` object lives will be determined by your application design and its business use case. 

Why? when designing a business application, operations are grouped into business transaction, in which, all operations are considered successfully executed only if none of them fail to execute. For example, in a online shopping application, operation to deduct the sold quality from available stock and operation of getting payment from customers are grouped into one transaction. Only when payment is made successfully, the former one is persisted. In other words, a business transaction coordinates the writing out of changes to affected data. Some data can only be meaningfully changed if other is changed too. And in Hibernate, a `Session` represents exactly that, a business transaction or a `unit of work`, a term used by (Hibernate documentation)[http://docs.jboss.org/hibernate/core/3.3/reference/en/html/transactions.html#transactions-locking]

A `Session`, therefore, can span a request (session-per-request) or a conversation (multiple requests).  
