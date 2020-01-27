#include "lx.h"

#define common_fields \
    LXElement elem

typedef struct common {
    common_fields;
} *Common;

typedef struct placename {
    common_fields;
    Char *id;
    Char *name;
    LTVector(struct place *, candidates);
    void *user_data;
} *Placename;

typedef enum place_type {
    pt_water, pt_civil, pt_civila, pt_country, pt_fac, pt_mtn, pt_ppl, pt_ppla,
    pt_pplc, pt_rgn, pt_road, pt_continent, pt_other
} PlaceType;

extern char *place_type_name[];

typedef struct place {
    common_fields;
    Char *name;
    Char *gazref;
    double latitude, longitude;
    enum place_type type;
    void *user_data;
} *Place;

typedef struct document {
    LXItem doc;
    LTVector(Placename, placenames);
} *Document;

Document read_document(FILE *in, int place_data_size, int placename_data_size);
void write_document(FILE *out, Document doc);

void set_attr_string(void *thing, char *attrname, Char *value);
Char *get_attr_string(void *thing, char *attrname);
void set_attr_int(void *thing, char *attrname, int value);
double get_attr_double(void *thing, char *attrname);
void set_attr_double(void *thing, char *attrname, double value);

double distance(double lats, double longs, double latf, double longf);

extern char *place_type_name[];
