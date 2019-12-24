# Data Representation Project
Data Representation Big Project 2019

## G00190832 
## Peter McGowan

This project has been carried out as an assignment of the Data Representation module of the Higher Diploma In Data Analytics at GMIT.


### Contents
It consists of the following elements:
* mySQL database
* Python 'DAO' programme to access the mySQL database
* Python 'application' to run a Flask server
* Several html pages and associated JavaScript and css files as a user interface
* Other files i.e. config file and API key stored separately for security


## Python Anywhere
The project is hosted on PythonAnywhere at the following location:

[http://pmcg19.eu.pythonanywhere.com](http://pmcg19.eu.pythonanywhere.com)

Login Details are as follows:
* username: guest
* password: guest


## mySQL Database
The database is running on a mySQL server on PythonAnywhere. It consists of three tables:
* Houses;
* Areas;
* Users;|

### Houses
The house table schema is as follows:

| Field | Type         | Null | Key | Default | Extra          |    
|-------|--------------|:----:|:---:|:-------:|----------------|
| id    | int(11)      | NO   | PRI | NULL    | auto_increment |
| descr | varchar(250) | YES  |     | NULL    |                |
| beds  | int(5)       | YES  |     | NULL    |                |
| baths | float        | YES  |     | NULL    |                |
| area  | int(5)       | NO   | MUL | NULL    |                |
| price | int(11)      | NO   |     | NULL    |                |

The primary key is the id field, area is a foreign key (to the areas table).
Several fields have also been set to not allow null values.
Area is stored as an integer - this field is linked to the areas table, a SQL join can be carried out to extract the appropriate area for each house.

### Areas
The areas table schema is as follows:

| Field     | Type         | Null | Key | Default | Extra |
!-----------!--------------!:----:|:---:|:-------:|-------+
| id        | int(5)       | NO   | PRI | NULL    |       |
| name      | varchar(150) | NO   |     | NULL    |       |
| latitude  | float        | YES  |     | NULL    |       |
| longitude | float        | YES  |     | NULL    |       |

The id field in the primary key. It and the name column may not be null.

### Users
The users table schema is as follows:

| Field | Type        | Null | Key | Default | Extra          |
|-------|-------------|:----:|:---:|:-------:|----------------|
| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| uname | varchar(30) | NO   | UNI | NULL    |                |
| upass | varchar(50) | NO   |     | NULL    |                |
| level | varchar(10) | NO   |     | NULL    |                |

Again, the id field is the primary key. Unlike the other tables, none of the fields may be null, and the uname field must contain unique values.


## DAO
DAO stands for Data Access Object. The housePriceDAO.py file consists of a number of functions which access the database and perform CRUD operations. In some cases, these functions perform SQL joins in order to extract relevant area names for the houses.

In order to prevent issues with numbers of connections on PythonAnywhere, the DAO file sets a pool of connections and manages them.

It does not directly store the database login details - these are imported from another python file, config.py.

## Application
The main python file, application.py, runs a Flask server in a virtual environment. Its required packages are stored in requirements.txt.

It consists of a series of functions that pick up on database requests sent from JavaScript in the html files and perform actions such as:
* Page redirects
* Database CRUD operations
* Checks for user credentials

It uses a number of flask modules for convenience, including:
* jsonify: for creating JSON strings
* redirect: for return a redirect to a different URL
* render_template: uses template .html files to serve data to the user

## HTML
Three .html pages are included:
* login.html
* houseviewer.html
* mapviewer.html

The webpages are mainly styled using bootstrap, including the template located here: [https://startbootstrap.com/previews/small-business/], although this has been modified and extended. CSS and JavaScript files for this are included.

Additionally, the following items are included:
* custom.css: additional CSS added to modify the bootstrap template
* jQuery: The jQuery library is included for use of AJAX as well as a function used by the houseviewer.html page
* ajaxscripts.js: The AJAX functions created for this project have been included as a separate file here
* jeaflet.js: This is included with the mapviewer.html page for display of the map
* thunderforestAPIKey.js: This is imported separately (and included in the .gitignore file, therefore not uploaded to Github) for security


### Login Page
The login page takes in a user name and password and compares them against the users table in the database. If accepted, the user is redirected to the houseviewer page

### Houseviewer Page
This page extracts the houses table (and areas table) data to build a table of house in Galway. The table hides the id of each house, but displays all other data. The user can update or delete the existing entries, or create new ones. Selecting update or create will hide the table and show a form instead.

The user input form restricts input for to certain datatypes. Once it is submitted, a jQuery function is run to refresh the table displayed - this ensures that a fresh extract is retrieved from the database.

### Mapviewer Page
There are two basic elements on this page. Firstly, leaflet.js is used to display a tiled map from the [Thunderforest](https://www.thunderforest.com/) API, specifically the Neighbourhood map, styled appropriately to show areas of Galway City. This API requires a Key for authentication, which is retrieved from a JavaScript file stored on the server.

The second element of this is a table showing areas of Galway. Although the Latitude and Longitude of each area is included, they are hidden along with the area ID. A button is included for each area, when clicked it displays a marker on the area's coordinates. Each button click clears the previous marker.