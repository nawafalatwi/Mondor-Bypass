compile: gen.cs
	csc -nologo -reference:MSCaptcha.dll -target:exe -out:gen.exe gen.cs

run: gen.exe
	./gen

comrun: compile run
