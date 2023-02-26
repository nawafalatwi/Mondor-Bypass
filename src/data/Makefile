compile: test.cs
	csc -nologo -reference:MSCaptcha.dll -target:exe -out:test.exe test.cs

run: test.exe
	./test

comrun: compile run
