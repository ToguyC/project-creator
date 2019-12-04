#!/bin/bash

set +v

export default_language="python"

default_language="$(tr '[:lower:]' '[:upper:]' <<< ${default_language:0:1})${default_language:1}"

# --------------------------------------------------------------------------
# START FUNCTIONS
# --------------------------------------------------------------------------

help() {
    echo -e "\e[36m---------------------------------------------------------------------------------\e[0m"
    echo
    echo "Description:"
    echo "      This command is used to create a new projet"
    echo "      and open it in vscode. In addition, it woll create"
    echo "      a github repo of that project."
    echo
    echo "Requirements:"
    echo -e "      Before making any project, you must refer a project folder. To do this,"
    echo -e "      user the command \"\e[32mcreate --folder/-F your/absolute/folder/path\e[0m"
    echo
    echo -e "\e[31mThe project name must be the \e[4mFIRST\e[24m argument of the command\e[0m"
    echo
    echo "And in addition of that, you can specify the langugae of your project"
    echo -e "has the \e[31m\e[4mSECOND\e[24m\e[0m argument to store it in the right folder."
    echo
    echo -e "Your GitHub user and password must be set as the \e[31m\e[4mTHIRD\e[24m\e[0m and \e[31m\e[4mFOURTH\e[24m\e[0m argument"
    echo "when you will create the project. Be carefull to put your password bwtween double quotes"
    echo
    echo -e "Example: \e[32mcreate MyProject python john.doe@gmail.com \"mypassword\"\e[0m"
    echo
    echo -e "                                 \e[36mNo data is saved\e[0m"
    echo -e "\e[36m---------------------------------------------------------------------------------\e[0m"
}

setupFolder() {
    # In a function, the $# are the arguments passing to the function at the call
    if [ "$1" == "" ]; then
        echo "You must refer an absolute path"
        exit 0
    fi

    python3 $(dirname $0)/python/save-folder.py -F $1 -C $(dirname $0)/user-folder.conf
    exit 0
}

createFolder() {
    if [ "$2" != "" ]; then 
        language=$2
    fi
    
    if [ "$3" != "" ]; then 
        user=$3 
    fi
    
    if [ "$4" != "" ]; then 
        password=$4 
    fi

    language="$(tr '[:lower:]' '[:upper:]' <<< ${language:0:1})${language:1}"

    # If the configuration exist, set folder to his value
    # Else remove folder
    if [ -f $(dirname $0)/user-folder.conf ]; then
        folder=$(<$(dirname $0)/user-folder.conf)
    fi

    if [ "$folder" != "" ]; then
        cd $folder

        if [ ! -f $language ]; then
            mkdir $language
        fi
        cd $language

        if [ ! -f $1 ]; then
            mkdir $1
            cd $1

            python3 $(dirname $0)/python/setup-github.py --project $1 --driver $(dirname $0)/driver --user $user --password $password

            rm geckodriver.log
            git init
            git remote add origin https://github.com/$user/$1.git
            touch README.md
            git add .
            git commit -m "Initial commit"
            git push -u origin master
            clear
            code .
            exit 0
        else
            echo This project already exists
        fi
    else
        echo -e "\e[31mYou must refer a project folder first\e[0m. Use \"\e[32mcreate -H/--help\e[0m\" to see the help"
    fi

    exit 0
}

# --------------------------------------------------------------------------
# END FUNCTIONS
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# START OF SCRIPT
# --------------------------------------------------------------------------

if [ "$1" == "--help" ] || [ "$1" == "-H" ]; then 
    help 
fi

if [ "$1" == "--folder" ] || [ "$1" == "-F" ]; then 
    setupFolder $2
fi

createFolder $1 $2 $3 $4

# --------------------------------------------------------------------------
# END OF SCRIPT
# --------------------------------------------------------------------------