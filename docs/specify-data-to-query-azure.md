# Specify Azure data to query

**Note:** This information applies to Alan Turing Institute projects using Azure (for example, Living with Machines)

**Note:** This information is not applicable if using Urika.

If running queries on datasets in the Alan Turing Institute Azure storage, then you need to configure your connection to Azure. For example:

```bash
export BLOB_ACCOUNT_NAME="<AZURE-ACCOUNT-NAME>"
export BLOB_SAS_TOKEN="<AZURE-SAS-TOKEN>"
export BLOB_CONTAINER_NAME="<AZURE-BLOB-CONTAINER-NAME>"
```

Paths in the data file need to be prefixed with `blob:`, for example:

```
blob:book37.zip
blob:000206133_0_1-1178pgs__1023547_dat.zip
```

## Living with Machines configuration

For configuration for Living with Machines datasets see [Azure storage access](https://github.com/alan-turing-institute/Living-with-Machines-code/wiki/Azure-storage-access) (project members only)
