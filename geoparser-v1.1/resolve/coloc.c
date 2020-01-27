#include <stdlib.h>
#include <math.h>

#include "lx.h"
#include "resolve.h"

void compute_colocs(LTVector(Placename, placenames), char *attr_name, char *score_name, double (*score_fn)(Place, Place));
double near_score(Place p, Place q);
double contains_score(Place p, Place q);
double contained_by_score(Place p, Place q);

void usage(int status)
{
    fprintf(stderr, "usage: cluster <placename_file\n");
    exit(status);
}

int main(int argc, char **argv)
{
#if 0
    int i, j;
#endif
    Document doc;

    if(argc != 1)
	usage(2);

    doc = read_document(stdin, 0, 0);

    compute_colocs(doc->placenames, "near", "scaled_near", near_score);
    compute_colocs(doc->placenames, "contains", "scaled_contains", contains_score);
    compute_colocs(doc->placenames, "contained-by", "scaled_contained_by", contained_by_score);

    write_document(stdout, doc);

    return 0;
}

void compute_colocs(LTVector(Placename, placenames), char *attr_name, char *score_name, double (*score_fn)(Place, Place))
{
    int i, j, k, l;
    Placename pn, pn2;
    Place p, p2;
    double best, score;
    Char *coloc_id;

    for(i=0; i<LTVectorCount(placenames); i++)
    {
	pn = placenames[i];

	for(j=0; j<LTVectorCount(pn->candidates); j++)
	    /* initialise to zero so we can safely give up */
	    set_attr_double(pn->candidates[j], score_name, 0);

	coloc_id = get_attr_string(pn, attr_name);
	if(!coloc_id)
	    /* no coloc */
	    continue;
	
	pn2 = 0;
	for(k=0; k<LTVectorCount(placenames); k++)
	{
	    pn2 = placenames[k];
	    if(LTStrcmp(coloc_id, pn2->id) == 0)
		break;
	}
	if(!pn2)
	{
	    /* coloc doesn't exist; shouldn't happen */
	    Fprintf(Stderr, "can't find coloc id %S for placename %S\n",
		    coloc_id, pn->name);
	    continue;
	}

#if 0
	Fprintf(Stderr, "coloc %s for %S is %S\n", attr_name, pn->name, pn2->name);
#endif

	for(j=0; j<LTVectorCount(pn->candidates); j++)
	{
	    p = pn->candidates[j];
	    best = 0.0;

	    for(l=0; l<LTVectorCount(pn2->candidates); l++)
	    {
		p2 = pn2->candidates[l];

		score = score_fn(p, p2);
		if(score > best)
		    best = score;
	    }

	    set_attr_double(p, score_name, best);
	}
    }
}

double near_score(Place p, Place q)
{
    double sep;

    sep = distance(p->latitude, p->longitude,
		   q->latitude, q->longitude);

    /* XXX Maybe take account of sizes */

    if(sep < 10)
	return 1;
    if(sep < 30)
	return .6;
    if(sep < 100)
	return 0.3;
    return 0;
}

/* Does p contain q? */

double contains_score(Place p, Place q)
{
    double radius, ppop, sep;
    Char *pcc, *qcc;

    ppop = get_attr_double(p, "pop");
    sep = distance(p->latitude, p->longitude,
		   q->latitude, q->longitude);
    pcc = get_attr_string(p, "in-cc");
    qcc = get_attr_string(q, "in-cc");

    switch(p->type)
    {
    case pt_country:

	if(pcc && qcc && LTStrcmp(pcc, qcc) == 0)
	    return 1.0;
	/* if it's not in it, give up - don't credit nearness to a country */
	return 0.0;

    case pt_ppl:
    case pt_ppla:
    case pt_pplc:

	/* Estimate the radius of p - call 1 million 100 sq km */
	radius = sqrt(ppop / 10000);
	if(sep < radius)
	    return 1.0;
	break;

    case pt_civila:

#if 0	
	Fprintf(Stderr, "%S to %S is %f km\n", p->name, q->name, sep);
#endif
	/* We don't really know much about the size of states */
	if(sep < 80.0)
	    return 0.7;
	if(sep < 160.0)
	    return 0.6;
	if(sep < 320.0)
	    return 0.5;
	if(sep < 640.0)
	    return 0.4;
	if(sep < 1280.0)
	    return 0.3;
	/* if it's not in it, give up - don't credit nearness to a state */
	return 0.0;

    default:
	break;
    }

    /* Otherwise give a little credit for nearness */

    if(sep < 10)
	return 0.3;
    if(sep < 30)
	return 0.2;
    if(sep < 100)
	return 0.1;
    return 0;
}

double contained_by_score(Place p, Place q)
{
    return contains_score(q, p);
}
