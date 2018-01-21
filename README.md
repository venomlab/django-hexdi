# django-hexdi

This is the project that integrates **hexdi** framework into Django.

Visit [github page](https://github.com/zibertscrem/hexdi) of **hexdi** project for use-cases and instructions.

Created for using with django-based applications.

# Installation

```bash
pip install django-hexdi
```

Keep in mind that we really recommend to use the same version of hexdi that django-hexdi has

# Usage

First step is to add `djhexdi` to your `INSTALLED_APPS` setting.

Imagine next project tree:

```
app_folder
|-->__init__.py
|-->services.py
|-->concrete_services.py
.....
|-->urls.py
|-->forms.py
|-->views.py

```

File services.py contains service class declarations and "interfaces".

File concrete_services.py contains implementations of services stored in services.py and binded using **hexdi** calls.

forms.py, views.py, and so on use services.py interfaces and inject these interfaces implementations using **hexdi** injections.
  
So, there are several ways to set up **hexdi** on Django for static or automatic implementations loading:

## Dummy strategy

This is the **default strategy** that does nothing on application startup. You really should use something other!

```python
HEXDI_STRATEGY = 'djhexdi.strategy.Dummy'
```

## Static strategy

This is the simplest and static strategy of implementations discovery using modules list that contain bindings.

Use next setting to set up this strategy:

```python
HEXDI_STRATEGY = 'djhexdi.strategy.Static'
```

Use the special setting to provide dotted path of modules where bindings are presented:

```python
HEXDI_MODULES_LIST = [
    'path.to.first.module',
    'path.to.second.module',
]
```

You can specify a module that contains this list:

```python
HEXDI_MODULE = '__hexdi__'
```

Use this discovery when you are sure that there is no other place with bindings and your dependency modules don't use hexdi, so on. 

## Fully automatic strategy

This is the dynamic strategy of modules finding which works on application startup.

Use next setting to set up this strategy: 

```python
HEXDI_STRATEGY = 'djhexdi.strategy.Auto'
```

By default, **hexdi** will search in packages that presented in `INSTALLED_APPS`.
But, you can also specify your special packages for searching using following setting:

```python
HEXDI_FINDER_PACKAGES = [
    'path.to.first.package',
    'path.to.second.package',
]
```

You can also specify a static modules to load it additionally if it is needed:

```python
HEXDI_MODULES_LIST = [
    'path.to.first.module',
    'path.to.second.module',
]
``` 

And you can specify a number of modules that should be excluded from loading:

```python
HEXDI_EXCLUDE_MODULES = [
    'path.to.first.excluded.module',
    'path.to.second.excluded.module',
]
```

Use this strategy if you can **rely on module-finder** or your dependencies are using **hexdi**, or something.

But keep in mind that **this strategy may slowdown your application startup** if you have a huge number of modules/dependencies.

## Pre-build automatic discovery with static loading

This is the best configuration for application that has a build process or same thing.

### Workflow explanation

Build process:

1. requirements installation
1. other build activities (migrations, caching, template building, etc.)
1. modules automatic discovery and storing results in py-file artifact

Run application:

1. application start
1. pre-searched artifact loading with modules list on application startup process

### Setup Django project 

Define setting for using static strategy:

```python
HEXDI_STRATEGY = 'djhexdi.strategy.Static'
```

Define a file where discovered modules will be stored:

```python
HEXDI_MODULE = '__hexdi__'
```

The best way is to use `__hexdi__` as HEXDI_MODULE value.

By default, **hexdi** will search in packages that presented in `INSTALLED_APPS`.
But, you can also specify your special packages for searching using following setting:

```python
HEXDI_FINDER_PACKAGES = [
    'path.to.first.package',
    'path.to.second.package',
]
```

You can also define modules that should be loaded additionally

```python
HEXDI_MODULES_LIST = [
    'path.to.first.module',
    'path.to.second.module',
]
```

### Set up build step

Use the special manage.py command for modules automatic discovery

If you have configured your Django project with `HEXDI_MODULE` setting then you can just apply following command:

```bash
python manage.py di_find --auto
```

If you want to specify some other module, just use -m option:

```bash
python manage.py di_find -m other.module.path --auto
```

**--auto** option is used for automatic creation of packages tree if not exists.

Use this strategy when you have too much dependencies to store all modules manually and if you have build process with controllable build steps.
That configuration allows you to have **fully automatic discovery** once while build process and then **quick application startup** with cached module paths. 

# All supported settings

List of built-in settings and it's description

- `HEXDI_STRATEGY` - Strategy for DI container bindings discovery used on application startup. Should be inherited from `djhexdi.strategy.AbstractStrategy` class. Default value `djhexdi.strategy.Dummy`;
- `HEXDI_FINDER_PACKAGES` - A list of packages(dotted paths). By default uses `INSTALLED_APPS` modules list. Used by `Automatic strategy` and `di_find` management command; 
- `HEXDI_MODULES_LIST` - A list of modules(dotted paths) that should be loaded on application startup. Used by `Static strategy` and `Automatic strategy`;
- `HEXDI_EXCLUDE_MODULES` - A list of modules that should be excluded from module-loading. Used by `Static loading` and `Automatic loading`;
- `HEXDI_MODULE_LIST_NAME` - A name of variable with modules list that should be presented in module(HEXDI_MODULE setting). Used by `Static strategy` and `di_find` management command;
- `HEXDI_MODULE` - A module path(dotted path) that contains a variable(name stores in HEXDI_MODULES_LIST_NAME) with list of module paths(dotted paths). Used by `Static strategy`, `Automatic strategy`, and `di_find` management command.
- `HEXDI_LOADER` - A string contained dotted path to a class that will be used as **module loader**. Default value `hexdi.loader.BasicLoader`
- `HEXDI_FINDER` - A string contained dotted path to a class that will be used as **module finder**. Default value `hexdi.finder.RecursiveRegexFinder`

# Custom strategy

If you have some other vision of startup loading strategy, then you are able to implement it.

Check module `djhexdi.strategy` for useful abstract classes and functions:
 
- function `load_modules` loads found or specified modules. Accepts modules list(dotted paths) as a first argument and modules to exclude(dotted paths) as a second argument. Uses loader specified in `HEXDI_LOADER` setting;
- function `find_modules` discover modules. Accepts packages list(dotted paths) to find as a single argument. Uses finder specified in `HEXDI_FINDER` setting;
- class `AbstractStrategy` is a very base abstract class that provides method `go` without arguments for doing some module-load staff on application startup. All other strategies should be inherited from that class.
- class `AbstractLoadModulesStrategy` is an abstract strategy inherited from `AbstractStrategy` and provides implemented method `go` and 2 other methods: discover_modules - abstract method that should return a modules list, get_excluded_modules - already implemented method that returns a list presented in `HEXDI_EXCLUDE_MODULES` setting.
- class `Static` is a ready-to-go strategy inherited from `AbstractLoadModulesStrategy` with implemented behaviour of static modules list(HEXDI_MODULES_LIST) loading and module loading(HEXDI_MODULE). You can inherit from that class and extend static loading with some other staff.
- class `Auto` is a ready-to-go strategy inherited from `Static` strategy and extended it with automatic discovery of modules to load.

Check module [hexdi.utils](https://github.com/zibertscrem/hexdi/blob/master/hexdi/utils.py) for useful functions   


