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

###### django
[Instructions](https://docs.djangoproject.com/en/2.0/faq/install/#faq-python-version-support) for Django Installation

###### xmltodict
`pip install xmltodict`

\*We are working hard to remove this dependency

###### Other Optional Python Packages

All the packages mentioned below are optional (i.e. their need depends on your usecase. If you are just trying out WarriorFramework, you may not need any of them). All these packages can be installed via pip.

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

#### Clone warriorframework

We strongly recommend getting the latest released version.

###### Get the Repository
`git clone https://github.com/warriorframework/warriorframework_py3.git`

###### Go into warriorframework_py3 Directory
`cd warriorframework_py3`

###### Get List of Versions Available
`git tag --list" command`

Output:

`warrior-4.1.0`<br/>
`warrior-4.1.0-beta`<br/>
`warrior-4.0.0-beta`<br/>
`warrior-3.4.0`<br/>
`warrior-3.3.0` <br/>
`warrior-3.2.0`<br/>

###### Check the Current Version You Are At
`git branch`

Output:

`\* master`<br/>
`\* indicates the active version.`<br/>
`In the above example master is the active version.`<br/>
`If the active version is master it means you are not using a standard release version of warriorframework and hence it may not be a stable tested version.`<br/>

###### Get A Specific Version from master
`git checkout warrior-4.1.0`

Output:

`Note: checking out 'warrior-4.1.0'.`

`You are in 'detached HEAD' state. You can look around, make experimental changes and commit them, and you can discard any commits you make in this state without impacting any branches by performing another checkout.`

`If you want to create a new branch to retain commits you create, you may do so (now or later) by using -b with the checkout command again. Example:`

`git checkout -b new_branch_name`

`HEAD is now at 2bba292... Merge pull request #234 from warriorframework/release-warrior-4.1.0`

###### Verify the Active Version. <br/>
`git branch`

Output:

`\* (HEAD detached at warrior-4.1.0)` <br/>
`master` <br/>

`\* indicates the active version.`

###### Switch Versions (Eg: current=warrior-3.4.0, switch to warrior-4.0.0-beta) <br/>

`git checkout warrior-4.1.0`

Output:

`Previous HEAD position was 2bba292... Merge pull request #234 from warriorframework/release-warrior-4.1.0`<br/>
`HEAD is now at b3bad2e... Update version.txt`


