Object:
	-python -O -m Project.py
	-python -m *.py
pack:
	-rm PySerial.py*
	-python -O -m Project.py
	-python -m *.py
	-rm *.py
	-rm -rf backup
	-rm zp.bmp
