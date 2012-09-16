Date: 2012-09-13
Title: MySQL Performance Optimization - Part 1
Tags: mysql, optimization
Slug: mysql-optimization
Category: Blog

Database optimization is very crucial for any production grade application to achieve scalability and high performance. MySQL optimization involves different levels, from optimizing SQL queries, configuring system variables, buffer and cache, refining database structure. This article is going to focus on the first part: optimizing SQL queries to reduce response time. 

Optimizing SQL query can be restructuring your query, adding indexes. The `(*)sec` returned when a query executed is the benchmark on how different optimizations affect the response time. This article will cover optimization of SELECT statments. The optimization of DML statements will be left for later posts.  

## The EXPLAIN syntax

`EXPLAIN` command is a very important tool to understand how query is executed in MySQL. When you type `EXPLAIN SELECT...`, MySQL doesn't actually perform the query. It just analyzes and tell you how the query will be executed. Some of the output information:  

    select_type | table | type | possible_keys | key | key_len | rows | extra

*   select_type: type of select statement.
*   table: table name 
*   type: Join Types, explains how tables are joined
*   possible_keys: possible indexes to choose
*   key: actually index chosen
*   rows: the estimated number of row need to be examined
*   extra: additional information

Based on these information, we can start optimize our query. When a `SELECT` is executed, there are two ways that MySQL will retrieve the records. It can either scan the table row by row or do an index look up to find the records explicitly. Most of the times, the later case is more desirable and can improve performance significantly. Or that is to say, there should be an used index, i.e, key value in result of explain command

### Simple SELECT example: 

Let's consider a `USER` table: 

    |id | first_name | last_name  |
    |---|------------|----------- |
    |INT| VARCHAR(30)| VARCHAR(30)|

Do a `SELECT` statement based on primary key `id`:

    EXPLAIN SELECT * FROM user WHERE id = 1;

Output:

    | id | select_type | table | type  | possible_keys | key     | key_len | ref   | rows | Extra |
    |----|-------------|-------|-------|---------------|---------|---------|-------|------|-------|
    |  1 | SIMPLE      | user  | const | PRIMARY       | PRIMARY | 4       | const |    1 |       |

*   select_type: `SIMPLE`, a single select statement, not a join statment. 
*   type: `const`, at most one matching row, very fast
*   key: `PRIMARY`, primary key is used for look up operation

Let's do another `SELECT`:
    
    EXPLAIN SELECT * FROM user WHERE first_name = 'khue';

We will see the result:

    | id | select_type | table | type  | possible_keys | key     | key_len | ref   | rows | Extra       |
    |----|-------------|-------|-------|---------------|---------|---------|-------|------|-------------|
    |  1 | SIMPLE      | user  | ALL   | NULL          | NULL    | NULL    | NULL  |   18 | Using where |

No key is used to look up the result. MySQL optimizer performs a full table scan (row by row) to retrieve the record. To improve the performance, simply add the index to first_name column: 

    ALTER TABLE user ADD INDEX first_name_index (first_name); 

When you have an index on `first_name`, optimizer will still be able to use this index when you only select based on part of the key only: 

    SELECT * FROM user WHERE first_name = 'kh%';

    | id | select_type | table | type  | possible_keys   | key             | key_len | ref   | rows | Extra       |
    |----|-------------|-------|-------|-----------------|-----------------|---------|-------|------|-------------|
    |  1 | SIMPLE      | user  | ALL   | first_name_index| first_name_index|       30| const |   1  | Using where |


### SELECT based on multiple columns:

How about searching for record based on two column: 

    SELECT * FROM user WHERE first_name = 'khue' AND last_name = 'vu';

You can add a multiple column index: 

    ALTER TABLE user ADD INDEX first_last_index (first_name, last_name); 

With the above index, the optimizer will use `first_last_index` for `SELECT` with `WHERE` clause like: 

    first_name = 'abc' AND last_name = 'xyz'
    first_name = 'abc' AND (last_name = 'x' OR last_name = 'y')

But not for: 
)
    last_name = 'xyz'
    first_name = 'abc' OR last_name = 'xyz'

In other words, MySQL optimizer only use index if the first component of the combined index is in the selection criteria.

What if you have two separate indexes on these two columns? MySQL optimizer will try to [merge the indexes](http://dev.mysql.com/doc/refman/5.6/en/index-merge-optimization.html) or select one which it think will filter out more rows.

    SELECT * FROM user WHERE first_name = 'abc' OR last_name = 'xyz'

With the above statement, optimizer won't use any index, either it is a combined index on two columns `first_name` and `last_name` or one index on each column. There is a trick to that: 

    SELECT * FROM user WHERE first_name = 'abc' UNION ALL SELECT * FROM user WHERE last_name = 'xyz'

Use `EXPLAIN` we will have: 

    | id | select_type  | table      | type | possible_keys  | key            |
    |----|--------------|------------|------|----------------|----------------|
    |  1 | PRIMARY      | user       | ref  | first_name     | first_name     |
    |  2 | UNION        | user       | ref  | last_name      | last_name      |
    | NULL | UNION RESULT | <union1,2> | ALL  | NULL           | NULL         |

The optimizer will execute two SELECT statement, one PRIMARY and one UNION, and then UNION the result set. On each SELECT statement, it uses the respective index to retrieve rows. As a result, we achieve better performance than the previous statement, in which MySQL do a full table scan. 


## Is index always necessary? 

At the begining of this article, I have mentioned that most of the time, key look up is better than full table scan. There is, however, case when full table scan is better. When you have a small table(less than 10 entries), performing a full table scan is faster than key look up. Or when the result set constitutes a large part of the table (more than 30%), full table scan to fetch result rows is faster than key look up and fetch rows later.  

Fortunately, MySQL optimizer internally takes on the job of calculating the expenses by different approaches and choose the right one for you. It decides whether accessing by index will be more expensive than table scan or vice versa; which index to use among the available.  

When you think MySQL optimizer is not doing the right thing, you should run [ANALYZE](http://dev.mysql.com/doc/refman/5.6/en/analyze-table.html) on the table your query applies to. `ANALYZE` gives optimizer up-to-date statistical analysis of tables (size, indexes, etc...) thus, it has a better idea on how much resources is needed for each approach. If the optimizer still fails you after running `ANALYZE`, try [making an index hint](http://dev.mysql.com/doc/refman/5.6/en/index-hints.html) to it. You can suggest, force it to use or ignore an index.  

## What next?

So far we have shortly discussed on how to optimize MySQL query - SELECT statement - through the use of `EXPLAIN`. Other topics I want to extend around this theme are: 
 
*   Optimizing DML statement. 
*   Configuring system variables and memory usage.

Hope I can spend time on them soon. In the mean time, there are plenty of resources to explore on MySQL optimization. You can check out the [Optimization Chapter](http://dev.mysql.com/doc/refman/5.6/en/optimization.html) on MySQL Reference Manual as a start.

