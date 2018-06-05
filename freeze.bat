CALL env_build\Scripts\activate
.bat
cd spring-launcher\spring_launcher

pyinstaller --windowed launcher.spec -y
