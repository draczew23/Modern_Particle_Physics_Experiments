@echo on

set WORKING_DIR=%USERPROFILE%\Docker

echo Creating working directory: %WORKING_DIR% 
mkdir %WORKING_DIR%

echo Checking for container updates.
docker pull akalinow/root-fedora35

echo Starting container.
docker run -ti --rm -v %WORKING_DIR%:/scratch -p 8000:8000 akalinow/root-fedora35

pause
