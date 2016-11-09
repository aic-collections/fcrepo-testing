# FCREPO Backup/Restore Test Scripts

Scripts to load resources to Fedora and that can check the status of those resources.  These are useful when testing the backup/restore feature of Fedora.

## Getting Started

### Prerequisites

Python3 (tested with 3.5)

### Installing

Assuming a virtualenv:

```
pip install -r requirements.txt
```

### Configuring

There are sample `config` files in the `config` directory.  If necessary, copy and modify one to fit your environment. The properties are largely self-explanatory, but a few notes:

- `[fcrepo][base]`: The value points to the container into which test resources will be loaded. This should end in a slash.
- `source_relations`: Leave alone. It is a carryover from earlier code.
- `source_data`: There are two options.  A file with 50000 resources or one with 5000 resources.  The larger file takes a little longer to process, but should ensure you can use a `multiplier` up to and including 190.
- `multiplier`: The number of resources to save under each of 256 pairtrees.  Must be at least 1 and can be up to 190 (or you will need more than the 50,000 resources in the sample data).
- `load_binary_data`: 1 or 0. If '1', then, in addition to loading an RDF resoruce, a binary file will be saved for each RDF resource.  This effectively doubles the load.
  
### Running

There are two ways to run these scripts, one more manual than the other.

The more or less automated way is to:

```
./backup-restore --config config/{file}.yaml
```

This method should only be used when it is sufficient to test the backup and restore functionality on the *same* version of Fedora and the *same* Fedora installation.  For example, if you are testing version FCREPO 4.6.1 on localhost, `backup-restore` will load to FCREPO 4.6.1 on localhost, verify the load, backup the repository on localhost, restore the repository to the same, and verify the contents.  It is not made to test a migration from a distinct Fedora installation to another.

The scripts can be run in a more manual way too.

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

Note the location of the backed up repository in the response.  Using that information, restore the repository:
```
curl -i -X POST -d {/path/to/backup/} http://{FCREPO_HOST}:{FCREPO_PORT}/fcrepo/rest/fcr:restore
```

You should get a `204 No Content` response.  Re-run the verification script:
```
./test-gets --config config/localhost.yaml --data source-data/loaded-uris/{previously_saved_file}.txt
```

The result should be all "200 OK" messages.  If you see 500s, something went wrong somewhere with the backup/restore process.
