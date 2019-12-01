@echo off
setlocal

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
if "%1"=="--folder" goto :SetupFolder
if "%1"=="-F" goto :SetupFolder
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
    if not [%3]==[] (set user=%3)
    if not [%4]==[] (set password=%4)

    call :FirstUp result %language%
    set language_folder=%result%

    rem If the configuration exist, set folder to his value
    rem Else remove folder
    if exist %~dp0user-folder.conf (
        set /P folder=<%~dp0user-folder.conf
    ) else set folder=

    rem Only if folder is defined, create the project
    if defined folder (
        rem 1) Change disk
        rem 2) Goto the root
        rem 3) Goto the folder
        %folder:~0,2%
        cd %folder:~2,1%
        cd %folder:~3%
        
        rem Create the language folder if it don't exists
        if not exist "%language_folder%" mkdir "%language_folder%"
        cd "%language_folder%"
        
        rem Create the project folder and initialize the git
        if not exist "%1" (
            mkdir %1
            cd %1

            rem Create the github repo
            rem The argument passed to the python file isn't capitalized
            python %~dp0python\setup-github.py --project %1 --user %user% --password %password%

            del geckodriver.log
            git init
            git remote add origin https://github.com/TanguyCavagna/%1.git
            type nul > README.md
            git add .
            git commit -m "Initial commit"
            git push -u origin master
            cls
            code .
            exit
        ) else echo This project already exists
    ) else echo [31mYout muse refer a project folder first[0m. Use "[32mcreate --help/-H[0m" to see the help
    goto :eof

rem Setup the projects folder
:SetupFolder
    if [%2]==[] echo You must refer an absolute folder path & goto :eof

    python %~dp0python\save-folder.py --folder %2 --conf %~dp0user-folder.conf
    goto :eof

rem Help statement
rem MUST USE "" ([ESC] special char) to trigger color modification
:Help
    echo [36m---------------------------------------------------------------------------------[0m
    echo.
    echo Description:
    echo        This command is used to create a new project
    echo        and open it in vscode. In addition, it will create
    echo        a github repo of that project.
    echo.
    echo Requirements:
    echo        Before making any project, you must refer a project folder. To do this, 
    echo        use the command "[32mcreate --folder/-F your/absolute/folder/path[0m"
    echo.
    echo [31mThe project name must be the [4mFIRST[24m argument of the command[0m
    echo.
    echo And in addition of that, you can specify the language of your project
    echo has the [31m[4mSECOND[24m[0m argumment to store it in the right folder. 
    echo.
    echo Your GitHub user and password must be set as the [31m[4mTHIRD[24m[0m and [31m[4mFOURTH[24m[0m argument
    echo when you will create the project. Be carefull to put your password bwtween double quotes
    echo.
    echo Example: [32mcreate MyProject python john.doe@gmail.com "mypassword"[0m
    echo.
    echo                                  [36mNo data is saved[0m
    echo.
    echo [36m---------------------------------------------------------------------------------[0m
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