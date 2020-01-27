/* Toponym resolution utilities */

#include <assert.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "lx.h"
#include "resolve.h"

static Placename process_placename(LXElement pn, int place_data_size, int placename_data_size);
static Char *get_attr_or_die(LXElement e, char *attrname);

static LXQuery placename_query, place_query;

void write_document(FILE *out, Document doc)
{
    LXSerializer s;

    s = LXFILESerializerCreate(out, 0, 0);
    LXWriteSubtree(s, doc->doc);
    LXSerializerClose(s);
}

Document read_document(FILE *in, int place_data_size, int placename_data_size)
{
    int i;
    LXParser p;
    LXItem item;
    LXXPathValue val;
    Document doc;

    LXInit(LX_GF_ExitOnAllErrors);

    doc = LTMalloc(sizeof(*doc));
    LTVectorInit(doc->placenames);

    if(!placename_query)
	placename_query = LXQueryCompile8("//placename", 0);

    p = LXFILEParserCreate(in, 0, 0);
    doc->doc = LXReadSubtree(p);
    val = LXQueryEval(placename_query, doc->doc);

    assert(val->type == LX_VT_node_set);
    for(i=0; i<LTVectorCount(val->value.nodes); i++)
    {
	item = val->value.nodes[i];
	assert(item->type == LX_IT_Element);
	LTVectorPush(doc->placenames, process_placename((LXElement)item, place_data_size, placename_data_size));
    }

    return doc;
}

static Placename process_placename(LXElement pn, int place_data_size, int placename_data_size)
{
    LXXPathValue val;
    int i, j;
    Char *s;
    Placename placename = LTMalloc(sizeof(*placename));

    placename->user_data = LTMalloc(placename_data_size);
    placename->elem = pn;
    placename->id = LTStrdup(get_attr_or_die(pn, "id"));
    placename->name = LTStrdup(get_attr_or_die(pn, "name"));
    LTVectorInit(placename->candidates);

    if(!place_query)
	place_query = LXQueryCompile8("place", 0);

    val = LXQueryEval(place_query, (LXItem)pn);
    assert(val->type == LX_VT_node_set);
    
    for(i=0; i<LTVectorCount(val->value.nodes); i++)
    {
	Place place = LTMalloc(sizeof(*place));
	LXElement p;

	place->user_data = LTMalloc(place_data_size);

	assert(val->value.nodes[i]->type == LX_IT_Element);
	p = (LXElement)val->value.nodes[i];

	place->elem = p;
	place->name = LTStrdup(get_attr_or_die(p, "name"));
	place->gazref = LTStrdup(get_attr_or_die(p, "gazref"));
	place->latitude = atof(LTStrdupC8(get_attr_or_die(p, "lat")));
	place->longitude = atof(LTStrdupC8(get_attr_or_die(p, "long")));

	s = get_attr_or_die(p, "type");
	place->type = pt_other;
	for(j=0; j<pt_other; j++)
	    if(LTStrcmpC8(s, place_type_name[j]) == 0)
	    {
		place->type = j;
		break;
	    }

	LTVectorPush(placename->candidates, place);
    }

    return placename;
}

#define sq(x) ((x)*(x))
#define earth_radius 6372.8 /* km */
#define degtorad(d) ((d) / 180.0 * 3.14159265358979)

/* Distance between two places, in km.  lat/long in degrees.
   Formula from http://en.wikipedia.org/wiki/Great-circle_distance */

double distance(double lats, double longs, double latf, double longf)
{
    double dlong;
    double num, denom;

    lats = degtorad(lats);
    longs = degtorad(longs);
    latf = degtorad(latf);
    longf = degtorad(longf);

    dlong = longf-longs;

    num = sqrt(sq(cos(latf)*sin(dlong)) + 
	       sq(cos(lats)*sin(latf) - sin(lats)*cos(latf)*cos(dlong)));
    denom = sin(lats)*sin(latf) + cos(lats)*cos(latf)*cos(dlong);

    return atan2(num, denom) * earth_radius;
}

void set_attr_string(void *thing, char *attrname, Char *value)
{
    LXAddAttribute(((Common)thing)->elem,
		   LXAttributeCreate(LTStrdup(LX_empty_string), LTStrdup8C(attrname), 0,
				     LTStrdup(value), LX_AT_CDATA, 1));
}

Char * get_attr_string(void *thing, char *attrname)
{
    return LXGetAttributeValue8(((Common)thing)->elem, "", attrname);
}

void set_attr_int(void *thing, char *attrname, int value)
{
    char val[20];

    sprintf(val, "%d", value);
    LXAddAttribute(((Common)thing)->elem,
		   LXAttributeCreate(LTStrdup(LX_empty_string), LTStrdup8C(attrname), 0,
				     LTStrdup8C(val), LX_AT_CDATA, 1));
}

void set_attr_double(void *thing, char *attrname, double value)
{
    char val[20];

    sprintf(val, "%.10g", value);
    LXAddAttribute(((Common)thing)->elem,
		   LXAttributeCreate(LTStrdup(LX_empty_string), LTStrdup8C(attrname), 0,
				     LTStrdup8C(val), LX_AT_CDATA, 1));
}

double get_attr_double(void *thing, char *attrname)
{
    Char *val;
    char *vals;
    double vald;

    val = LXGetAttributeValue8(((Common)thing)->elem, "", attrname);
    if(!val)
	return 0.0;		/* XXX reconsider */
    vals = LTStrdupC8(val);
    vald = atof(vals);

    LTFree(vals);
    
    return vald;
}

static Char *get_attr_or_die(LXElement e, char *attrname)
{
    Char *s = LXGetAttributeValue8(e, "", attrname);
    if(!s)
    {
	Fprintf(Stderr, "Missing attribute \"%s\" on element \"%S\"\n",
		attrname, e->localName);
	exit(1);
    }
    return s;
}

char *place_type_name[] = 
{
    "water", "civil", "civila", "country", "fac", "mtn", "ppl", "ppla",
    "pplc", "rgn", "road", "continent", "other"
};


