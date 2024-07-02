

import pytest
import re
import subprocess
import sys
import os 

class Test_front():
    

    verificarlo = "@VERIFICARLO_EXECUTABLE@"
    verrou = "@VERROU_EXECUTABLE@"
    pin = "@PIN_EXECUTABLE@"
    lib = "@LIB@"
    new_back = "@BACKEND_VERIFICARLO@"
    

    def launch_PENE(self, prec, op, mode, nLoop, a, b):

        cmdLine = ("{pin} -t {tool} -fp-replace 5 -counter_mode 1 -- {executable} {prec} {operation} {mode} {nLoop} {a} {b}").format(pin = self.pin, 
                                                                              tool = self.lib,
                                                                              executable = self.verrou,
                                                                              prec = prec,
                                                                              operation = op,
                                                                              mode = mode,
                                                                              nLoop = nLoop,
                                                                              a=a,
                                                                              b=b)
        
        
        out = subprocess.run(cmdLine.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        output = out.stdout.decode('utf-8')
        print("Output", output)

        p = r"\A=*[\r\n]{1,2}\s*?PENE: Pin Enabled Numerical Exploration\s*?[\r\n]{1,2}=*[\r\n]{1,2}"
        assert re.search(p, output) is not None, f"failed to launch instrumentation with PENE"

        return output
    
    def launch_verrou(self, prec, op, mode, nLoop, a, b):
        
        cmdLine = ("valgrind --tool=verrou --count-op=yes {verrou} {prec} {operation} {mode} {nLoop} {a} {b}").format(verrou = self.verrou, 
                                                                                                                    prec = prec,
                                                                                                                    operation = op,
                                                                                                                    mode = mode,
                                                                                                                    nLoop = nLoop,
                                                                                                                    a=a,
                                                                                                                    b=b)
        out = subprocess.run(cmdLine.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        output = out.stdout.decode('utf-8')

        p = r"Verrou, Check floating-point rounding errors"
        assert re.search(p, output) is not None, f"failed to launch instrumentation with Verrou{cmdLine}"

        return output

    
    def launch_verificarlo(self, prec, op, mode, nLoop, a, b):

        command = ("VFC_BACKENDS=\"{back} --count-op\" {verificalo} {prec} {operation} {mode} {nLoop} {a} {b}").format(back=self.new_back,
                                                                                                        verificalo=self.verificarlo,
                                                                                                        prec = prec,
                                                                                                        operation = op,
                                                                                                        mode = mode,
                                                                                                        nLoop = nLoop,
                                                                                                        a=a,
                                                                                                        b=b)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        output, error = process.communicate()

        # Afficher la sortie standard
        output_str = output.decode("utf-8")
        print(output_str)

        p = r"loaded backend"
        assert re.search(p, output_str) is not None, f"failed to launch instrumentation with Verificarlo"

        return output_str
    
    
    def get_result_Pene(self, pattern):

        regex = r"Result : (?P<value>-?\d+)"
        p = re.compile(regex)
        res = p.search(pattern)
        assert res, "Le motif ne contient pas de résultat valide"
        return float(res.group("value"))
    
    
    def get_result_verrou(self, pattern):

        regex = r"Result : (?P<value>\d+)"
        p = re.compile(regex)
        assert re.search(regex, pattern)
        res = p.search(pattern)

        return res 
    
    def get_result_verificarlo(self, pattern):

        regex = r"Result : (?P<value>-?\d+)"
        p = re.compile(regex)
        res = p.search(pattern)
        assert res, "Le motif ne contient pas de résultat valide"
        return float(res.group("value")) 
    
    def expectResult(self, op, nLoop, a, b):
        switcher = {
            "add": lambda a1, b1:a1+b1,
            "sub": lambda a1, b1:a1-b1,
            "mul": lambda a1, b1:a1*b1,
            "div": lambda a1, b1:a1/b1,
            "fma": lambda a1, b1:a1+a1*b1,
        }
        for i in range(int(nLoop)):
            a = switcher[op](a,b)
        return a
       
       
    @pytest.mark.parametrize("prec, op, mode, nLoop, a, b", [
            ("float", "mul", "scalar", 2, 2, 2),  
            ("float", "sub", "scalar", 10, 2, 2), 
            ("float", "add", "scalar", 10, 2, 2), 
            ("float", "fma", "scalar", 10, 2, 2),
            ("double", "mul", "scalar", 10, 2, 2), 
            ("double", "sub", "scalar", 10, 2, 2), 
            ("double", "add", "scalar", 10, 2, 2),  

    ])
    def test_result_PENE(self, prec, op, mode, nLoop, a, b):
        output_PENE = self.launch_PENE(prec, op, mode, nLoop, a, b)
        result_pene=self.get_result_Pene(output_PENE)  
        result_expected=self.expectResult(op, nLoop, a, b)
        assert result_pene==result_expected, \
            f"Pene have note the expected result"


    @pytest.mark.parametrize("prec, op, mode, nLoop, a, b", [
            ("float", "mul", "scalar", 2, 2, 2),  
            ("float", "sub", "scalar", 10, 2, 2), 
            ("float", "add", "scalar", 10, 2, 2), 
            ("float", "fma", "scalar", 10, 2, 2),
            ("double", "mul", "scalar", 10, 2, 2), 
            ("double", "sub", "scalar", 10, 2, 2), 
            ("double", "add", "scalar", 10, 2, 2),  
    ])
    def test_result_Verificarlo(self, prec, op, mode, nLoop, a, b):
        output_verificarlo = self.launch_verificarlo(prec, op, mode, nLoop, a, b)
        result_verificarlo=self.get_result_verificarlo(output_verificarlo)
        result_expected=self.expectResult(op, nLoop, a, b)
        assert result_verificarlo==result_expected, \
            f"verificarlo have note the expected result"
    
    
if __name__ == "__main__":
    pytest.main()
    