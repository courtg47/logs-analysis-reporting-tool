# Logs Analysis Reporting Tool Project

This project is a reporting tool which analyzes the logs in a PostgreSQL database of a fictional newspaper site. The reporting tool 
analyzes the database to answer three questions and display the results on the command line:

1)	What are the three most popular articles of all time?
2)	Who are the most popular article authors of all time?
3)	On which days did more than 1% of requests lead to errors?

This project does not take any input from the user. Instead, it will connect to the database, use SQL queries to analyze the log data, 
and print out the answers to the above questions.  This project satisfies the third project for Udacity’s Full Stack Web Developer 
program.

## Technologies utilized

This project is written in Python 3.7 and queries a PostgreSQL database which resides on a Virtual Machine. Python DB-API is 
utilized to connect to and query the database. 

## Installation

To use this project, first install the below programs:

### Python 3:
Download the [latest Python version 3](https://www.python.org/downloads/), based on your operating system, and install on your machine. 

### VirtualBox: 
[Install the platform package](https://www.virtualbox.org/wiki/Downloads) for your operating system. You do not need the extension pack
or the SDK. You also do not need to launch VirtualBox after installation.

### Vagrant:

[This program](https://www.vagrantup.com/downloads.html) will download a Linux operating system and run it inside the virtual machine. 
Windows users may be asked to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

### Download the Vagrantfile [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f73b_vagrantfile/vagrantfile). 
Put this file in a new directory on your computer. Using your terminal, `cd` into that directory, then run the command `vagrant up`.  
Let it run, this will take a few minutes.
 
Now you’ll have a PostgreSQL server running in a Linux virtual machine. 

## Configuration

* Logging into the Virtual Machine: using your terminal or git bash, `cd` into the `vagrant` directory and run the command 
`vagrant ssh`.  
* Next, run the command `cd /vagrant` then `ls` and you will see the Vagrantfile you downloaded.
* Download the [data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
* Unzip the file after downloading. The file inside it is called `newsdata.sql`.  Put this file into the vagrant directory, 
  which is shared with the VM.
* To load the data: `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`

Running the above command will connect to your installed DB server and execute the SQL commands in the downloaded file. 

### If you get the below error: 

```psql: FATAL: database "news" does not exist
psql: could not connect to server: Connection refused
```

This means the DB server is not running or is not set up correctly. This can happen if you have an older version of the VM configuration. To continue, download the VM configuration again into a fresh directory and start from there.
Pull this repo onto your computer and place the Reporting directory in the same directory as the Vagrantfile.

## Create a View

Before running this program successfully, you must create a view within the news database. This view will be necessary to answer 
the third report question correctly. To create the view, `cd` into the `Vagrant` directory, `vagrant ssh` to login, then use the 
following commands:

`cd /vagrant`

`psql news`

```CREATE VIEW daily_errors AS
SELECT to_char(time::date, 'FMMonth DD, YYYY') AS date,
COUNT(*) FILTER(WHERE status LIKE '%4%') AS errors,
COUNT(time::date) AS views
FROM log
GROUP BY date
ORDER BY errors DESC;
```

Run `\dv` to confirm that the new view `daily_errors` was created. `\q` to quit.

## Running the program

* `cd` into the directory containing the Vagrantfile, then run `vagrant ssh` to login to the Virtual Machine. 
* `cd` into `/vagrant`
* `cd` into `Reporting`
* Run the python file reporting.py (`python reporting.py`)

You should then see the output from the report display in your terminal/command line. You have completed running the program.

