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

#define USAGE "usage: jcdb\
 [-v] [-h]"

#define HELP "Common JCDB commands:\n\
\n\
"

/* The application */
int main (int argc, char **argv) {
  int parse_char;
  int parse_non_arg_i;

  char *cvalue = NULL;

  /* Parse arguments */
  {
    /* No arguments -> Usage */
    if (argc == 0) {
      printf("%s\n", USAGE);
    }

    opterr = 0; // return '?' rather than throwning errors

    /* Loop through options args */
    while ((parse_char = getopt(argc, argv, "vhc:")) != -1) {
      switch (parse_char) {

        /* -v | Print the JCDB version */
        case 'v':
          printf("JCDB %s\n", DB_VERSION);
          return 0;
          break;

        /* -h | Print some helpful commands */
        case 'h':
          printf("%s\n\n%s\n", USAGE, HELP);
          return 0;
          break;

        case 'c':
          cvalue = optarg;
          break;

        /* Something went wrong */
        case '?':
          /* Additional info required -> Usage */
          if (optopt == 'c')
            fprintf (stderr,
              "Expected an argument for -%c.\n\n%s\n",
              optopt, USAGE);

          /* Unknown option -> Usage */
          else if (isprint (optopt))
            fprintf (stderr,
              "Unknown option `-%c'.\n\n%s\n",
              optopt, USAGE);

          /* Unknown character -> Usage */
          else
            fprintf (stderr,
              "Unknown option character `\\x%x'.\n\n%s\n",
              optopt, USAGE);

          return 1; // exit with error 1

        /* Something worse went wrong */
        default:
          return 2;
      }
    }

    /* Non- option args */
    for (parse_non_arg_i = optind;
        parse_non_arg_i < argc; parse_non_arg_i++) {
      printf ("Non-option argument %s\n", argv[parse_non_arg_i]);
    }
  }

  /* TODO: execute the given command */

  return 0;
}
