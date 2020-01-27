INCLUDES=	-I$(LTXML2)/include -I$(LTXML2)/include/ltxml2
#LIBRARIES=	-static -L$(LTXML2)/lib -lltxml2 -lrxp -Bdynamic -lm
LIBRARIES=	$(LTXML2)/lib/libltxml2.a $(LTXML2)/lib/librxp.a -lm

DEBUG=		-g
OPT=		-O
CC=		gcc
GCCFLAGS=	-Wall -ansi -pedantic
CFLAGS=		$(GCCFLAGS) $(INCLUDES) $(DEBUG) $(OPT)
LDFLAGS=	$(DEBUG) $(OPT)

PROGS=	cluster score scalemisc coloc locality evalresults grid2latlong known-gridref

all:	$(PROGS)

cluster:	cluster.o resolve.o
	$(CC) $(LDFLAGS) -o cluster cluster.o resolve.o $(LIBRARIES)

cluster.o:	cluster.c resolve.h

scalemisc:		scalemisc.o resolve.o
	$(CC) $(LDFLAGS) -o scalemisc scalemisc.o resolve.o $(LIBRARIES)

scalemisc.o:	scalemisc.c resolve.h

score:		score.o resolve.o
	$(CC) $(LDFLAGS) -o score score.o resolve.o $(LIBRARIES)

score.o:	score.c resolve.h

coloc:		coloc.o resolve.o
	$(CC) $(LDFLAGS) -o coloc coloc.o resolve.o $(LIBRARIES)

coloc.o:	coloc.c resolve.h

locality:		locality.o resolve.o
	$(CC) $(LDFLAGS) -o locality locality.o resolve.o $(LIBRARIES)

locality.o:	locality.c resolve.h

resolve.o:	resolve.c resolve.h

gridref.o:	gridref.c gridref.h
	$(CC) -c $(CFLAGS) -std=gnu99 gridref.c

grid2latlong.o:	grid2latlong.c gridref.h
	$(CC) -c $(CFLAGS) -std=gnu99 grid2latlong.c

grid2latlong:	grid2latlong.o gridref.o
	$(CC) -o grid2latlong grid2latlong.o gridref.o -lm

evalresults:	evalresults.o resolve.o
	$(CC) $(LDFLAGS) -o evalresults evalresults.o resolve.o $(LIBRARIES)

evalresults.o:	evalresults.c resolve.h

known-gridref:	known-gridref.o resolve.o gridref.o
	$(CC) $(LDFLAGS) -o known-gridref known-gridref.o resolve.o gridref.o $(LIBRARIES)

known-gridref.o:	known-gridref.c resolve.h gridref.h
	$(CC) $(CFLAGS) -c $(CFLAGS) -std=gnu99 known-gridref.c
