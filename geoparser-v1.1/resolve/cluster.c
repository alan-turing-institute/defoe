#include <stdlib.h>
#include <math.h>

#include "lx.h"
#include "resolve.h"

struct place_data {
    double clusteriness;
};
#define clusteriness(p) ((struct place_data *)p->user_data)->clusteriness

void compute_clusteriness(LTVector(Placename, placenames));

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

    doc = read_document(stdin, 0, sizeof(struct place_data));

    compute_clusteriness(doc->placenames);
#if 0
    for(i=0; i<LTVectorCount(placenames); i++)
    {
	Printf("%S:\n", doc->placenames[i]->name);
	for(j=0; j<LTVectorCount(doc->placenames[i]->candidates); j++)
	    Printf("  %S (%s) %lf (%d)\n", 
		   doc->placenames[i]->candidates[j]->name,
		   place_type_name[doc->placenames[i]->candidates[j]->type],
		   doc->placenames[i]->candidates[j]->clusteriness,
		   doc->placenames[i]->candidates[j]->clusteriness_rank);
    }
#endif

    write_document(stdout, doc);

    return 0;
}

#define INFINITE_DISTANCE (1e6)
#define MAX_NEIGHBOURS 5

static int compare_double(const void *a, const void *b)
{
    double aa = *(double *)a, bb = *(double *)b;

    return aa < bb ? -1 : (aa > bb ? 1 : 0);
}

static int compare_clusteriness(const void *a, const void *b)
{
    Place aa = *(Place *)a, bb = *(Place *)b;

    return clusteriness(aa) < clusteriness(bb) ? -1 : (clusteriness(aa) > clusteriness(bb) ? 1 : 0);
}

void compute_clusteriness(LTVector(Placename, placenames))
{
    int i, j, k, l, neighbours;
    Placename pn, pn2;
    Place p, p2;
    double d, avg, clus, best_dist_to_pn2;
    LTVector(double, distances);
    LTVector(Place, candidates);
    Char *in_cc, *cc;

    for(i=0; i<LTVectorCount(placenames); i++)
    {
	pn = placenames[i];
	LTVectorInit(candidates);

	for(j=0; j<LTVectorCount(pn->candidates); j++)
	{
	    p = pn->candidates[j];
	    LTVectorPush(candidates, p);
	    LTVectorInit(distances);

	    in_cc = get_attr_string(p, "in-cc");

	    for(k=0; k<LTVectorCount(placenames); k++)
	    {
		pn2 = placenames[k];

		/* Don't rely on there not being duplicates */
		if(LTStrcmp(pn->name, pn2->name) == 0)
		    continue;

		best_dist_to_pn2 = INFINITE_DISTANCE;

		for(l=0; l<LTVectorCount(pn2->candidates); l++)
		{
		    p2 = pn2->candidates[l];

		    d = distance(p->latitude, p->longitude,
				 p2->latitude, p2->longitude);
		    if(d < best_dist_to_pn2)
			best_dist_to_pn2 = d;

		    cc = get_attr_string(p2, "cc");
		    if(in_cc && cc && LTStrcmp(in_cc, cc) == 0)
			best_dist_to_pn2 = 0;
		}
		
		if(best_dist_to_pn2 != INFINITE_DISTANCE)
		    LTVectorPush(distances, best_dist_to_pn2);
	    }

	    if(LTVectorCount(distances) == 0)
	    {
		clusteriness(p) = INFINITE_DISTANCE;
		set_attr_double(p, "clusteriness", INFINITE_DISTANCE);
		set_attr_double(p, "scaled_clusteriness", 0);
		continue;
	    }

	    qsort(distances, LTVectorCount(distances), sizeof(distances[0]), 
		  compare_double);

	    neighbours = LTVectorCount(distances) > MAX_NEIGHBOURS ? MAX_NEIGHBOURS : LTVectorCount(distances);

	    avg = 0;
	    for(k=0; k<neighbours; k++)
		avg += distances[k];
	    avg /= neighbours;
	    
	    LTVectorFree(distances);

	    clusteriness(p) = avg;
	    set_attr_double(p, "clusteriness", avg);

	    /* log scale, 10 -> 1, 1000 -> 0 */

	    if(avg < 10)
		clus = 1.0;
	    else if(avg > 1000)
		clus = 0.0;
	    else
		clus = 1.5 - log10(avg) / 2;
	    set_attr_double(p, "scaled_clusteriness", clus);
	}
	
	qsort(candidates, LTVectorCount(candidates), sizeof(candidates[0]),
	      compare_clusteriness);
	for(j=0; j<LTVectorCount(candidates); j++)
	    set_attr_int(candidates[j], "clusteriness_rank", j+1);
    }
}

