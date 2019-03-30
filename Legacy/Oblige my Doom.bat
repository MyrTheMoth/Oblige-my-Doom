@ECHO off

SET oblige_path=""
SET oblige_config=""
SET source_port=""
SET iwad=""
SET pwads=""

IF [%1] EQU [] (
    GOTO MAIN
    ) ELSE (
        SET config=%~n1%~x1
        GOTO READCONFIG
    )

:MAIN 

CLS
ECHO Welcome to Oblige my Doom!
ECHO:
ECHO What would you like to do?
ECHO:
ECHO A: Start a new Game
ECHO:
ECHO B: Quit
ECHO:
CHOICE /N /C AB /M "Choose an option (A/B): "
IF %ERRORLEVEL% == 1 GOTO CONFIG
IF %ERRORLEVEL% == 2 GOTO QUIT

:CONFIG

CLS
SET /P "config=Type the name of your Config File: "
ECHO:

:READCONFIG

ECHO Reading %config%
ECHO:

FOR /F "tokens=1*" %%i IN (%config%) DO (
    ECHO %%i %%j
    ECHO:
    IF %%i==oblige_path SET oblige_path=%%j
    IF %%i==oblige_config SET oblige_config=%%j
    IF %%i==source_port SET source_port=%%j
    IF %%i==iwad SET iwad=%%j
    IF %%i==pwads SET pwads=%%j
)

:NEW

ECHO Generating Oblige Map, this may take a while, Generation time depends on your Oblige Config
ECHO:
%oblige_path% --verbose --batch OUTPUT.wad --load %oblige_config%
ECHO Finished Oblige Map Generation
ECHO:

ECHO Starting Game
ECHO:
%source_port% -iwad %iwad% -file OUTPUT.wad %pwads%
ECHO Game Finished
ECHO:

CHOICE /N /M "Would you like to delete the Map? (Y/N): "
ECHO:
IF %ERRORLEVEL% == 1 GOTO DELETEMAP
IF %ERRORLEVEL% == 2 GOTO SAVEMAP

:DELETEMAP

DEL OUTPUT.wad
ECHO Oblige Map Deleted
ECHO:
GOTO NEWMAP

:SAVEMAP

SET /P "wadname=Give a name to the map wad file (No .wad or invalid characters): "
ECHO:
REN OUTPUT.wad "%wadname%.wad"

:NEWMAP

CHOICE /N /M "Would you like another Map generated with the same Config? (Y/N): "
ECHO:
IF %ERRORLEVEL% == 1 GOTO NEW
IF %ERRORLEVEL% == 2 GOTO NEWCONFIG

:NEWCONFIG

CHOICE /N /M "Would you like another Map with a new Config? (Y/N): "
ECHO:
IF %ERRORLEVEL% == 1 GOTO CONFIG
IF %ERRORLEVEL% == 2 GOTO QUIT

:QUIT
CLS
EXIT