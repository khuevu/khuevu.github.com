Date: 2013-01-27
Title: Application Design with Hibernate 
Tags: hibernate, java
Slug: understand-hibernate
Category: Blog

This article aims to discuss the basic design pattern of a web application using Hibernate; the basic concepts that you need to know well before actually implementing a Hibernate-based application. Hibernate Documentation can be a little bit confusing sometimes. This article tries to distill the important points to help you have a better understanding of Hibernate. And if you are already using Hibernate, hope it is still useful for you. Fundamentals always serves as building blocks for advanced techniques, an idea well illustrated in old time Chinese martial art movies. 

## Hibernate's business case: 

Hibernate has `Session` object as its persistence interface. All of the database operations can be invoked through the `Session` object. This `Session` object should be accessed from a single thread. How long a `Session` object lives will be determined by your application design and its business use case. 

Why? when designing a business application, operations are grouped into business transaction, in which, all operations are considered successfully executed only if none of them fail to execute. For example, in a online shopping application, operation to deduct the sold quality from available stock and operation of getting payment from customers are grouped into one transaction. Only when payment is made successfully, the former one is persisted. In other words, a business transaction coordinates the writing out of changes to affected data. Some data can only be meaningfully changed if other is changed too. And in Hibernate, a `Session` represents exactly that, a business transaction or a `unit of work`, a term used by [Hibernate documentation](http://docs.jboss.org/hibernate/core/3.3/reference/en/html/transactions.html#transactions-locking). In this article, we use the terms business transaction, unit of work, conversation interchangably. 

Hibernate is mainly designed for web application. In which, A `Session`, therefore, can span a request (session-per-request) or a conversation - multiple requests, response cycles (however, you should not keep the Session for a long conversion. We will discuss this later).  

So how exactly a `Session` is related to a business transaction, and why we need to decide how we keep the `Session`? 

A `Session` is not only an abstract layer for your database operations, but also an objects cache. When an object is loaded from a `Session`, Hibernate caches it in memory. This object is often called `managed object`. A particular `Session` always knows which objects it has loaded. When flush is called on this `Session`, Hibernate check for modification on the object (dirty check) and the change made to the object, if any, is automatically flushed to database. 

This mechanism is perfectly suitable for a match between a `Session` and a business transaction. Change during a transaction is staged in memory - `Session`'s cache. Change is persisted by flushing the change to database. If there is error, i.e, Hibernate throws exceptions, `Session` object needs to be discarded, database changes need to be rolled back if necessary. A `Session` also does version checking of managed object when updating to database to detect changes made to this data entity between the time it is loaded to memory and the time it is persisted back to database, which ensures the data integrity during a transaction. 

## Hibernate's Design Pattern:

From Hibernate [documentation](http://docs.jboss.org/hibernate/core/3.3/reference/en/html/transactions.html#transactions-basics):

> A Session is an inexpensive, non-threadsafe object that should be used once and then discarded for. A Session will not obtain a JDBC Connection, or a Datasource, unless it is needed. It will not consume any resources until used. 

A Hibernate Session can span multiple physical database transactions. Hibernate `Session` will acquire a JDBC connection when transaction start. That means all communication with database must occur inside a transaction. When transaction is committed, Hibernate will release the collection. Typically, your data access code will be: 

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

    // Obtain new Session at the begining of unit of work.
    Session session = sessionFactory.openSession();  
    session.setFlushMode(FlushMode.NEVER); // IMPORTANT
    
    //Obtain new JDBC Connection, start DB Transaction
    Transaction tx = session.beginTransaction(); 
    Foo foo = session.get(Foo.class, id);
    ...
    // release JDBC Connection during the unit of work. Waiting for user next request.
    tx.commit(); 
     
    
The `Session` should be disconnectied from JDBC connection during user think time by calling `tx.commit()`. Note that you need to set the `FlushMode` to `NEVER`. The `tx.commit()` will auto flush the session otherwise. We are still in a unit of work (business transaction), thus we don't want to flush the cahnge to database yet. (I believe there is a bug in Hibernate documentation, in which it states that the `FlushMode.MANUAL` will prevent the flushing when a transaction is committed. But the [java doc](http://docs.jboss.org/hibernate/orm/3.2/api/org/hibernate/Transaction.html) says the former')

The next request within the same unit of work, the `Session` object will open another database transaction: 

    Transaction tx = session.beginTransaction // same Session, obtain new JDBC Connection
    
    //previously loaded foo object. 
    foo.setProperty("bar");
    
    tx.commit();

The `Session` knows the foo object is the one it loaded previously. At the last transaction in the conversation, we flush the change to database and discard the `Session`: 


    session.flush();
    tx.commit();
    session.close();
       
Change made to the foo object will be flushed to database. This approach is efficient in database access. No resource is used until needed. Refer to this [article](https://community.jboss.org/wiki/OpenSessionInView#What_about_the_extended_Session_pattern_for_long_Conversations) for more details. 

And you should never have a long transaction spanning the whole conversation. Having a long database transaction not only hogs resource but also leads to stale data due to concurrent access. StaleObjectStateException will be thrown. It prevents your application to scale concurrently. (Do note that within a thread, a single database transaction is going to perform better than many small transactions, [even for reading data](http://docs.jboss.org/hibernate/core/3.3/reference/en/html/transactions.html#transactions-demarcation))

This pattern, however, is not suitable for a long conversation. With loaded objects kept in memory, you will soon run hit OutOfMemory error if you keep the `Session` for too long. So for a long conversation, we use an alternative approach. 

### Detached Session - For long conversation

To keep memory from overflowing during a long conversation, we use a new session for each user interaction. In this pattern, the staging change will be kept by mean of persistent objects. The managed objects that change is made directly to. You keep these objects between interactions, detach them from old `Session` when it is closed and re-attach them to the new `Session`. So the persistent objects are ones that are kept within `HttpSession` 's context within a unit of work. You can re-attach an object by calling `Session`'s `merge` or `saveOrUpdate`:

    // foo is an instance loaded by a previous Session
    foo.setProperty("bar");
    
    session = factory.openSession(); // open new session
    Transaction tx = session.beginTransaction();
    
    session.saveOrUpdate(foo); // Use merge() if "foo" might have been loaded already
    
    t.commit();
    session.close();
    
## Hibernate Integration

In practice, we don't often need to write our own transaction code. We use Hibernate or Spring's HibernateTransactionManager instead. These transaction managers wrap a transaction around method invokation, which requires database accesses. But in essense, they are all doing the same thing as described above: obtain a session, start the transaction, flush the session if needed, commit the transaction, discard the session if needed; roll back transaction and discard session if exception is thrown. 

Transaction's boundary can be defined using annotation or clear [point cut (AOP)](https://community.jboss.org/wiki/SessionHandlingWithAOP); transactions can be nested; A business transaction might not involve only Hibernate's transaction but other resources' transactions as well; nested transactions. We will discuss these matters in next article on hibernate. 
