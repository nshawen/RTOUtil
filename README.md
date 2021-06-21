# RTOUtil

Project to form a python package encapsulating the core workflows used by the Research Technologies and Outcomes lab to apply data science to wearables and healthcare.

Additional utilities code for RTO lab projects using jupyter notebooks.

Created by Nick Shawen
This project is licensed under the terms of the MIT license.

## Using in your project:

Example command line code when running in main project folder (not submodule folder)

* Adding this repository as a submodule

```
git add submodule https://github.com/nshawen/RTOUtil
```

* Pulling code when cloning a repository that uses this code (e.g. this package is already being used in the project, you just want to pull it in)

```
git submodule init
git submodule update
```

* Pulling future updates to the submodule version used in a project

```
git submodule update
```

* Check for changes to this repository and incorporate into your project

```
git submodule update --remote
```

## Contributing

If you have ideas for code that should be added to this repository for use in other projects, you can:

* Fork this repository, make your changes and send a pull request (https://docs.github.com/en/github/getting-started-with-github/fork-a-repo)
OR
* Contact nshawen to collaborate on this repo directly (best for lab members planning to make consistent updates across many projects). Best practice is to use branchs to test new features, then make a pull request to incorporate them into the master once ready.
