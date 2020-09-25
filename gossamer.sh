#!/bin/bash
if [ $1 == "component" ]
then
    python3 gossamer/generate_component.py $2 $3
elif [ $1 == "build" ]
then
    python3 gossamer/build_project.py $2
elif [ $1 == "new" ]
then
    python3 gossamer/generate_project.py $2
else
    echo "Invalid command: $1"
fi
