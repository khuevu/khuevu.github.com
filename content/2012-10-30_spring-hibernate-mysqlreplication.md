Title: Integrate Spring and Hibernate with MySQL master/slave database
Category: Technology
Tags: java, spring, hibernate, mysql, scalability

In my previous [post]({filename}/posts/Programming/2012-10-05_mysqlreplication.md), we have setup one master and one slave MySQL database. If you write your application to interact with database using jdbc connector, it already has the [support for database replication](http://dev.mysql.com/doc/refman/5.1/en/connector-j-reference-replication-connection.html). Basically, you need to use `com.mysql.jdbc.ReplicationDriver` and change connection to `readOnly` when you want it to direct traffics to slave instances. What if your application interfaces with database through Hibernate API? Hibernate doesn't explicitly support the replication. Setting Hibernate or Spring's transactions to `readOnly` doesn't change the underlying jdbc connection to `readOnly`. 

The first thing come to mind is to have two separate instances of `Datasource`, one which connection set to `readOnly` and one not; and have two Hibernate's `SessionFactory` contain each. However, this method changes your existing programming model. The second choice is to access the underlying jdbc connection of Hibernate's SessionFactory and switch it to `readOnly` when it is read operation. 

Here we are going to use Spring's AspectJ API to implement this. With Spring AspectJ annotation, we can introduce the switching of connection `readOnly` with least amount of change on code.  

    #!java
    ...
    @Aspect
    public class ConnectionInterceptor {
       
        @Autowired
        private SessionFactory sessionFactory; 

        @Around("@annotation=ReadOnlyConnection")
        public Object proceed(ProceedingJoinPoint pjp) throws Throwable {
            Session session = sessionFactory.getCurrentSession();
            ConnectionReadOnly readOnlyWork = new ConnectionReadOnly();

            try {
                session.doWork(readOnlyWork);
                return pjp.proceed();
            } finally {
                readOnlyWork.switchBack();
                session.doWork(readOnlyWork);
            }
        }
    
    }

Next, define the `@ReadOnlyConnection`:

    #!java

    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.METHOD)
    public @interface ReadOnlyConnection {
    
    }

The `ConnectionReadOnly` class implements `org.hibernate.jdbc.Work` interface.  

    #!java
    ...
    public class ConnectionReadOnly implements Work {
    
        @Override
        public void execute(Connection connection) throws SQLException {
            ...
            connection.setReadOnly(true);
            ...

        }

        //method to restore the connection state before intercepted
        public void switchBack() {
            ... 
        }
    
    }

To enable AspectJ annotation in Spring, you need to add to spring context config file: 

    #!xml
    <aop:aspectj-autoproxy/>
    <bean id="connectionInterceptor" class="com.x.y.z.ConnectionInterceptor">
    </bean>

So for any `ReadOnly` method at your DAO layer, you just need to add the `@ReadOnlyConnection`:

    #!java
    ...
    public class SomeDaoImpl implements SomeDao {
        @Autowired
        private SessionFactory sessionFactory;
        ...
        
        @ReadOnlyConnection
        public Some get(Long id) {
            Session session = sessionFactory.getCurrentSession();
            ...
        }
    }

In case you don't want to use annotation, you can use Spring's xml configuration. For the above example, we will have: 

    #!xml
    <aop:config>
        <aop:aspect id="connectionAspect" ref="connectionInterceptor">
            <aop:pointcut id="connPointCut" expression="execution(* com.x.y.SomeDaoImpl.get(..))"/>
            <aop:around method="proceed" pointcut-ref="connPointCut"/>
        </aop:aspect>
    </aop:config>






