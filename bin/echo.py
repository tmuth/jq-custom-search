
import subprocess

useless_cat_call = subprocess.run(["cat"], stdout=subprocess.PIPE, text=True, input="Hello from the other side")
print(useless_cat_call.stdout)


import subprocess

useless_cat_call = subprocess.Popen(["cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output, errors = useless_cat_call.communicate(input="Hello from the other side!")
useless_cat_call.wait()
print(output)
print(errors)



from subprocess import Popen, PIPE

# Run "cat", which is a simple Linux program that prints it's input.
process = Popen(['echo'], stdin=PIPE, stdout=PIPE,universal_newlines=True,bufsize=1)
process.stdin.write("Hello")
process.stdin.flush()
print(repr(process.stdout.readline())) # Should print 'Hello\n'
process.stdin.write(b'World\n')
process.stdin.flush()  
print(repr(process.stdout.readline())) # Should print 'World\n'

# "cat" will exit when you close stdin.  (Not all programs do this!)
process.stdin.close()
print('Waiting for cat to exit')
process.wait()
print('cat finished with return code %d' % process.returncode)