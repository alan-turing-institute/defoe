char *gridref_to_nums(char *gridref, double *E, double *N);
char *newgridref_to_nums(char *gridref, double *E, double *N);
char *oldgridref_to_nums(char *gridref, double *E, double *N);
char *numgridref_to_nums(char *gridref, double *E, double *N);

char *letter_to_num(char letter, long *number);
char *digits_to_nums(char *digits, long *E, long *N);
char *digits_to_num(char *digits, double *EN);

void en_to_osgb36(double E, double N, double *lat, double *lon);
void en_to_wgs84(double E, double N, double *lat, double *lon);

struct ellipsoid {double a, b;};

extern struct ellipsoid airy1830, grs8;

