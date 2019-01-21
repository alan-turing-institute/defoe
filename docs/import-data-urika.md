# Import data into Urika

Urika compute nodes have no network access and so cannot remote datasets. All data should be copied into your home directory, and then copied into a directory on Lustre, a high-performance parallel filesystem connected to Urika.

## Transfer data into Urika

To transfer data into Urika, see [Data transfer to and from the Turing's Cray Urika-GX service](https://ati-rescomp-service-docs.readthedocs.io/en/latest/cray/data-transfer.html) in the [Alan Turing Institute Research Computing Service](https://ati-rescomp-service-docs.readthedocs.io/en/latest/index.html) documentation.

## Move data into Lustre

Once your data is in your directory on Urika, can put your data into Lustre as follows:

Create directory on Lustre:

```bash
mkdir -p /mnt/lustre/<your-urika-username>/<directory-name>
```

Set file permissions so that no other user can access your data:

```bash
chmod -R go+rwx /mnt/lustre/<your-urika-username>
```

Move your data from your home directory into your Lustre directory. Alternativerly, you can move the data.
