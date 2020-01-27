#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "gridref.h"

static void debprintf(const char *format, ...);

#define MIN_SHEET 64
#define MAX_SHEET 190
struct sheet {int num, e, n;} sheets[MAX_SHEET - MIN_SHEET + 1];

char *gridref_to_nums(char *gridref, double *E, double *N)
{
    if(strchr(gridref, '-') != 0)
	return oldgridref_to_nums(gridref, E, N);
    else if(strchr(gridref, ',') != 0)
	return numgridref_to_nums(gridref, E, N);
    else
	return newgridref_to_nums(gridref, E, N);
}

char *numgridref_to_nums(char *gridref, double *E, double *N)
{
    long elen, nlen;
    long scale;
    int precision, i;
    double e, n;
    char *comma = strchr(gridref, ','), *p;
    char buf[8];

    /* The two coordinates must have the same length, or the northings must
       be 1 digit longer and start with 1 (this happens for the islands to
       the north of Scotland) */

    if(!comma)
	return("no comma in numeric grid reference");
    elen = comma - gridref;
    nlen = strlen(comma+1);

    if(nlen == elen && elen <= 6)
	/* normal case */
	precision = elen;
    else if(nlen == elen+1 && comma[1] == '1')
	/* far north: northings > 1,000,000 so they have an extra digit */
	precision = elen;
    else if(nlen == elen && elen <= 7 &&
	    gridref[0] == '0' && comma[1] == '1')
	/* stupid case: like far north but eastings have a leading zero
	   added to make the coordinates have the same number of digits,
	   so scaling is off; see
	   http://en.wikipedia.org/wiki/Talk:Ordnance_Survey_National_Grid */
	precision = elen-1;
    else
	return("malformed numeric grid reference");

    for(scale=1, i=precision; i<6; i++)
	scale *= 10;

    for(p=gridref; *p; p++)
	if(p != comma && (*p < '0' || *p > '9'))
	    return "bad digit in numeric gridref";

    memcpy(buf, gridref, elen);
    buf[elen] = 0;
    e = atol(buf);
    n = atol(comma+1);

    *E = e * scale;
    *N = n * scale;

    return 0;
}

char *newgridref_to_nums(char *gridref, double *E, double *N)
{
    long let1, let2;		/* in km */
    long numn, nume;		/* in m */
    double e, n;
    char *err;

    if(strlen(gridref) < 2)
	return "grid reference too short";

    /* convert letters */

    if((err = letter_to_num(gridref[0], &let1)) != 0 || 
       (err = letter_to_num(gridref[1], &let2)) != 0)
	return err;

    /* from an origin at SW of AA */

    e = (let1 % 5) * 500 + (let2 % 5) * 100;
    n = -((let1 / 5) * 500 + (let2 / 5) * 100);

    /* from the "false origin" at SW of SV */

    e -= 1000;
    n += 1900;

    /* convert digits */

    if((err = digits_to_nums(gridref+2, &nume, &numn)) != 0)
	return err;

    *E = e * 1000.0 + nume;
    *N = n * 1000.0 + numn;

    return 0;
}

char *letter_to_num(char letter, long *number)
{
    long n;

    if(letter >= 'a' && letter <='z' && letter != 'i')
	n = letter - 'a';
    else if(letter >= 'A' && letter <='Z' && letter != 'I')
	n = letter - 'A';
    else
	return "bad letter";

    if(n > 'i' - 'a')
	/* I is not used */
	n--;

    *number = n;
    return 0;
}

char *digits_to_nums(char *digits, long *E, long *N)
{
    int len = strlen(digits), numlen;
    char buf[6];
    int i;
    long scale;

    if(len > 10)
	return "too many digits";
    if(len % 2 != 0)
	return "must have an even number of digits";

    numlen = len/2;
    for(scale=1, i=numlen; i<5; i++)
	scale *= 10;

    for(i=0; i<len; i++)
	if(digits[i] < '0' || digits[i] > '9')
	    return "bad digit";

    memcpy(buf, digits, numlen);
    buf[numlen] = 0;
//    *E = atol(buf) * scale + scale/2;
    *E = atol(buf) * scale;

    memcpy(buf, digits+numlen, numlen);
    buf[numlen] = 0;
//    *N = atol(buf) * scale + scale/2;
    *N = atol(buf) * scale;

    return 0;
}


char *oldgridref_to_nums(char *gridref, double *E, double *N)
{
    long numn, nume;		/* in m */
    double e, n;		/* in km */
    char *err;
    struct sheet *sheet;
    int sheetnum;
    char *hyphen;

    hyphen = strchr(gridref, '-');
    if(!hyphen || hyphen < gridref+2)
	return "malformed grid reference";

    /* look up sheet origin */

    sheetnum = atoi(gridref);
    if(sheetnum < MIN_SHEET || sheetnum > MAX_SHEET ||
       (sheet = &sheets[sheetnum - MIN_SHEET])->e == -1)
	return "bad sheet number";

    /* convert digits */

    if((err = digits_to_nums(hyphen+1, &nume, &numn)) != 0)
	return err;

    if(nume / 1000 >= sheet->e % 100)
	e = (sheet->e / 100) * 100;
    else
	e = (sheet->e / 100 + 1) * 100;

    if(numn / 1000 >= sheet->n % 100)
	n = (sheet->n / 100) * 100;
    else
	n = (sheet->n / 100 + 1) * 100;


    *E = e * 1000.0 + nume;
    *N = n * 1000.0 + numn;

    return 0;
}

#define MIN_SHEET 64
#define MAX_SHEET 190
struct sheet sheets[MAX_SHEET - MIN_SHEET + 1] =
{
    {64, 375, 630},
    {65, -1, -1},
    {66, -1, -1},
    {67, -1, -1},
    {68, -1, -1},
    {69, -1, -1},
    {70, -1, -1},
    {71, 390, 595},
    {72, -1, -1},
    {73, -1, -1},
    {74, -1, -1},
    {75, 293, 550},
    {76, 333, 550},
    {77, 373, 550},
    {78, 403, 550},
    {79, -1, -1},
    {80, -1, -1},
    {81, -1, -1},
    {82, 293, 505}, 
    {83, 333, 505},
    {84, 373, 505},
    {85, 413, 505},
    {86, 453, 485},
    {87, -1, -1},
    {88, 300, 460},
    {89, 330, 460},
    {90, 370, 460},
    {91, 410, 460},
    {92, 450, 460},
    {93, 487, 465},
    {94, 330, 420},
    {95, 360, 415},
    {96, 400, 415},
    {97, 440, 420},
    {98, 460, 420},
    {99, 500, 420},
    {100, 320, 375},
    {101, 360, 375},
    {102, 400, 385},
    {103, 435, 375},
    {104, 475, 375},
    {105, 515, 375},
    {106, 220, 353},
    {107, 248, 340},
    {108, 288, 340},
    {109, 320, 345},
    {110, 360, 330},
    {111, 400, 345},
    {112, 440, 330},
    {113, 480, 330},
    {114, 520, 330},
    {115, 210, 320},
    {116, 248, 308},
    {117, 288, 300},
    {118, 328, 300},
    {119, 360, 300},
    {120, 400, 300},
    {121, 428, 300},
    {122, 455, 300},
    {123, 495, 300},
    {124, 535, 300},
    {125, 575, 302},
    {126, 615, 302},
    {127, 248, 263},
    {128, 288, 255},
    {129, 328, 255},
    {130, 360, 255},
    {131, 388, 255},
    {132, 428, 255},
    {133, 455, 255},
    {134, 495, 255},
    {135, 535, 255},
    {136, 575, 257},
    {137, 615, 257},
    {138, 164, 205},
    {139, 208, 218},
    {140, 248, 218},
    {141, 288, 210},
    {142, 328, 210},
    {143, 360, 210},
    {144, 388, 210},
    {145, 428, 210},
    {146, 455, 210},
    {147, 495, 210},
    {148, 535, 210},
    {149, 570, 212},
    {150, 610, 212},
    {151, 145, 190},
    {152, 208, 180},
    {153, 248, 173},
    {154, 288, 165},
    {155, 328, 165},
    {156, 353, 165},
    {157, 388, 165},
    {158, 428, 165},
    {159, 463, 173},
    {160, 495, 180},
    {161, 535, 180},
    {162, 570, 180},
    {163, 211, 110},
    {164, 280, 110},
    {165, 320, 130},
    {166, 353, 120},
    {167, 388, 120},
    {168, 428, 120},
    {169, 463, 128},
    {170, 495, 135},
    {171, 535, 135},
    {172, 570, 135},
    {173, 602, 128},
    {174, 200,  85},
    {175, 240,  70},
    {176, 280,  70},
    {177, 320,  85},
    {178, 353,  68},
    {179, 388,  75},
    {180, 428,  75},
    {181, 461,  90}, 
    {182, 495,  99},
    {183, 535,  93},
    {184, 570, 105},
    {185, 170,  55},
    {186, 200,  45},
    {187, 240,  35},
    {188, 260,  35},
    {189,  80,  05},
    {190, 170,  10}
};

/* Algorithms from "A guide to coordinate systems in Great Britain"
   (http://badc.nerc.ac.uk/help/coordinates/OSGB.pdf)
 */

struct ellipsoid airy1830 = { 6377563.396, 6356256.910};
struct ellipsoid grs80 = {6378137.0, 6356752.3141};

void to_xyz(double lat, double lon, double eheight,
	    double *x, double *y, double *z,
	    struct ellipsoid *ell)
{
    double e2 = (ell->a*ell->a - ell->b*ell->b) / (ell->a*ell->a);
    double v = ell->a / sqrt(1 - e2 * sin(lat) * sin(lat));
    *x = (v + eheight) * cos(lat) * cos(lon);
    *y = (v + eheight) * cos(lat) * sin(lon);
    *z = ((1 - e2) * v + eheight) * sin(lat);
}

void from_xyz(double x, double y, double z,
	      double *lat, double *lon, double *eheight,
	      struct ellipsoid *ell)
{
    double e2 = (ell->a*ell->a - ell->b*ell->b) / (ell->a*ell->a);
    double p = sqrt(x*x + y*y);
    double oldlat, newlat, v;

    *lon = atan2(y, x);

    newlat = atan(z / (p * (1 - e2)));
    do
    {
	oldlat = newlat;
	v = ell->a / sqrt(1 - e2 * sin(oldlat) * sin(oldlat));
	newlat = atan((z  + e2 * v * sin(oldlat)) / p);
    } while(fabs(newlat - oldlat) > 1e-12); /* roughly 0.01mm */
    *lat = newlat;

    v = ell->a / sqrt(1 - e2 * sin(oldlat) * sin(newlat));
    *eheight = p / cos(newlat) - v;
}

#define sec_to_rad(x) (((x) / (180*60*60)) * M_PI)

void osgb36_to_wgs84(double olat, double olon, double *wlat, double *wlon)
{
    double tx = 446.448, ty = -125.157, tz = 542.060;
    double s = -20.4894 / 1e6;
    double rx = sec_to_rad(0.1502), ry = sec_to_rad(0.2470), rz = sec_to_rad(0.8421);
    double ox, oy, oz, wx, wy, wz;
    double oh = 50.0, wh;

    to_xyz(olat, olon, oh, &ox, &oy, &oz, &airy1830);

    wx = tx + ox * (1+s) + oy * -rz   + oz * ry;
    wy = ty + ox * rz    + oy * (1+s) + oz * -rx;
    wz = tz + ox * -ry   + oy * rx    + oz * (1+s);

    debprintf("%.2f,%.2f,%.2f -> %.2f,%.2f,%.2f\n",
	    ox, oy, oz, wx, wy, wz);
    from_xyz(wx, wy, wz, wlat, wlon, &wh, &grs80);
    debprintf("height %f\n", wh);
}

void en_to_wgs84(double E, double N, double *lat, double *lon)
{
    double olat, olon;

    en_to_osgb36(E, N, &olat, &olon);
    osgb36_to_wgs84(olat, olon, lat, lon);
}

/* Algorithm from 
 * http://www.ordnancesurvey.co.uk/oswebsite/gps/docs/convertingcoordinatesEN.pdf
 * (also in "A guide to coordinate systems in Great Britain")
 * See also
 * http://www.ordnancesurvey.co.uk/oswebsite/gps/docs/convertingcoordinates3D.pdf
 * http://www.ordnancesurvey.co.uk/oswebsite/gps/information/coordinatesystemsinfo/guidecontents/guidea.html
 *
 * NB this produces OSGB36 lat/long coordinates, which may differ by
 * up to 120m from WGS84 as used by Google Maps, GPS, etc.
 */

#define deg_to_rad(x) ((x) / 180.0 * M_PI)

void en_to_osgb36(double E, double N, double *lat, double *lon)
{
    /* Airy 1830 parameters */
    double a = airy1830.a, b = airy1830.b;
    double e2 = (a*a - b*b) / (a*a);

    /* National Grid parameters */
    double N0 = -100000, E0 = 400000;
    double F0 = 0.9996012717;
    double lat0 = deg_to_rad(49), lon0 = deg_to_rad(-2);

    double latp, M;
    double n = (a-b)/(a+b);
    double nu, rho, eta2, t;

    double tlat, slat;
    double nu3, nu5, nu7;
    double tlat2, tlat4, tlat6;
    double Ed, Ed2, Ed3, Ed4, Ed5, Ed6, Ed7;
    double VII, VIII, IX, X, XI, XII, XIIA;
    
    M=0;
    latp = lat0;
    do {
	latp = (N - N0 - M) / (a * F0) + latp;
	M = b * F0 *
	    ((1 + n + (5.0/4)*n*n + (5.0/4)*n*n*n) * (latp - lat0) -
	     (3*n + 3*n*n + (21.0/8)*n*n*n) * sin(latp-lat0) * cos(latp+lat0) +
	     ((15.0/8)*n*n + (15.0/8)*n*n*n) * sin(2*(latp-lat0)) * cos(2*(latp+lat0)) -
	     (35.0/24)*n*n*n*sin(3*(latp-lat0))*cos(3*(latp+lat0)));
	debprintf("latp = %g, M = %g\n", latp, M);
    } while(N - N0 - M >= 0.00001); /* 0.01mm */


    t = 1 - e2 * sin(latp) * sin(latp);
    nu = a * F0 / sqrt(t);
    rho = a * F0 * (1 - e2) / t / sqrt(t);
    eta2 = nu / rho - 1;

    debprintf("nu %g rho %g eta %g\n", nu, rho, eta2);

    tlat = tan(latp);
    slat = 1/cos(latp);

    nu3 = nu*nu*nu; nu5 = nu3*nu*nu; nu7 = nu5*nu*nu;
    tlat2 = tlat*tlat; tlat4 = tlat2*tlat2; tlat6 = tlat4*tlat2;
 
    VII = tlat / (2*rho*nu);
    debprintf("VII %g\n", VII);
    VIII = tlat / (24*rho*nu3) * (5 + 3*tlat2 + eta2 - 9*tlat2*eta2);
    debprintf("VIII %g\n", VIII);
    IX = tlat / (720*rho*nu5) * (61 + 90*tlat2 + 45*tlat4);
    debprintf("IX %g\n", IX);
    X = slat / nu;
    debprintf("X %g\n", X);
    XI = slat / (6*nu3) * (nu/rho + 2*tlat2);
    debprintf("XI %g\n", XI);
    XII = slat / (120*nu5) * (5 + 28*tlat2 + 24*tlat4);
    debprintf("XII %g\n", XII);
    XIIA = slat / (5040*nu7) * (61 + 662*tlat2 + 1320*tlat4 + 720*tlat6);
    debprintf("XIIA %g\n", XIIA);

    Ed = E - E0;
    Ed2 = Ed*Ed;  Ed3 = Ed2*Ed; Ed4 = Ed3*Ed; 
    Ed5 = Ed4*Ed; Ed6 = Ed5*Ed; Ed7 = Ed6*Ed;
    
    *lat = latp - VII*Ed2 + VIII*Ed4 - IX*Ed6;
    *lon = lon0 + X*Ed - XI*Ed3 + XII*Ed5 - XIIA*Ed7;
}

void debprintf(const char *format, ...)
{
#if 0
    va_list args;

    va_start(args, format);
    vfprintf(stderr, format, args);
    va_end(args);
#endif
}
