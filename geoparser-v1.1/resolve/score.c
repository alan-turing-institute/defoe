#define _XOPEN_SOURCE 600	/* for random() etc */
#include <stdlib.h>
#include <math.h>

#include "lx.h"
#include "resolve.h"

struct place_data {
    double score;
    int randnum;
};
#define score(p) ((struct place_data *)p->user_data)->score
#define randnum(p) ((struct place_data *)p->user_data)->randnum

void compute_score(LTVector(Placename, placenames), LXQuery sq);

void usage(int status)
{
    fprintf(stderr, "usage: score score-xpath <placename_file\n");
    exit(status);
}

int main(int argc, char **argv)
{
    Document doc;
    LXQuery sq;

    if(argc != 2)
	usage(2);

    doc = read_document(stdin, 0, sizeof(struct place_data));

    sq = LXQueryCompile8(argv[1], 0);

    compute_score(doc->placenames, sq);

    write_document(stdout, doc);

    return 0;
}

static int compare_score(const void *a, const void *b)
{
    Place aa = *(Place *)a, bb = *(Place *)b;

    if(score(aa) != score(bb))
	return score(aa) > score(bb) ? 1 : -1;

#if 0

    /* break ties by latitude and longitude to ensure repeatable results
       (if they have the same latitude/longitude it won't matter to the
       score which we choose) */

    if(aa->latitude > bb->latitude)
	return 1;
    if(aa->latitude < bb->latitude)
	return -1;

    if(aa->longitude > bb->longitude)
	return 1;
    if(aa->longitude < bb->longitude)
	return -1;
 
    /* prefer earliest in doc order */

    if(aa->elem->number < bb->elem->number)
	return 1;
    if(aa->elem->number > bb->elem->number)
	return -1;
#else
    if(randnum(aa) > randnum(bb))
	return 1;
    if(randnum(aa) < randnum(bb))
	return -1;
#endif
	
    return 0;
}

void compute_score(LTVector(Placename, placenames), LXQuery sq)
{
    int i, j;
    Placename pn;
    Place p;
    LXXPathValue val;

    srandom(83457834);

    for(i=0; i<LTVectorCount(placenames); i++)
    {
	pn = placenames[i];
	
	for(j=0; j<LTVectorCount(pn->candidates); j++)
	{
	    p = pn->candidates[j];

	    randnum(p) = random();

	    val = LXQueryEval(sq, (LXItem)p->elem);
	    if(val->type != LX_VT_number)
	    {
		fprintf(stderr, "score query did not return number\n");
		exit(1);
	    }

	    score(p) = val->value.number;
	    set_attr_double(p, "score", score(p));
	}

	qsort(pn->candidates, LTVectorCount(pn->candidates), sizeof(pn->candidates[0]),
	      compare_score);
	for(j=0; j<LTVectorCount(pn->candidates); j++)
	    set_attr_int(pn->candidates[j], "rank", LTVectorCount(pn->candidates)-j);
    }
}
