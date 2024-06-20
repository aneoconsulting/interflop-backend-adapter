


import pytest
import re
import subprocess
from pathlib import Path
import sys
import os 

class Test_front():
    
    counterModes = ["0", "1", "2"]

    precisions = ["float", "double"]
    operations = ["add", "sub", "mul", "div", "fma"]
    modes = ["scalar", "simd"]


    verificarlo = "@VERIFICARLO_EXECUTABLE@"
    verrou = "@VERROU_EXECUTABLE@"
    pin = "@PIN_EXECUTABLE@"
    lib = "@LIB@"
    new_back = "@BACKEND_VERIFICARLO@"

    expected = r"0x1\.000002p\+0"


    def launch_PENE(self):

        cmdLine = ("{pin} -t {tool} -fp-replace 5 -counter_mode 1 -- {executable}").format(pin = self.pin, 
                                                                              tool = self.lib,
                                                                              executable = self.verrou,
                                                                              )
        
        
        out = subprocess.run(cmdLine.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        output = out.stdout.decode('utf-8')
        print(output)

        p = r"\A=*[\r\n]{1,2}\s*?PENE: Pin Enabled Numerical Exploration\s*?[\r\n]{1,2}=*[\r\n]{1,2}"
        assert re.search(p, output) is not None, f"failed to launch instrumentation with PENE"

        return output
    
     
    def launch_verificarlo(self):

        command = ("VFC_BACKENDS=\"{back} --count-op\" {verificarlo}").format(back=self.new_back,
                                                                             verificarlo=self.verificarlo,
                                                                            )
        
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        output, error = process.communicate()

        output_str = output.decode("utf-8")
        print(output_str)

        p = r"loaded backend"
        assert re.search(p, output_str) is not None, f"failed to launch instrumentation with Verificarlo"

        return output_str
    
    def checkout_binary(self, pattern, expected):

        p = re.compile(expected)

        res = p.search(pattern)
        assert res, "The result is false"
    

    def test_binary(self):
        
        output=self.launch_PENE()
        self.checkout_binary(output, self.expected)

        output=self.launch_verificarlo()
        self.checkout_binary(output, self.expected)


if __name__ == "__main__":
    pytest.main()



    