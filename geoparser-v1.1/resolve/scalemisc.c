/* Scale the population and type propoerties to [0,1] for ease of combination */

#include <stdlib.h>
#include <math.h>

#include "lx.h"
#include "resolve.h"

void scale(LTVector(Placename, placenames));

void usage(int status)
{
    fprintf(stderr, "usage: scalemisc <placename_file\n");
    exit(status);
}

int main(int argc, char **argv)
{
    Document doc;

    if(argc != 1)
	usage(2);

    doc = read_document(stdin, 0, 0);

    scale(doc->placenames);

    write_document(stdout, doc);

    return 0;
}

void scale(LTVector(Placename, placenames))
{
    int i, j;
    Placename pn;
    Place p;
    double t, pop, type;

    for(i=0; i<LTVectorCount(placenames); i++)
    {
	pn = placenames[i];
	
	for(j=0; j<LTVectorCount(pn->candidates); j++)
	{
	    p = pn->candidates[j];

	    /* population: log scale, 10^3 -> .2, 10^7 -> 1 */
	    t = get_attr_double(p, "pop");
	    if(t < 1000)
		pop = 0.0;
	    else
		pop = log10(t) / 5 - 0.4;
	    set_attr_double(p, "scaled_pop", pop);

	    /* type */
	    switch(p->type)
	    {
	    case pt_continent:
	    case pt_country:
		type = 1.0;
		break;
	    case pt_pplc:
		type = 1.0;
		break;
	    case pt_civila:
		type = 0.8;
		break;
	    case pt_ppla:
		type = 0.8;
		break;
	    case pt_ppl:
		type = 0.6;
		break;
	    case pt_civil:
	    case pt_water:
	    case pt_mtn:
	    case pt_rgn:
		type = 0.4;
		break;
	    case pt_fac:
		type = 0.2;
		break;
	    default:
		type = 0.0;
		break;
	    }
	    set_attr_double(p, "scaled_type", type);
	}
    }
}

