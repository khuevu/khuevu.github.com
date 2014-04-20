Title: A Tutorial to set up MySQL replication (master/slave) for high scalability
Tags: mysql, replication, scalability, tutorial

In this tutorial, we will set up two instances of MySQL on your localhost, one master and one slave and enable data replication between the master and the slave.

There are several options when you want to scale horizontally with a MySQL database including database sharding, using MySQL Cluster with NDB storage or a master/slave setup. You can refer to this [link](http://www.oshyn.com/_blog/General/post/A_Summary_of_Scaling_Options_for_MySQL/) for a more detailed summary. Master/slave will be suitable for your application if it performs a lot of read operations rather than write. So distributing the read operations accross multiple instance will help reduce the load on one master instance and enables scaling out. 

### Configuration

If you haven't had MySQL, download it from [here](http://www.mysql.com/downloads/mysql/), untar it and extract to a folder of your choice. Add the `bin` folder to your `PATH` if you don't want to specify the full path when invoking the process.  

Create the folder for config files and data of master and slave instances:

    #!bash
    mkdir -vp ~/replication/{master,slave}/{conf,data,log}

Run `mysql_install_db` script to populate the require `mysql` schema for each instance: 

    #!bash
    scripts/mysql_install_db --no-defaults --datadir=~/replication/master/data
    scripts/mysql_install_db --no-defaults --datadir=~/replication/slave/data

Configure master instance: In `~/replication/master/conf/`, create `my.cnf`:

    #!bash
    # master my.cnf

    [client] 
    port    =   3306
    socket  =   ~/replication/master/mysqld.sock

    [mysqld]
    socket  =   ~/replication/master/mysqld.sock
    port    =   3306
    datadir =   ~/replication/master/data
    #basedir: location of your MySQL installation
    basedir =   ... 
    ...

Next, start the master instance using the command: 
    
    #!bash
    mysqld --defaults-file=~/replication/master/conf/my.cnf

Create `replicatedb`, after log in using mysql client: 

    #!bash
    mysql> CREATE SCHEMA `replicatedb`;

Populate some table and data for your schema. Next we need to tell the server to use binary log to log change made to this schema. Add the following lines to the `my.cnf` file, under server section: 

    #!bash
    log-bin =   ~/replication/master/log/mysql-bin.log
    binlog-do-db    =   replicatedb
    server-id   =   1

Note that the server-id must be unique between master and slaves. If you want replication for multiple schema, use multiple `binlog-do-db` option. Restart the server.

### Create user for replication:

Next create the user which has the `REPLICATION SLAVE` permission, which slave instances will use to access master data. In mysql client command: 

    #!mysql
    mysql> CREATE USER 'slave'@'127.0.0.1' IDENTIFIED BY `slave`;
    mysql> GRANT REPLICATION SLAVE ON *.* TO 'slave'@'127.0.0.1';

### Obtain replication point

Still in the mysql client console: 

    #!mysql
    mysql> FLUSH TABLES WITH READ LOCK;
    mysql> SHOW MASTER STATUS;
    
Output: 

    #!mysql
    +------------------+----------+------------------+------------------+
    | File             | Position | Binlog_Do_DB     | Binlog_Ignore_DB |
    +------------------+----------+------------------+------------------+
    | mysql-bin.000016 |      106 | replicatedb      |                  |
    +------------------+----------+------------------+------------------+

The above commands will lock the master database, preventing any writes to it, and output the current coordinate of binary log. Then we will dump a database snapshot of the master and restore it to the slave instance. If we don't look the database, and new change made to it, there will be inconsistence between the master's data and the snapshot, which leads to a corrupted databases on the slave. 

    #!bash
    mysql -u root -p replicatedb > replicatedb.sql


### Setup slave instance

To setup the slave, instance, create a similar configure file as master instance and change the port number to 3307. Enable `binlog` for slave instance if you want it later to serve as the master to other slave instances (which help reduces the sync requests to a single master). And add the following lines:

    #!bash
    [mysqld]
    ...
    server-id   =   2
    replicate-do-db =   replicatedb

Start slave instance: 
    
    #!bash
    mysqld --defaults-file=~/replication/slave/conf/my.cnf

Restore the dumped file: 

    #!bash
    mysql -u root -p -h "127.0.0.1" -P 3307 replicatedb < replicatedb.sql

After you has restore the dumped data to slave instance, unlock the table in master instance:

    #!mysql
    mysql> UNLOCK TABLES;

Then we need to tell the slave instance the username and password it is going to use for replication, the coordinate of the bin log file. Login to slave instance using mysql client, type in the following commands:

    #!mysql
    mysql> STOP SLAVE;
    mysql> CHANGE MASTER TO
            MASTER_HOST='127.0.0.1',
            MASTER_USER='slave',
            MASTER_PASSWORD='slave',
            MASTER_PORT=3306,
            MASTER_LOG_FILE=mysql-bin.000016,
            MASTER_LOG_POS=106;
    mysql> START SLAVE;






