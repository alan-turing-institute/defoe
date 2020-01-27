/* Reward a place for being within a given radius of some lat/long 
   or within a bounding box. */

#include <stdlib.h>
#include <math.h>

#include "lx.h"
#include "resolve.h"

void usage(int status)
{
    fprintf(stderr, "usage: locality [-c] lat long radius score <placename_file\n"
	            "       locality -b west north east south score <placename_file\n");
    exit(status);
}

int main(int argc, char **argv)
{
    Document doc;
    Placename pn;
    Place p;
    int box = 0, good;
    double lat, lon, radius;
    double score = 0;
    double w, n, e, s;
    int i, j;

    if(argc == 5 ||
       (argc == 6 && strcmp(argv[1], "-c") == 0))
    {
	if(argc == 6)
	    argv++;
 	lat = atof(argv[1]);
	lon = atof(argv[2]);
	radius = atof(argv[3]);
	score = atof(argv[4]);
    }
    else if(argc == 7 && strcmp(argv[1], "-b") == 0)
    {
	box = 1;
	w = atof(argv[2]);
	n = atof(argv[3]);
	e = atof(argv[4]);
	s = atof(argv[5]);
	score = atof(argv[6]);
    }
    else
	usage(2);

    doc = read_document(stdin, 0, 0);

    for(i=0; i<LTVectorCount(doc->placenames); i++)
    {
	pn = doc->placenames[i];

	for(j=0; j<LTVectorCount(pn->candidates); j++)
	{
	    p = pn->candidates[j];
	    if(box)
		/* XXX won't work around 180 e/w */
		good = (p->latitude >= s && p->latitude <= n &&
			p->longitude >= w && p->longitude <= e);
	    else
		good = (distance(p->latitude, p->longitude, lat, lon) < radius);
	    set_attr_double(p, "locality", good ? score : 0);
	}
    }

    write_document(stdout, doc);

    return 0;
}

