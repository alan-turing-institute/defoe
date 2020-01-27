/* reward a place for being near a (presumably correct) known grid reference */

#include <stdlib.h>
#include <math.h>

#include "lx.h"
#include "resolve.h"
#include "gridref.h"

void do_gridrefs(LTVector(Placename, placenames));
void dummy_score(Placename pn);

void usage(int status)
{
    fprintf(stderr, "usage: known-gridref <placename_file\n");
    exit(status);
}

int main(int argc, char **argv)
{
    Document doc;

    if(argc != 1)
	usage(2);

    doc = read_document(stdin, 0, 0);

    do_gridrefs(doc->placenames);

    write_document(stdout, doc);

    return 0;
}

void do_gridrefs(LTVector(Placename, placenames))
{
    int i, j;
    Placename pn;
    Place p;
    char *err;
    double E, N, lat, lon, d, score;
    Char *gr;
    char *gridref;

    for(i=0; i<LTVectorCount(placenames); i++)
    {
	pn = placenames[i];

	if(LXGetAttributeValue8(pn->elem, "", "known-lat") &&
	   LXGetAttributeValue8(pn->elem, "", "known-long"))
	{
	    lat = get_attr_double(pn, "known-lat");
	    lon = get_attr_double(pn, "known-long");
	}
	else
	{
	    gr = get_attr_string(pn, "known-gridref");
	    if(!gr)
	    {
		dummy_score(pn);
		continue;
	    }
	    gridref = LTStrdupC8(gr);

	    if((err = gridref_to_nums(gridref, &E, &N)) != 0)
	    {
		fprintf(stderr, "bad grid reference <%s>: %s\n", gridref, err);
		dummy_score(pn);
		continue;
	    }

	    en_to_wgs84(E, N, &lat, &lon);
	    lat = lat * 180 / M_PI;
	    lon = lon * 180 / M_PI;

	    set_attr_double(pn, "known-lat", lat);
	    set_attr_double(pn, "known-long", lon);
	}

//	fprintf(stderr, "%f %f\n", E, N);
//	fprintf(stderr, "%f %f\n", lat, lon);

	for(j=0; j<LTVectorCount(pn->candidates); j++)
	{
	    p = pn->candidates[j];

	    d = distance(p->latitude, p->longitude, lat, lon);
//	    fprintf(stderr, "%f\n", d);

	    if(d < 1.0)
		score = 1.0;
	    else if(d < 5.0)
		score = 0.8;
	    else if(d < 25.0)
		score = 0.5;
	    else
		score = 0.0;

	    set_attr_double(p, "distance-to-known", d);
	    set_attr_double(p, "scaled_known", score);
	}
    }
}

void dummy_score(Placename pn)
{
    int j;

    for(j=0; j<LTVectorCount(pn->candidates); j++)
    {
	set_attr_double(pn->candidates[j], "distance-to-known", 99999.0);
	set_attr_double(pn->candidates[j], "scaled_known", 0.0);
    }
}
