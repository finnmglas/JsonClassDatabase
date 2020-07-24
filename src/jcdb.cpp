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
#include <cstring>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>

#include "../lib/json.hpp"

using json = nlohmann::json;

/* Defines */
#define DB_LOCATION "/var/jcdb"
#define DB_VERSION "v2.0.0"

#define USAGE "usage: jcdb\
 [-v] [-h] <command> [<db>] [<class>] [<instance>]"

#define HELP "Common JCDB commands:\n\
\n\
'help': print this text\n\
    help\n\
\n\
'version': print the JCDB version\n\
    version\
"

/* The application */
int main (int argc, char **argv) {
  int parse_char;
  int parse_non_arg_i;

  char *parsed_command = NULL;
  char *parsed_db = NULL;
  char *parsed_instance = NULL;

  bool parsed_flag_help = false;
  bool parsed_flag_version = false;

  parse_arguments: {
    /* No arguments -> Help */
    if (argc == 1) {
      printf("%s\n\n%s\n", USAGE, HELP);
      return 0;
    }

    opterr = 0; // return '?' rather than throwning errors

    /* Loop through options args */
    while ((parse_char = getopt(argc, argv, "hv")) != -1) {
      switch (parse_char) {

        /* -h | Print some helpful commands */
        case 'h':
          parsed_flag_help = true;
          break;

        /* -v | Print the JCDB version */
        case 'v':
          parsed_flag_version = true;
          break;

        /* Something went wrong */
        case '?':
          /* Unknown option -> Usage */
          if (isprint(optopt))
            fprintf(stderr,
              "Unknown option '-%c'.\n\n%s\n",
              optopt, USAGE);

          /* Unknown character -> Usage */
          else
            fprintf(stderr,
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
      if (parse_non_arg_i == 1)
        parsed_command = argv[parse_non_arg_i];
      else if (parse_non_arg_i == 2)
        parsed_db = argv[parse_non_arg_i];
      else if (parse_non_arg_i == 3)
        parsed_instance = argv[parse_non_arg_i];
    }
  }

  execute_command: {

    /* help | Print some helpful commands (same as -h) */
    if (parsed_flag_help ||
        parsed_command && strcmp(parsed_command, "help") == 0) {
      printf("%s\n\n%s\n", USAGE, HELP);
    }

    /* version | Print the JCDB version (same as -v) */
    else if (parsed_flag_version ||
        strcmp(parsed_command, "version") == 0) {
      printf("JCDB %s\n", DB_VERSION);
    }

    /* Unknown command */
    else {
      fprintf (stderr,
        "Unknown command '%s'.\n\n%s\n",
        parsed_command, USAGE);
      return 3;
    }
  }

  return 0;
}
