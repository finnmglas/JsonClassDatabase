/**
 *  jcdb.cpp
 *
 *   JsonClassDatabase (JCDB) is a simple, yet effective
 *   key- value Database.
 *
 *  Author: Finn M Glas <finn@finnmglas.com>
 *
 *  History:
 *   Recreation:       2020-07-23
 *   Python Version:   2020-01-28
 *   First thought:    2019-01-04
 */

/* Imports */
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* Defines */
#define DB_LOCATION "/var/jcdb"
#define DB_VERSION "v2.0.0"

#define USAGE "jcdb\
 [-v] [-h]"

#define HELP "Common JCDB commands:\n\
\n\
"

/* The application */
int main (int argc, char **argv) {
  int aflag = 0;
  int bflag = 0;
  char *cvalue = NULL;
  int index;
  int c;

  /* Parse arguments */
  {
  opterr = 0; // return '?' rather than throwning errors

  while ((c = getopt (argc, argv, "vhc:")) != -1) {
    switch (c) {

      /* -v | Print the JCDB version */
      case 'v':
        printf("JCDB %s\n", DB_VERSION);
        return 0;
        break;

      /* -h | Print some helpful commands */
      case 'h':
        printf("usage: %s\n\n%s\n", USAGE, HELP);
        return 0;
        break;

      case 'c':
        cvalue = optarg;
        break;
      case '?':
        if (optopt == 'c')
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);
        else if (isprint (optopt))
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr,
                   "Unknown option character `\\x%x'.\n",
                   optopt);
        return 1;
      default:
        abort();
      }
    }
  }

  /* TODO: execute the given command */

  printf ("cvalue = %s\n", cvalue);

  for (index = optind; index < argc; index++)
    printf ("Non-option argument %s\n", argv[index]);
  return 0;
}
