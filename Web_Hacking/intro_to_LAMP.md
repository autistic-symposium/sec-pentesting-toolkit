# Getting started with LAMP and CodeIgniter 


LAMP is an acronym for a model of web service solution stacks: Linux, the Apache HTTP Server, the MySQL relational database management system, and the PHP programming language.

## Building a MySQL Database

We will use a web interface to access data in our database:

* Login with your root login/password (set in the installation above): ```http://localhost/phpmyadmin```.
The left-hand column contains a list of all of the databases you currently have.

 - mysql: contains information about the MySQL database server.
 - information_schema: contains information about all of the other databases on your computer.

* In the Databases interface you are presented with a list of all of the databases.
* Above that list there should be a form labeled “Create new database” with a text field.
* Create tables within. Chose the types of your data. Every table should always have an id column (auto-incrementing integer, meaning that each new record will be automatically assigned an id value, starting at 1). You can do this by selecting A_I checkbox.
* Add some data (using insert). The database is located at 
```/var/lib/mysql```.

### MySQL Query Basis

Selecting items:
```
Retrieve all of the records (* means columns):
SELECT * FROM db_name;
Select only some columns:
SELECT col1, col2 FROM db_name;
Select only some values from some column:
SELECT * FROM db_name WHERE col1 = 'item';
Select the first 10 items:
SELECT * FROM cars WHERE make = 'Porsche' LIMIT 10
```

Inserting an item:
```
INSERT INTO db_name (col1, col2, col3) VALUES ('item1', 'item2', 'item3')
```

Updating an item:
```
UPDATE db_name SET col1 = 'item' WHERE col2 = 'item2' AND col3='item3'
```

Deleting items:
```
DELETE db_name WHERE col1 = item"
```

## PHP Basics

Variables:

```
<? php 
$result = 4*8; 
?>
Comments with / or ./* */.
Print function:
<? php
echo "that's a print";
?>
```

Functions:
```
<? php
function print_this($name){
 echo 'Print this ' . $name . '.';
 return 'nice printing';
}
extra_print = print_this('aaaaa');
print(extra_print);
?>
```

When a PHP file is accessed, all of its functions are initialized before any of the other lines of code are executed. As long as a function is defined in the same file, it can be called from anywhere within that file.

The scope of a variable refers to the domain within which it can be referenced. In PHP, any variables initialized and contained within a function itself are only available within that function.

### Arrays

Creating an empty array:

```
<? php $new_array = array(); ?>
```

Adding elements:
```
<? php $new_array[] = 1; $new_array[] = 5; ?>
```

Creating an array with values already:
```
<? php $other_array = array(1,2,3); ?>
```

In PHP, arrays are like dictionaries:. If you add item likes above, it will increment from 0. You can also give the key:
```
<? php $dictionary['dog'] = 1; ?> echo $dictionary['dog'];
```

Multi-arrays:

```
$cars = array
 (
 array("Volvo",22,18),
 array("BMW",15,13),
 array("Saab",5,2),
 array("Land Rover",17,15)
 );
```

Loop foreach:

```
<? php
foreach ($array_number as $variable_representing_current_item){
}
?>
```

Loop for:
```
<?
$other_array = []
for ($i; $i<4; $i++){
$other_array[] = $i;
} ?>
```

## The Model-View-Controller Pattern (MVC)

In a high level, the flow of a web app is:

* User request to view a certain page by typing a URL in the browser.
* The app determines what needs to be displayed.
* The data required for the page is requested and retrieved from the database.
* The resulting data is used to render the page's display to the user.
* The MVC structure is based on the presence of 3 main components: models, views, and controllers.

### Models: Representing the Data Object

Responsible for communicating with the database. Composed of two parts:

* fields: Responsible for representing the various pieces of data within an object (the information within the database).
* methods: Provide extra functionality within our models. Allow the manipulation of the model's initial information or perform additional actions related to the data.

### Controllers: Workhorses

Determine what objects to retrieve and how to organize them.

Handle user request, retrieve proper information, and pass it to the proper view.

Different request is handled by different controller actions.

### Views: What the User Sees

Responsible for the presentation layer, the actual visual display.

Each individual page within a web app has its own view.
Views contain HTML code and PHP (if this is the backend language) to inject objects' information, passed to the view via a controller.

A simplified version of Facebook profile view:
```
<section id="personal_info"> <?php // some code ?> </section> <section id="photos"> <?php // some code ?> </section>
```

## Frameworks

The basis/foundation of your web app.

For PHP, we can download CodeIgniter, rename to our project name, copy it to the /var/www folder, and open it in the localhost/folder. We can modify the files for our app now.

If you get the 403 forbidden error, check the permissions and then type:
```
restorecon -r /var/www/html
```
(restorecon is used to reset the security context (type) (extended attributes) on one or more files).

The user guide can be seen at 
```http://localhost/APP_NAME/user_guide/```

### CodeIgniter Basics

The system folder contains all of the inner-working.
The application folder is where all the code specific to our app will live, include models, controllers, and view.

Controllers (```application/controllers/welcome.php```)
The welcome class is inherent from the CI_Controller class.

An index refers to a main/default location.
The index action is responsible for loading the view that renders the welcome message:
public function index() { $this->load->view('welcome_message'); }
In the case of controllers, each action is frequently associated with a URL.

The ```'welcomemessage'``` view is at ```applications/views/welcomemessage.php```.

### Routes

The way that our web app knows where to direct our users, based on the URLs they enter, is by establishing routes. Routes are a mapping between URLs and specific controller actions.

We can configure routes at ```application/config/routes.php```:
```
$route['desired-url-fragment'] = "controller-name/action-name”;
```
Some routes work automatically: you can reference any controller action using the following URL format:
```http://localhost/APP_NAME/index.php/[controller-name]/[action-name]```

For example:
```http://localhost/APP_NAME/index.php/welcome/index/```

### Configuring our app to use the Database

CI has built-in support for interacting with a database.
In our application, the database configuration file is store at application/config/database.php

To connect our app to the MySQL database, update this file to:

```
$db['default']['hostname'] = 'localhost';
$db['default']['username'] = 'root';
$db['default']['password'] = '<your-root-password>';
$db['default']['database'] = '<database-name-from-before';
```

To have access to the database functionality throughout the entire web app, auto-load the database library by changing the file ```application/config/autoload.php``` with:
```
$autoload['libraries'] = array('template', 'database'); $autoload['libraries'] = array('database');
Check if the page is still working fine 
($autoload['libraries'] = array('template', 'database'); does not work yet).
```

### Models

Each model starts the same, as they intend to serve the same general function.

We create a new file in application/models folder named todomodel.php with the code:
```
<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed'); 
class Todomodel extends CIModel {
function _construct() {
parent::_construct();
} 
```

The second responsibility of models is to interact with our database. We need to implement a way for our todomodel to retrieve all of the todos in our database. We add a getallentries function bellow the constructor:
```
function get_all_entries() { //$query = $this->db->get('todos'); $query = $this->db->order_by('order','ASC')->get('todos'); $results = array(); foreach ($query->result() as $result) { $results[] = $result; } return $results; }
```

In this snippet, we query our database by order, using ascending order.


---
Enjoy! This article was originally posted [here](https://coderwall.com/p/5ltrxq/lamp-and-codeigniter).

