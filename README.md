# FCREPO Backup/Restore Test Scripts

Scripts to load resources and that can check the status of those resources.  Otherwise, testing the FCREPO backup/restore capability is mostly manual.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python3 (tested with 3.5)

### Installing

Assuming a virtualenv:

```
pip install -r requirements
```

There are is a `config` file.  If necessary, copy and modify one to fit your environment.

## Running

Load some resources:

```
./load-resources --config config/localhost.yaml 
```

The above command will save a list of loaded URIs to the source-data/loaded-uris/ directory to a file named with a datetime string indicating when the run finished.  

Verify them.  This will perform a simple GET on each loaded resource:
```
./test-gets --config config/localhost.yaml --data source-data/loaded-uris/{previously_saved_file}.txt
```

Assuming the response codes for the resources are all 200s, perform a backup of the repository.
```
curl -i -X POST http://{FCREPO_HOST}:{FCREPO_PORT}/fcrepo/rest/fcr:backup
```

Note the location of the backed up repository in the response.  

You can try to `restore` the repository from the backup just created, but I've *always* had to use the [Fcrepo upgrade utils](https://github.com/fcrepo4-exts/fcrepo4-upgrade-utils/releases/) on the backup prior to it succeeding.

```
java -jar {frepo_upgrade_utils.jar} {/path/to/backup/}
```

Then restore the repository:
```
curl -i -X POST -d {/path/to/backup/} http://{FCREPO_HOST}:{FCREPO_PORT}/fcrepo/rest/fcr:restore
```

You should get a `204 No Content` response.  Re-run the verification script:
```
./test-gets --config config/localhost.yaml --data source-data/loaded-uris/{previously_saved_file}.txt
```

If you see 500s, something went wrong somewhere.
