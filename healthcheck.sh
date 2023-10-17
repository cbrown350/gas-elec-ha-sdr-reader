#!/bin/sh

netstat -ltn | grep -c ':1234' > /dev/null; if [ 0 != $? ]; then exit 1; else netstat -tln | grep -c ':2222' > /dev/null; if [ 0 != $? ]; then exit 1; else exit 0; fi; fi;\": stat netstat -ltn | grep -c ':1234' > /dev/null; if [ 0 != $? ]; then exit 1; else netstat -tln | grep -c ':2222' > /dev/null; if [ 0 != $? ]; then exit 1; else exit 0; fi; fi;