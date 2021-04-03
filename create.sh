#!/bin/bash
# --------------------------------------------------------------------------
# START OF CONTSANTS
# --------------------------------------------------------------------------
WHITE="\033[1;37m";
NC="\033[0m";
# --------------------------------------------------------------------------
# END OF CONSTANTS
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# START OF FUNCTIONS
# --------------------------------------------------------------------------
function script_help {
    printf "${WHITE}NAME${NC}\n";
    printf "\tcreate - create a programmation project and link it to github\n";
    printf "\n";
    printf "${WHITE}SYNOPSIS${NC}\n";
    printf "\t${WHITE}create${NC} [-h] [-c] [-g] [-n project-name] [-f project-path] [-l programming-language]\n";
    printf "\n";
    printf "${WHITE}DESCRIPTION${NC}\n";
    printf "\tThis manual page document the command ${WHITE}create${NC}. ${WHITE}create${NC} make a new project and open it\n";
    printf "\tin vscode. In addition, it will create a github repo of that project.\n";
    printf "\n";
    printf "${WHITE}OPTIONS${NC}\n";
    printf "\t-h\tShow this manual page.\n";
    printf "\n";
    printf "\t-c\tSave the AUTH_TOKEN of your github account.\n";
    printf "\n";
    printf "\t-g\tOpen the GUI.\n";
    printf "\n";
    printf "\t-n project-name\n";
    printf "\t\tSpecify the name of the document.\n"
    printf "\n";
    printf "\t-f project-path\n";
    printf "\t\tSpecify the path of the project.\n"
    printf "\n";
    printf "\t-l programming-language\n";
    printf "\t\tSpecify the programming language.\n"
    printf "\n";
    printf "${WHITE}AUTHOR${NC}\n";
    printf "\tTanguy Cavagna - tanguy.cvgn@gmail.com\n";
    printf "\n";
    printf "${WHITE}COPYRIGHT${NC}\n";
    printf "\tFair Use\n";
}

function to_lower_case {
    echo "${1,,}";
}

function setup_folder {
    echo $1 > user-folder.conf
}

function save_auth_token {
    openssl genrsa -out ./key.txt 2048 > /dev/null
    echo
    read -s -p "Enter your token: " token
    echo $token | openssl rsautl -inkey ./key.txt -encrypt > token.txt
}

function decrypt_token {
    openssl rsautl -inkey ./key.txt -decrypt < token.txt
}
# --------------------------------------------------------------------------
# END OF FUNCTIONS
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# START OF SCRIPT
# --------------------------------------------------------------------------
# If a letter is followed by a colon, a value is required
while getopts ":hcn:f:l:" arg; do
    case $arg in
        h) script_help;;
        c) save_auth_token;;
        n) project_name=$OPTARG;;
        f) setup_folder $OPTARG;;
        l) language=$OPTARG;;
        \? ) echo "Unknown option: -$OPTARG" >&2; exit 1;;
        :  ) echo "Missing option argument for -$OPTARG" >&2; exit 1;;
        *  ) echo "Unimplemented option: -$OPTARG" >&2; exit 1;;
    esac
done

if [ ! -z "$language" ] && [ -z "$project_name" ]; then
    echo "Missing -n.";
    exit 1;
fi
if [ ! -z "$project_name" ] && [ -z "$language" ]; then
    echo "Missing -l.";
    exit 1;
fi
if [ -z "$project_name" ] && [ -z "$language" ]; then
    exit 1;
fi

if [ ! -f "./user-folder.conf" ]; then
    echo "No folder as been setup."
    exit 1;
fi

projects_folder=$(head -n 1 ./user-folder.conf);

mkdir -p "${projects_folder}/${language}";
mkdir -p "${projects_folder}/${language}/${project_name}";

token=$(decrypt_token);
curl -s -H "Authorization: token ${token}" --data "{\"name\":\"${project_name}\", \"private\": true}" https://api.github.com/user/repos > /dev/null;

cd "${projects_folder}/${language}/${project_name}";
read -p "Github username: " username;
git init;
git remote add origin git@github.com:${username}/${project_name}.git;
echo "# ${project_name}" > README.md;
git add .;
git commit -m "Initial commit";
git push --set-upstream origin master

code "${projects_folder}/${language}/${project_name}";
# --------------------------------------------------------------------------
# END OF SCRIPT
# --------------------------------------------------------------------------