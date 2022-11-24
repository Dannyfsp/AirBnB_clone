#!/usr/bin/python3
''' The console module '''

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    ''' The HBNB console class '''

    prompt = '(hbnb) '
    __classes = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review"
    }

    def emptyline(self):
        ''' an empty line + ENTER shouldn’t execute anything '''
        pass

    def default(self, arg):
        ''' Default behavior for cmd module when input is invalid '''
        argdict = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy
        }
        args = arg.split('.')
        if len(args) == 2:
            command = args[1][:-1].split('(')
            if len(command) == 2:
                call = "{} {}".format(args[0], command[1])
                if command[0] in argdict:
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        ''' Quit command to exit the program '''
        return True

    def do_EOF(self, arg):
        ''' EOF signal to exit the program '''
        print()
        return True

    def do_create(self, arg):
        ''' Usage: create <class>
        Create a new class instance and print its id.
        '''
        if not arg:
            print("** class name missing **")
        elif arg not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj = eval(arg)()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        ''' Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        '''
        objdict = storage.all()
        args = parse(arg)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(args[0], args[1])])

    def do_destroy(self, arg):
        ''' Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id.
        '''
        objdict = storage.all()
        args = parse(arg)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in objdict:
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(args[0], args[1])]
            storage.save()

    def do_all(self, arg):
        ''' Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        '''
        objdict = storage.all()
        args = parse(arg)

        if len(args) == 0:
            print([str(v) for v in objdict.values()])
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in objdict.items()
                  if k.split('.')[0] == args[0]])

    def do_update(self, arg):
        ''' Usage: update <class> <id> <attribute name> <attribute value>
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair.
        '''
        objdict = storage.all()
        args = parse(arg)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in objdict:
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            obj = objdict["{}.{}".format(args[0], args[1])]
            if hasattr(obj, args[2]):
                type_attr = type(getattr(obj, args[2]))
                setattr(obj, args[2], type_attr(args[3]))
            else:
                setattr(obj, args[2], args[3])
            obj.save()

    def do_count(self, arg):
        ''' Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        '''
        objdict = storage.all()
        args = parse(arg)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            count = 0
            for k in objdict.keys():
                if k.split('.')[0] == args[0]:
                    count += 1
            print(count)


def parse(arg):
    args = arg.split()
    args_stripped = []
    for a in args:
        a.strip()
        a = a.strip('\"')
        args_stripped.append(a)
    return args_stripped


if __name__ == '__main__':
    HBNBCommand().cmdloop()
