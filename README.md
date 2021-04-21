# warriorframework
[warriorframework.org](http://warriorframework.org)

Warrior Framework is an open source automation framework designed to enable anyone to automate their testing, processes, and repetitive tasks by simplifying the complex process of building an automation infrastructure. As a keyword and data driven framework, Warrior’s infrastructure is built to maximize on re-usability of  built in keywords. In addition, Warrior’s app based platform provides the users with native apps to easily implement their automation needs, while providing the user with the ability to customize their own workflow apps.

#### Prerequisites

###### Linux
Get VirtualBox [here](https://www.virtualbox.org/wiki/Downloads)<br/>
Get Linux Image [here](https://www.ubuntu.com/download/desktop?)<br/>
Follow these [Instructions](https://www.lifewire.com/run-ubuntu-within-windows-virtualbox-2202098) to get a Virtual Machine set up on your system

###### Python 3.6+ &amp; pip
Follow this [tutorial](http://thelazylog.com/install-python-as-local-user-on-linux/) to get the Python you need.

#### Procedure to install warrior framework
###### Create and Activate virtual environment<br/>
   `python3 -m venv warriorenv`<br/>
   `source warriorenv/bin/activate`<br/>   
###### Procedure to install warrior pip module (from pypi server)<br/>
1. Install warriorframework, This installs only warrior without any warrior modules.<br/>
    1. Latest version warriorframework from PyPI server<br/>
           `pip install warriorframework`<br/>
    2. Specfic Version warriorframework from PyPI Server<br/>
	   `pip install warriorframework==4.3.0`<br/>
    3. Uninstall warriorframework<br/>
	   `pip uninstall warriorframework`<br/> 
2. Install required warrior modules.<br/>
    1. Required warrior modules can be installed from PyPI Server.<br/> 
       For Example, Install only warriorcli module if you have only cli automation tasks<br/>
       `pip install warriorcli`<br/> 
       `pip install warriornetconf`<br/> 
       `pip install warriorsnmp`<br/> 
       `pip install warriorgnmi`<br/> 
       `pip install warriorcloudshell`<br/> 
       `pip install warriorrest`<br/> 
       `pip install warriorselenium`<br/> 
       `pip install warriorkafka`<br/> 
       `pip install warriornetwork`<br/> 
       `pip install warriorserver`<br/> 
       `pip install warriormongo`<br/> 
       `pip install warriordemo`<br/> 
       `pip install warriorfile`<br/> 
       `pip install warriorciregression`<br/> 
       `pip install warriormicroapps`<br/> 
       `pip install warriorwapp`<br/> 
    2. Specfic Version warrior module from PyPI Server<br/>
	   `pip install warriorcli==1.0.0`<br/> 
3. Install warrior framework and all modules<br/>
        `pip install warriorframeworkallmodules`

###### Procedure to install warrior from git (this step is not required if you have installed warrior from pypi server)<br/>
We strongly recommend getting the latest released version.<br/>

1. Get the Repository<br/>
`git clone https://github.com/warriorframework/warriorframework_py3.git`<br/>

2. Go into warriorframework_py3 Directory<br/>
`cd warriorframework_py3`<br/>

3. Get List of Versions Available<br/>
`git tag --list" command`<br/>

Output:<br/>
`warrior-4.3.0`<br/>
`warrior-4.2.0`<br/>
`warrior-4.1.0`<br/>
`warrior-4.1.0-beta`<br/>
`warrior-4.0.0-beta`<br/>
`warrior-3.4.0`<br/>
`warrior-3.3.0` <br/>
`warrior-3.2.0`<br/>

4. Check the Current Version You Are At<br/>
`git branch`<br/>

Output:

`\* master`<br/>
`\* indicates the active version.`<br/>
`In the above example master is the active version.`<br/>
`If the active version is master it means you are not using a standard release version of warriorframework and hence it may not be a stable tested version.`<br/>

5. Get A Specific Version from master<br/>
`git checkout warrior-4.3.0`<br/>

Output:<br/>

`Note: checking out 'warrior-4.3.0'.`

`You are in 'detached HEAD' state. You can look around, make experimental changes and commit them, and you can discard any commits you make in this state without impacting any branches by performing another checkout.`

`If you want to create a new branch to retain commits you create, you may do so (now or later) by using -b with the checkout command again. Example:`

`git checkout -b new_branch_name`

`HEAD is now at 2bba292... Merge pull request #234 from warriorframework/release-warrior-4.1.0`

6. Verify the Active Version. <br/>
`git branch`<br/>

Output:<br/>

`\* (HEAD detached at warrior-4.3.0)` <br/>
`master` <br/>

`\* indicates the active version.`<br/> 

7. Install requirements (make sure you are in virtual environment)<br/>
  `pip install -r requirements.txt`<br/>
  
   Python Packages used by warriorframework<br/>
	pexpect<br/>
	requests<br/>
	selenium<br/>
	pysnmp<br/>
	kafka-python<br/>
	pyvirtualdisplay<br/>
	pycryptodome<br/>
	paramiko<br/>
	lxml<br/>
	xlrd<br/>
	cloudshell-automation-api<br/>
	pytest<br/>
	openpyxl<br/>
	pandas<br/>
	configobj<br/>
###### Execute Warriormigrate command (this is required if custom lib is using warrior imports)<br/>
 1. pip installation<br/>
   `Warriormigrate -pkgs_list all`<br/>
   `Warriormigrate -pkgs_list warriorcli,warriornetconf`<br/>
   (or) <br/>
 2. git installation <br/>
   `./warrior/Warriormigrate -pkgs_list all` (to use all inbuilt warrior keywords, utils in custom lib)<br/>
   `./warrior/Warriormigrate -pkgs_list warriorcli,warriornetconf` (to use only cli, netconf keywords, utils in custom lib)<br/> 
   
###### Execute scripts<br/>
 1. pip installation<br/>
    `Warrior -pythonpath <customlibpath> <testcase.xml>`<br/>
    (or)<br/>
 2. git installation<br/>
    `./warrior/Warrior -pythonpath <customlibpath> <testcase.xml>`<br/>
   
