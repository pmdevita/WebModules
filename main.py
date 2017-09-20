from venv_manager import venv
v = venv("int-flask", ["flask", "watchdog", "apscheduler"])

from flask import Flask, redirect, request
import os
import sys
import importlib
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DEBUG = False

module_path = "modules"
template_path = "templates"

modules = {} # route: module object
module_filenames = {} # filename: route

app = Flask(__name__,  template_folder=template_path)
sys.path.append(module_path)


def _load_module(filename):
    print("Loading {}... ".format(filename), end="")
    try:
        imp_module = importlib.import_module(filename).Module
        temp_module = imp_module()
    except Exception as e:
        print("Error\n{} {}"
              .format(type(e), e))
        return
    if not modules.get(temp_module.route, None):
        if temp_module.route:
            modules[temp_module.route] = temp_module
            module_filenames[filename] = temp_module.route
            print("Done")
        else:
            print("Empty module?")
    else:
        print("Duplicate route!")


def _reload_module(filename):
    print("Reloading {}... ".format(filename), end="")
    try:
        pimp_module = importlib.import_module(filename)
        imp_module = importlib.reload(pimp_module).Module
        temp_module = imp_module()
    except Exception as e:
        print("Error\n{} {}"
              .format(type(e), e))
        _remove_module(filename)
        return

    if temp_module.route:
        # if route previously exists and has changed then unregister old one
        if filename in module_filenames:
            if module_filenames.get(filename, None) != temp_module.route:
                modules.pop(module_filenames[filename])
                module_filenames[filename] = temp_module.route
        else:
            module_filenames[filename] = temp_module.route
        modules[temp_module.route] = temp_module
        print("Done")
    else:
        print("Empty module?")

def _remove_module(filename):
    print("Removing {}...".format(filename), end="")
    name = module_filenames.pop(filename)
    modules.pop(name)
    print("Done")


class Update(FileSystemEventHandler):
    def on_created(self, event):
        p = Path(event.src_path).parts[1]
        if p[-3:] == ".py":
            # print(event.src_path, "Created!", p)
            _load_module(p[:-3])

    def on_modified(self, event):
        p = Path(event.src_path).parts[1]
        if p[-3:] == ".py":
            # print(event.src_path, "Modified!", p)
            _reload_module(p[:-3])

    def on_deleted(self, event):
        p = Path(event.src_path).parts[1]
        if p[-3:] == ".py":
            # print(event.src_path, "Deleted!", p)
            _remove_module(p[:-3])

# setup scanner
handler = Update()
observer = Observer()
observer.schedule(handler, "modules")

@app.route("/")
def mainpage():
    page = ""
    for module in modules:
        page = page + str(modules[module])
    return page

@app.route("/<path:route>")
def routing(route):
    if request.method == "GET":
        args = request.args
    elif request.method == "POST":
        args = request.form
    path = route.split("/")
    module = modules.get(path[0], None)
    if module:
        try:
            return module.run(path, request.method, args)
        except Exception as e:
            print("Module {} could not be run due to error\n{} {}"
                  .format(i[:-3], type(e), e))

    return redirect("/")


if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or DEBUG == False:
    observer.start()
    modules = {}
    for i in os.listdir("modules"):
        if i[-3:] == ".py":
            _load_module(i[:-3])

if __name__ == "__main__":
    app.debug = DEBUG
    app.run()
    observer.stop()
else:
    application = app
