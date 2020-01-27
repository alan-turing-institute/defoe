/* Take a "compare" file and count how many pairs have the same id
   and how many are within a given distance of each other. */

#include <stdlib.h>
#include <math.h>

#include "lx.h"
#include "resolve.h"

void usage(int status)
{
    fprintf(stderr, "usage: evalresults maxdist compare-file ...\n");
    exit(status);
}

#define require(cond) requiref(cond, #cond);

void requiref(int ok, char *message)
{
    if(!ok)
    {
	fprintf(stderr, "error: assertion failed: %s\n", message);
	exit(1);
    }
}

char *getat(LXItem item, char *name)
{
    Char *val;

    require(item->type == LX_IT_Element);

    val = LXGetAttributeValue8((LXElement)item, "", name);
    require(val && val[0]);

    return LTStrdupC8(val);
}

int main(int argc, char **argv)
{
    double maxdist;
    int f, i;
    LXParser p;
    LXItem doc;
    LXXPathValue val;
    LXQuery goldq, resolverq;
    LTVector(LXItem, gold);
    LTVector(LXItem, resolver);

    int exact = 0, fuzzy = 0, total = 0;

    if(argc < 3)
	usage(2);

    maxdist = atof(argv[1]);

    LXInit(LX_GF_ExitOnAllErrors);

    goldq = LXQueryCompile8("//compare/gold", 0);
    resolverq = LXQueryCompile8("//compare/resolver", 0);

    for(f = 2; f < argc; f++)
    {
/*	fprintf(stderr, "%s\n", argv[f]); */

	p = LXURIParserCreate(LTStrdup8C(argv[f]), 0, 0);
	doc = LXReadSubtree(p);

	val = LXQueryEval(goldq, doc);
	require(val->type == LX_VT_node_set);
	gold = val->value.nodes;

	val = LXQueryEval(resolverq, doc);
	require(val->type == LX_VT_node_set);
	resolver = val->value.nodes;

	require(LTVectorCount(gold) == LTVectorCount(resolver));

	for(i=0; i<LTVectorCount(resolver); i++)
	{
	    char *gid, *rid;
	    double glat, glong, rlat, rlong, dist;

	    gid = getat(gold[i], "gazref");
	    rid = getat(resolver[i], "gazref");
	    glat = atof(getat(gold[i], "lat"));
	    glong = atof(getat(gold[i], "long"));
	    rlat = atof(getat(resolver[i], "lat"));
	    rlong = atof(getat(resolver[i], "long"));
	    dist = distance(glat, glong, rlat, rlong);

	    if(strcmp(gid, rid) == 0)
		exact++;
	    if(dist <= maxdist)
		fuzzy++;
	    total++;
	}

	LXParserClose(p);
    }

    printf("total: %d   exact: %d (%.1f%%)   within %.1fkm %d (%.1f%%)\n",
	   total, exact, exact*100.0/total,
	   maxdist, fuzzy, fuzzy*100.0/total);

    return 0;
}

