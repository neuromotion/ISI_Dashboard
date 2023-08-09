:: From https://gist.github.com/JohannesDeml/779b29128cdd7f216ab5000466404f11
:: Convert vector file formats in the current folder and their subsfolders

@echo off
setlocal ENABLEDELAYEDEXPANSION

:: Possible paths to check for the installation
set "inkscapePaths[1]=C:\Program Files\Inkscape\bin\inkscape.com"
set "inkscapePaths[2]=C:\Program Files\Inkscape\bin\inkscape.exe"
set "inkscapePaths[3]=C:\Program Files\Inkscape\inkscape.com"
set "inkscapePaths[4]=C:\Program Files (x86)\Inkscape\bin\inkscape.com"
set "inkscapePaths[5]=C:\Program Files (x86)\Inkscape\bin\inkscape.exe"
set "inkscapePaths[6]=C:\Program Files (x86)\Inkscape\inkscape.com"
set "inkscapePaths[7]=%UserProfile%\scoop\apps\inkscape\current\bin\inkscape.exe"

set "inkscapePath="
set /a "pathIndex=1"

:: Find the inkscape installation path
:inkscapepath_loop_start
if defined inkscapePaths[%pathIndex%] (
	set "currentPath=!inkscapePaths[%pathIndex%]!"
	if exist "!currentPath!" (
		:: found installation path
		set "inkscapePath=!currentPath!"
		goto :inkscapepath_loop_end
	)
	set /a "pathIndex+=1"
	goto :inkscapepath_loop_start
) else (
	echo Can't find Inkscape installation, aborting.
    goto end
)
:inkscapepath_loop_end

:: Set the path to allow for spaces without any needed additional quotes
set inkscapePath="%inkscapePath%"

:: Define supported input file extensions
set validInput=svg pdf eps emf wmf ps ai
set validInputString=
(for %%a in (%validInput%) do ( 
   set validInputString=!validInputString!, %%a
))
:: Remove the leading comma
set validInputString=%validInputString:~2%

:: Define supported output file extensions
set validOutput=svg png pdf eps emf wmf ps
set validOutputString=
(for %%a in (%validOutput%) do ( 
   set validOutputString=!validOutputString!, %%a
))
:: Remove the leading comma
set validOutputString=%validOutputString:~2%

:: If this can't be run, then the version is an older one
FOR /F "tokens=* USEBACKQ" %%g IN (`%inkscapePath% --version`) do (SET "inkscapeVersion=%%g")
if "%inkscapeVersion%" EQU "" (
	set inkscapeVersion=0.x
	set /a inkscapeMajorVersion=0
) else (
set /a inkscapeMajorVersion=%inkscapeVersion:~9,1%
)

echo.
echo This script allows you to convert all files in this folder from one file type to another
echo Running with %inkscapeVersion% from %inkscapePath%
echo (type q to quit at any question)
echo.

set valid=0
echo Allowed file types for source: %validInputString%
:whileInNotCorrect
	set /p sourceType=What file type do you want to use as a source?
	if "%sourceType%" EQU "q" exit /b
	for %%a in (%validInput%) do (
	  if "%%a"=="%sourceType%" (
		set valid=1
		goto inSet
	  )
	)
	if %valid% EQU 0 (
		echo Invalid input! Please use one of the following: %validInputString%
		goto :whileInNotCorrect
	)

:inSet
echo.

set valid=0
echo Allowed file types for output: %validOutputString%
:whileOutNotCorrect
	set /p outputType=What file type do you want to convert to? 
	if "%outputType%" EQU "q" exit /b
	for %%a in (%validOutput%) do (
	  if "%%a"=="%outputType%" (
		set valid=1
		goto outSet
	  )
	)
	if %valid% EQU 0 (
		echo Invalid input! Please use one of the following: %validOutputString%
		goto :whileOutNotCorrect
	)

:outSet

if "%outputType%" EQU "%sourceType%" (
	echo Input and Output are the same, no point in doing anything. Exiting...
	exit /b
)

echo.

:: Older inkscape versions need to generate a pdf before generating svgs
if %inkscapeMajorVersion% EQU 0 (
	set toDelOrNot=n
	if "%sourceType%" NEQ "pdf" (
		if "%outputType%" EQU "%validOutput4%" (
			set valid=0
			:whilePdfDelNotCorrect
				set /p toDelOrNot=EPS to SVG also generates pdfs, delete these after conversion? (y/n^) 
				if "%toDelOrNot%" EQU "y" set valid=1
				if "%toDelOrNot%" EQU "n" set valid=1
				if "%toDelOrNot%" EQU "q" exit /b
				if %valid% EQU 0 (
					echo Invalid input! Please type either y or n.
					goto :whilePdfDelNotCorrect
				)
		)
	)
)

:: Set DPI for exported file
:whileNotValidDpiNumber
	set /p dpi=With what dpi should it be exported (e.g. 300)? 
	if "%dpi%" EQU "q" exit /b
	IF %dpi% NEQ +%dpi% (
		echo Invalid input! Please input an actual number.
		goto :whilenotValidDpiNumber
	)
echo.

:: count how many files we need to convert before converting!
set /a total=0
for /R %%i in (*.%sourceType%) do (	set /a total=total+1 )
echo Found %total% file(s) of type *.%sourceType% in the current folder (%~dp0)

echo.

set /a count=0
:: Running through all files found with the defined ending
if %inkscapeMajorVersion% NEQ 0 (
	:: Inkscape 1.0 and newer
	for /R %%i in (*.%sourceType%) do (
		set /a count=count+1
		
		:: Create out folder if it does not exist
		if not exist "%%~di%%~piout" mkdir "%%~di%%~piout"
		
		echo %%i -^> %%~di%%~piout\%%~ni.%outputType% ^[!count!/%total%^]
		
		%inkscapePath% --export-filename="%%~di%%~piout\%%~ni.%outputType%" --export-dpi=%dpi% "%%i"
	)
) else (
	:: Inkscape 0.9.x and older
	for /R %%i in (*.%sourceType%) do (
		set /a count=count+1
		
		:: Create out folder if it does not exist
		if not exist "%%~di%%~piout" mkdir "%%~di%%~piout"
		
		echo %%i -^> %%~di%%~piout\%%~ni.%outputType% ^[!count!/%total%^]
		
		if "%outputType%" NEQ "%validOutput4%" (
			%inkscapePath% --without-gui --file="%%i" --export-%outputType%="%%~di%%~piout\%%~ni.%outputType%" --export-dpi=%dpi%
		) else (
			if "%sourceType%" NEQ "pdf" (
				%inkscapePath% --without-gui --file="%%i" --export-pdf="%%~di%%~piout\%%~ni.pdf" --export-dpi=%dpi%
			)
			%inkscapePath% --without-gui -z -f "out\%%~ni.pdf" -l "%%~di%%~piout\%%~ni.%validOutput4%"
			if "%toDelOrNot%" EQU "y" (
				del "%%~ni.pdf" /f /q
			)
		)
	)
)

echo.
echo %count% file(s) converted from %sourceType% to %outputType%! (Saved in out folder)
echo.

:end
pause