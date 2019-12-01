@echo off
setlocal

set folder=E:\Programmation\
set default_language=python

call :FirstUp result %default_language%
set default_language_folder=%result%

rem --------------------------------------------------------------------------
rem START OF SCRIPT
rem --------------------------------------------------------------------------

rem %1 => project name
rem if project name == --help OR -H, show help
if "%1"=="--help" goto :Help
if "%1"=="-H" goto :Help
goto :CreateFolder

rem --------------------------------------------------------------------------
rem END OF SCRIPT
rem --------------------------------------------------------------------------

rem --------------------------------------------------------------------------
rem START FUNCTIONS
rem --------------------------------------------------------------------------

rem Create the new folder
:CreateFolder
    if [%2]==[] (set language=%default_language%) else (set language=%2)

    call :FirstUp result %language%
    set language_folder=%result%

    rem Go in the folder
    E:
    cd /
    cd Programmation
    
    rem Create the language folder if it don't exists
    if not exist "%language_folder%" mkdir "%language_folder%"
    cd "%language_folder%"
    
    rem Create the project folder and initialize the git
    if not exist "%1" (
        mkdir %1
        cd %1

        rem Create the github repo
        rem The argument passed to the python file isn't capitalized
        python E:\Programmation\Utilities\project-creator\python\setup-github.py --project %1

        del geckodriver.log
        git init
        git remote add origin https://github.com/TanguyCavagna/%1.git
        type nul > README.md
        git add .
        git commit -m "Initial commit"
        git push -u origin master
        code .
    ) else echo This project already exists
    goto :eof

rem Help statement
rem MUST USE "" ([ESC] special char) to trigger color modification
:Help
    echo [36m----------------------------------------------------------[0m
    echo.
    echo This command is used to create a new project
    echo and open it in vscode. In addition, it will create
    echo a github repo of that project.
    echo.
    echo [31mThe project name must be the [4mFIRST[24m argument of the command[0m
    echo.
    echo And in addition of that, you can specify the language of your project
    echo has the [31m[4mSECOND[24m[0m argumment to store it in the right folder. 
    echo.
    echo [32m(By default : %folder%%default_language_folder%)[0m
    echo.
    echo [36m----------------------------------------------------------[0m
    goto :eof

:FirstUp
    setlocal EnableDelayedExpansion
    set "temp=%~2"
    set "helper=##AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ"
    set "first=!helper:*%temp:~0,1%=!"
    set "first=!first:~0,1!"
    if "!first!"=="#" set "first=!temp:~0,1!"
    set "temp=!first!!temp:~1!"
    (
        endlocal
        set "result=%temp%"
        goto :eof
    )

rem --------------------------------------------------------------------------
rem END FUNCTIONS
rem --------------------------------------------------------------------------