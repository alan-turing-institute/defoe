/* Convert OS National Grid References to lat/long */

/* Assumes ascii */

#include <math.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gridref.h"

void usage(void)
{
    fprintf(stderr, "usage: grid2latlong [-d] gridref\n");
    exit(1);
}

int main(int argc, char **argv)
{
    char *err;
    double E, N, lat, lon;
    int decimal = 0, os = 0;

    while(argc > 1 && argv[1][0] == '-')
    {
	if(strcmp(argv[1], "-d") == 0)
	{
	    decimal = 1;
	    argc--;
	    argv++;
	}
	else if(strcmp(argv[1], "-o") == 0)
	{
	    os = 1;
	    argc--;
	    argv++;
	}
	else
	    usage();
    }

    if(argc == 2)
    {
	if((err = gridref_to_nums(argv[1], &E, &N)) != 0)
	{
	    fprintf(stderr, "bad grid reference <%s>: %s\n", argv[1], err);
	    return 1;
	}
    }
    else 
	usage();

/*
    dprintf("%f %f\n", E, N);
*/

    (os ? en_to_osgb36 : en_to_wgs84)(E, N, &lat, &lon);
/*
    en_to_wgs84(651409.903, 313177.270, &lat, &lon);
*/
    if(decimal)
	printf("%.4f, %.4f\n", lat * 180 / M_PI, lon * 180 / M_PI);
    else
    {
	long latsec, lonsec;
	char latdir = 'N', londir = 'E';

	if(lat < 0)
	{
	    lat = -lat;
	    latdir = 'S';
	}
	if(lon < 0)
	{
	    lon = -lon;
	    londir = 'W';
	}

	latsec = round(lat / M_PI * 180 * 3600);
	lonsec = round(lon / M_PI * 180 * 3600);
	printf("%ld %ld' %ld\" %c  %ld %ld' %ld\" %c\n",
	       latsec / 3600, (latsec / 60) % 60, latsec % 60, latdir,
	       lonsec / 3600, (lonsec / 60) % 60, lonsec % 60, londir);
    }

    return 0;
}
