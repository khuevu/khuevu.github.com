Date: 2013-01-27
Title: Basic of Hibernate Concepts 
Tags: hibernate, java
Slug: understand-hibernate
Category: Blog

This article aims to discuss the basic concepts of Hibernate. Those that you need to know well before actually implementing a Hibernate-based application. And if you are already using Hibernate, hope it is still useful for you. Fundamentals always serves as building blocks for advanced techniques, an idea well illustrated in old time Chinese martial art movies. 

## Hibernate's business case: 

Hibernate has `Session` object as its persistence interface. All of the database operations can be invoked through the `Session` object. This `Session` object should be accessed from a single thread. How long a `Session` object lives will be determined by your application design and its business use case. 

Why? when designing a business application, operations are grouped into business transaction, in which, all operations are considered successfully executed only if none of them fail to execute. For example, in a online shopping application, operation to deduct the sold quality from available stock and operation of getting payment from customers are grouped into one transaction. Only when payment is made successfully, the former one is persisted. In other words, a business transaction coordinates the writing out of changes to affected data. Some data can only be meaningfully changed if other is changed too. And in Hibernate, a `Session` represents exactly that, a business transaction or a `unit of work`, a term used by [Hibernate documentation](http://docs.jboss.org/hibernate/core/3.3/reference/en/html/transactions.html#transactions-locking)

Hibernate is mainly designed for web application. In which, A `Session`, therefore, can span a request (session-per-request) or a conversation - multiple requests, response cycles (however, you should not keep the Session for a long conversion. We will discuss this later).  

## Hibernate's design: 

So how exactly a `Session` is related to a business transaction, and why we need to decide how we keep the `Session`? 

A `Session` is not only an abstract layer for your database operations, but also an objects cache. When an object is loaded from a `Session`, Hibernate caches it in memory. This object is often called `managed object`. A particular `Session` always knows which objects it has loaded. When flush is called on this `Session`, Hibernate check for modification on the object (dirty check) and the change made to the object, if any, is automatically flushed to database. 

This mechanism is perfectly suitable for a match between a `Session` and a business transaction. Change during a transaction is staged in memory - `Session`'s cache. Change is persisted by flushing the change to database. If there is error, i.e, Hibernate throws exceptions, `Session` object needs to be discarded, database changes need to be rolled back if necessary. A `Session` also does version checking of managed object when updating to database to detect changes made to this data entity between the time it is loaded to memory and the time it is persisted back to database, which ensures the data integrity during a transaction. 

## Hibernate's Design Pattern:

From Hibernate [documentation](http://docs.jboss.org/hibernate/core/3.3/reference/en/html/transactions.html#transactions-basics):

> A Session is an inexpensive, non-threadsafe object that should be used once and then discarded for. A Session will not obtain a JDBC Connection, or a Datasource, unless it is needed. It will not consume any resources until used. 

A Hibernate Session can span multiple physical database transactions. Hibernate `Session` will acquire a JDBC connection when transaction start. That means all communication with database must occur inside a transaction. When transaction is committed, Hibernate will release the collection. Typically, your data access code will be: 

    #!java
    Session sess = factory.openSession();
    Transaction tx;
    try {
        tx = sess.beginTransaction();
        //do some work
        ...
        tx.commit();
    }
    catch (Exception e) {
        if (tx!=null) tx.rollback();
        throw e;
    }
    finally {
        sess.close();
    }
    
The code above is simplest form to give you an idea of different steps handling a `Session`. Usually, you should access the `Session` object through `SessionFactory.getCurrentSession`, or putting the transaction boiler plate code in a filter or AOP interceptor instead. 

If, outside a transaction, you try to access a data object or its laizly initialized property (we will talk about it later) exception will be thrown by Hibernate. You will need to start DB transactions to write to DB or transactions to read only. That's why you might have several physical transactions over a Session - a business transaction. We will discuss these scenarios nextby considering some of the design pattern for Hibernate web application: 

### Session per Request:

Your business transaction spans only one request. For each thread that handles incoming request, a new `Session` is opened and closed after processing is finished. 

You might encountered a problem with this design. Your `Session` object is normally closed when the main processing logic is completed but before your application renders view to return to client. When rendering view, some uninitialized data might need to retrieved for displayed; but the `Session` is already closed. A typical scenario is displaying collection which is marked as `LazyInitialization`. One feature of Hibernate is Lazy Loading. In ORM, relations between tables are represented as properties of collections in a object model. When retriveing the object from database, if the object's collection is lazy loaded, Hibernate defers the retrieval of the collection until being queried. It helps avoid overflow of available memory due to large collections. 

The solution to this problem is keep the session open until the view rendered completely but just before the response is returned to client (`Open Session In View`). Alternatively, you can have two DB transactions for one `Session`. The first transaction is opened for main logic processing. Don't discard the `Session` after that. The second transaction is a read only transaction started during rendering phase. You can find a very good article about these solutions [here](https://community.jboss.org/wiki/OpenSessionInView). 

### Extended Session - Session per conversation 

Your business transaction spans multiple request-reply cycles. In this Extended Session pattern, you reused the `Session` object between requests and only discard it when the unit of work complete. The `Session` object is bind to the conversation by storing in the `HttpSession`. The `Session` should keep the transaction boundary within a request processing time:

    #!java
    Session session = sessionFactory.openSession(); // Obtain new Session at the begining of unit of work. 
    Transaction tx = session.beginTransaction(); //Obtain new JDBC Connection, start DB Transaction
    Foo foo = session.get(Foo.class, id);
    ...
    tx.commit(); // release JDBC Connection during the unit of work. Waiting for user next request. 
    
The `Session` should be disconnectied from JDBC connection during user think time. This approach is efficient in database access. No resource is used until needed. And you should never have a long transaction spanning the whole conversation.  

### Detached Session - For very long conversation
