# Web Modules v.8



Web Modules is a framework for quickly and easily making
* small test websites
* server scripts that need a UI

Website Modules dynamically loads modules so you do not have to reload the entire
WSGI solution, allowing for quick testing and deployment. It also provides a job scheduler interface (coming soon!).

Example cases:
* Used to quickly develop a script that would cache and display the latest advisory
for Hurricane Irma in case internet dropped.

Simple example module:

    from BaseModule import BaseModule

    class Module(BaseModule):
        name = "A module"
        route = "module"
        def run(self, route:list, method:str, args:dict):
            return "module is up and running!"

An example module is provided.

#### Changelog

9/15/17 - v.8

* Initial Release


#### Future
* Add template and resource to example
* Add job scheduler
* Make test cases